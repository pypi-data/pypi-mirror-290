import posixpath
import uuid
from typing import Dict, List, Optional, Sequence, Union

# SQLAlchemy imports
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload, load_only

# Entities imports
from mlflow.pydantic_v1 import BaseModel
from mlflow.entities.mlfoundry_artifacts.artifact_version_in_transit import (
    ArtifactVersionInTransit,
)
from mlflow.entities.mlfoundry_artifacts.enums import (
    ArtifactType,
    ArtifactVersionStatus,
    ArtifactVersionTransitStatus,
    EventType,
)
from mlflow.entities.view_type import ViewType
from mlflow.entities.mlfoundry_artifacts.artifact import Artifact, ArtifactVersion

# Store imports
from mlflow.store.db.base_sql_achemy_store import BaseSqlAlchemyStore
from mlflow.store.mlfoundry_artifacts.dbmodels.models import (
    SqlArtifact,
    SqlArtifactVersion,
    SqlArtifactMaxVersion,
    SqlArtifactVersionInTransit,
    SqlEvent,
    ArtifactsRootSequence,
)
from mlflow.store.entities.paged_list import PagedList
from mlflow.store.utils import paginate_query, err_if_not_exist_wrapper
from mlflow.utils.time_utils import now_utc
from mlflow.utils.uri import append_to_uri_path


class SqlAlchemyArtifactStore(BaseSqlAlchemyStore):

    def __init__(self, db_uri: str, default_artifact_root: str=None):
        super().__init__(db_uri, default_artifact_root)

    def _create_artifact_max_version(self, session: Session, artifact_id: uuid.UUID) -> None:
        artifact_max_version = SqlArtifactMaxVersion(artifact_id=artifact_id, max_version=0)
        session.add(artifact_max_version)

    # Artifact CRUDs
    def create_artifact(self, artifact: Artifact) -> Artifact:
        with self.ManagedSessionMaker() as session:
            sql_artifact = SqlArtifact(
                id=artifact.id,
                experiment_id=artifact.experiment_id,
                type=artifact.type,
                name=artifact.name,
                fqn=artifact.fqn,
                description=artifact.description,
                artifact_storage_root=artifact.artifact_storage_root,
                created_by=artifact.created_by,
            )
            session.add(sql_artifact)

            # Add the artifact to the artifact_max_version table
            self._create_artifact_max_version(session=session, artifact_id=artifact.id)

            session.flush()
            return sql_artifact.to_entity()

    def _get_artifact(
        self,
        experiment_id: int,
        artifact_type: ArtifactType,
        artifact_id: Optional[uuid.UUID] = None,
        name: Optional[str] = None,
        view_type: ViewType = ViewType.ACTIVE_ONLY,  # TODO: Implement view_type
    ) -> Optional[Artifact]:
        with self.ManagedSessionMaker() as session:
            filters = [
                SqlArtifact.experiment_id == experiment_id,
                SqlArtifact.type == artifact_type.value,
                or_(SqlArtifact.name == name, SqlArtifact.id == artifact_id),
            ]
            query = session.query(SqlArtifact).filter(*filters)
            instance = query.one_or_none()
            return instance.to_entity() if instance else None

    def get_artifact_by_id(
        self,
        experiment_id: int,
        artifact_type: ArtifactType,
        artifact_id: uuid.UUID,
        view_type: ViewType = ViewType.ACTIVE_ONLY,
    ) -> Optional[Artifact]:
        return self._get_artifact(
            experiment_id=experiment_id,
            artifact_type=artifact_type,
            artifact_identifier=artifact_id,
            name=None,
            view_type=view_type,
        )

    def get_artifact_by_name(
        self,
        experiment_id: int,
        artifact_type: ArtifactType,
        name: str,
        view_type: ViewType = ViewType.ACTIVE_ONLY,
    ) -> Optional[Artifact]:
        return self._get_artifact(
            experiment_id=experiment_id,
            artifact_type=artifact_type,
            artifact_id=None,
            name=name,
            view_type=view_type,
        )

    def _update_artifact(self, session: Session, artifact_id: uuid.UUID) -> Artifact:
        updated = (
            session.query(SqlArtifact)
            .filter(SqlArtifact.id == artifact_id)
            .update({"updated_at": now_utc()})
        )

        if updated == 0:
            raise ValueError(f"No artifact with ID {artifact_id} found")
        elif updated > 1:
            raise ValueError(f"More than one row updated when expected one")

    # Artifact Versions In Transit CRUDs
    def create_artifact_version_in_transit(
        self,
        artifact: Artifact,
    ) -> ArtifactVersionInTransit:
        with self.ManagedSessionMaker() as session:
            id_ = str(session.query(ArtifactsRootSequence.next_value()).scalar())
            artifact_storage_root = append_to_uri_path(
                artifact.artifact_storage_root, id_, posixpath.sep
            )
            instance = SqlArtifactVersionInTransit(
                artifact_id=artifact.id,
                artifact_storage_root=artifact_storage_root,
                status=ArtifactVersionTransitStatus.CREATED.value,
            )
            session.add(instance)
            session.flush()

            return instance.to_entity()

    @err_if_not_exist_wrapper("artifact version in transit")
    def get_artifact_version_in_transit(
        self,
        version_id: uuid.UUID,
        status: ArtifactVersionTransitStatus,
    ) -> Optional[ArtifactVersionInTransit]:
        with self.ManagedSessionMaker() as session:
            instance = (
                session.query(SqlArtifactVersionInTransit)
                .options(joinedload(SqlArtifactVersionInTransit.artifact))
                .filter_by(version_id=version_id, status=status.value)
                .one_or_none()
            )
            return instance.to_entity() if instance else None

    def _delete_artifact_version_in_transit(self, session: Session, version_id: uuid.UUID) -> None:
        instance = (
            session.query(SqlArtifactVersionInTransit)
            .filter_by(version_id=version_id)
            .one_or_none()
        )
        if not instance:
            raise ValueError(
                f"No ArtifactVersionInTransit with version_id={version_id} found"
            )
        session.delete(instance)

    def finalize_artifact_version(
        self,
        artifact: Artifact,
        artifact_version: ArtifactVersion,
    ) -> ArtifactVersion:

        artifact_metadata = artifact_version.artifact_metadata or {}
        internal_metadata = artifact_version.internal_metadata or {}
        internal_metadata_dict = (
            internal_metadata.dict()
            if isinstance(internal_metadata, BaseModel)
            else internal_metadata
        )

        with self.ManagedSessionMaker() as session:
            artifact_id = artifact_version.artifact_id
            # select for update (lock)
            artifact_max_version = (
                session.query(SqlArtifactMaxVersion)
                .filter(SqlArtifactMaxVersion.artifact_id == artifact_id)
                .with_for_update()
                .one_or_none()
            )
            if not artifact_max_version:
                raise ValueError(f"No artifact with ID {artifact_id} found")

            # add to main table
            new_version = artifact_max_version.max_version + 1
            sql_artifact_version = SqlArtifactVersion(
                id=artifact_version.id,
                artifact_id=artifact_id,
                artifact_type=artifact.type,
                version=new_version,
                artifact_storage_root=artifact_version.artifact_storage_root,
                status=ArtifactVersionStatus.COMMITTED.value,
                description=artifact_version.description,
                artifact_metadata=artifact_metadata,
                internal_metadata=internal_metadata_dict,
                data_path=artifact_version.data_path,
                step=artifact_version.step if artifact_version.run_id else None,
                artifact_size=artifact_version.artifact_size,
                created_by=artifact_version.created_by,
                run_uuid=artifact_version.run_id if artifact_version.run_id else None,
            )
            try:
                session.add(sql_artifact_version)
                # update the artifact to Update the updated_at field
                self._update_artifact(session=session, artifact_id=artifact_id)
                session.flush()
            except IntegrityError as e:
                raise ValueError(
                    f"Failed to finalize artifact version with ID {artifact_version.id}"
                ) from e

            # Delete from transit table
            self._delete_artifact_version_in_transit(
                session=session, version_id=artifact_version.id
            )
            # Calculate the new max version
            artifact_max_version.max_version = max(
                artifact_max_version.max_version, new_version
            )
            session.flush()

            # create an event
            event = SqlEvent(
                run_uuid=artifact_version.run_id if artifact_version.run_id else None,
                artifact_id=artifact_id,
                artifact_version_id=artifact_version.id,
                type=EventType.OUTPUT.value,
            )
            session.add(event)

            # return ArtifactVersion entity
            # note that to_entity will end up firing a select call for `artifact` relationship
            artifact_version = sql_artifact_version.to_entity()

        return artifact_version

    # Artifact Versions CRUDs
    def create_artifact_version(
        self, artifact: Artifact, artifact_version: ArtifactVersion
    ) -> ArtifactVersion:
        with self.ManagedSessionMaker() as session:
            sql_artifact_version = SqlArtifactVersion(
                artifact_id=artifact_version.artifact_id,
                artifact_type=artifact.type.value,
                version=artifact_version.version,
                artifact_storage_root=artifact_version.artifact_storage_root,
                artifact_metadata=artifact_version.artifact_metadata,
                internal_metadata=artifact_version.internal_metadata,
                data_path=artifact_version.data_path,
                description=artifact_version.description,
                status=artifact_version.status,
                step=artifact_version.step,
                created_by=artifact_version.created_by,
            )
            session.add(sql_artifact_version)
            session.commit()
            return sql_artifact_version.to_entity()

    # Get or List Artifact Versions
    def _get_artifact_version(
        self,
        version_id: Optional[uuid.UUID] = None,
        experiment_id: Optional[int] = None,
        artifact_name: Optional[str] = None,
        version: Optional[int] = None,
        artifact_type: Optional[ArtifactType] = None,
        fqn: Optional[str] = None,
        status: Optional[ArtifactVersionStatus] = None,
    ) -> Optional[ArtifactVersion]:
        with self.ManagedSessionMaker() as session:
            query = session.query(SqlArtifactVersion).options(
                joinedload(SqlArtifactVersion.artifact)
            )

            # Apply filters based on the provided arguments
            filters = []
            if fqn:
                artifact_fqn, _version = ArtifactVersion.get_artifact_fqn_and_version(fqn)
                filters.append(SqlArtifact.fqn == artifact_fqn)
                version = _version if version is None else version
            elif version_id:
                filters.append(SqlArtifactVersion.id == version_id)
            elif experiment_id and artifact_name and artifact_type:
                filters.extend(
                    [
                        SqlArtifact.experiment_id == experiment_id,
                        SqlArtifact.name == artifact_name,
                        SqlArtifact.type == artifact_type.value,
                    ]
                )
            else:
                raise ValueError("Invalid arguments provided")

            # Apply additional filters
            if status:
                filters.append(SqlArtifactVersion.status == status.value)

            # Fetch speific version when version is specified, else fetch the latest version
            if version is not None and version != -1:
                query = query.filter(SqlArtifactVersion.version == version)
            elif version == -1 or fqn or (experiment_id and artifact_name and artifact_type):
                query = query.order_by(SqlArtifactVersion.version.desc()).limit(1)
            query = query.filter(*filters)
            result = query.one_or_none()
            return result.to_entity() if result else None

    @err_if_not_exist_wrapper("artifact version")
    def get_artifact_version_by_id(
        self, version_id: uuid.UUID, status: Optional[ArtifactVersionStatus] = None
    ) -> Optional[ArtifactVersion]:
        return self._get_artifact_version(version_id=version_id, status=status)

    @err_if_not_exist_wrapper("artifact version")
    def get_artifact_version_by_fqn(
        self, fqn: str, status: Optional[ArtifactVersionStatus] = None
    ) -> Optional[ArtifactVersion]:
        return self._get_artifact_version(fqn=fqn, status=status)

    @err_if_not_exist_wrapper("artifact version")
    def get_artifact_version(
        self,
        experiment_id: int,
        artifact_name: str,
        version: int,
        artifact_type: ArtifactType,
        status: Optional[ArtifactVersionStatus] = None,
    ) -> Optional[ArtifactVersion]:
        return self._get_artifact_version(
            experiment_id=experiment_id,
            artifact_name=artifact_name,
            artifact_type=artifact_type,
            version=version,
            status=status,
        )

    def list_artifact_versions(
        self,
        artifact_id: Optional[uuid.UUID] = None,
        run_ids: Optional[List[str]] = None,
        run_steps: Optional[List[str]] = None,
        experiment_ids: Optional[List[uuid.UUID]] = None,
        artifact_types: Optional[List[ArtifactType]] = None,
        statuses: Optional[Sequence[ArtifactVersionStatus]] = None,
        max_results: Optional[int] = None,
        page_token: Optional[str] = None,
    ) -> PagedList[ArtifactVersion]:

        filters = []

        # Apply filters based on the provided arguments
        if artifact_id:
            filters.append(SqlArtifactVersion.artifact_id == artifact_id)
        elif run_ids:
            filters.append(SqlArtifactVersion.run_uuid.in_(run_ids))
            if run_steps:
                if len(run_ids) != 1:
                    raise ValueError(
                        "Only one run_id must be passed in `run_ids` when `run_steps` is given"
                    )
                filters.append(SqlArtifactVersion.step.in_(run_steps))
        elif experiment_ids:
            filters.append(SqlArtifact.experiment_id.in_(experiment_ids))
        else:
            raise ValueError(
                "At least one of `artifact_id`, `run_ids`, or `experiment_ids` must be provided"
            )

        # Apply additional filters
        statuses = statuses or [ArtifactVersionStatus.COMMITTED]
        if statuses:
            filters.append(SqlArtifactVersion.status.in_([s.value for s in statuses]))

        artifact_types = artifact_types or []
        if artifact_types:
            filters.append(
                SqlArtifactVersion.artifact_type.in_((at.value for at in artifact_types))
            )

        # Apply ordering
        if run_ids and len(run_ids) == 1:
            order_by_clauses = [SqlArtifactVersion.step.desc(), SqlArtifactVersion.version.desc()]
        else:
            order_by_clauses = [SqlArtifactVersion.version.desc()]

        with self.ManagedSessionMaker() as session:
            # Create the base query for SqlArtifactVersion
            session_query = session.query(SqlArtifactVersion)

            # Join with SqlArtifact and select only necessary fields
            session_query = session_query.join(
                SqlArtifact, SqlArtifact.id == SqlArtifactVersion.artifact_id
            ).options(
                load_only(SqlArtifact.experiment_id, SqlArtifact.fqn)  # Load only necessary fields
            )

            # Apply the filters to the query
            query = session_query.filter(*filters)

            # Execute the query and fetch paginated results
            instances_paged_list = paginate_query(
                query=query,
                count_field=SqlArtifactVersion.id,
                order_by_clauses=order_by_clauses,
                max_results=max_results,
                page_token=page_token,
            )
            entities_list = [instance.to_entity() for instance in instances_paged_list]
            return PagedList(
                entities_list,
                token=instances_paged_list.token,
                total=instances_paged_list.total,
            )

    def delete_artifact_version(self, version_id: uuid.UUID):
        with self.ManagedSessionMaker() as session:
            instance = (
                session.query(SqlArtifactVersion)
                .filter(
                    SqlArtifactVersion.id == version_id,
                    SqlArtifactVersion.status == ArtifactVersionStatus.HARD_DELETED,
                )
                .one_or_none()
            )
            if not instance:
                raise ValueError(
                    f"No ArtifactVersion with version_id={version_id} status={ArtifactVersionStatus.HARD_DELETED!r} found"
                )
            session.delete(instance)

    def _update_artifact_version(
        self,
        session: Session,
        version_id: uuid.UUID,
        description: Optional[str] = None,
        artifact_metadata: Optional[Dict[str, Union[str, int, float, bool]]] = None,
    ):
        query = session.query(SqlArtifactVersion).filter_by(
            id=version_id, status=ArtifactVersionStatus.COMMITTED.value
        )
        artifact_version = query.one_or_none()

        if not artifact_version:
            raise ValueError(f"Artifact version with ID {version_id} not found")

        if description is not None:
            artifact_version.description = description
        if artifact_metadata is not None:
            artifact_version.artifact_metadata = artifact_metadata

        try:
            self._update_artifact(
                session=session,
                artifact_id=artifact_version.artifact_id,
                updated_at=artifact_version.updated_at,
            )
            session.flush()
        except IntegrityError as e:
            raise ValueError(f"Failed to update artifact version with ID {version_id}") from e

    def update_artifact_version(
        self,
        version_id: uuid.UUID,
        description: Optional[str] = None,
        artifact_metadata: Optional[Dict[str, Union[str, int, float, bool]]] = None,
    ) -> ArtifactVersion:
        with self.ManagedSessionMaker() as session:
            self._update_artifact_version(
                session=session,
                version_id=version_id,
                description=description,
                artifact_metadata=artifact_metadata,
            )

            artifact_version = self._get_artifact_version(
                version_id=version_id, status=ArtifactVersionStatus.COMMITTED
            )

            if not artifact_version:
                raise ValueError(f"Failed to update artifact version with ID {version_id}")

            return artifact_version
