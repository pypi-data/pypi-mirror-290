from __future__ import annotations

import csv
import functools
import logging
import os
import re
from datetime import datetime
from typing import TYPE_CHECKING, Any, BinaryIO

from gql import Client as GQLClient
from gql.transport.requests import RequestsHTTPTransport

from vectice.__version__ import __version__
from vectice.api._auth import Auth
from vectice.api.attachment import AttachmentApi
from vectice.api.columns_description import ColumnsDescriptionApi
from vectice.api.compatibility import CompatibilityApi
from vectice.api.gql_attachment import GqlAttachmentApi
from vectice.api.gql_dataset import GqlDatasetApi
from vectice.api.gql_entity_file import GqlEntityFileApi
from vectice.api.gql_feature_flag import GqlFeatureFlagApi
from vectice.api.gql_metric import GqlMetricApi
from vectice.api.gql_model import GqlModelApi
from vectice.api.gql_organization import GqlOrganizationApi
from vectice.api.gql_property import GqlPropertyApi
from vectice.api.gql_user_workspace_api import UserAndDefaultWorkspaceApi
from vectice.api.http_error_handlers import MissingReferenceError, VecticeException
from vectice.api.iteration import IterationApi
from vectice.api.json import (
    ArtifactName,
    ModelRegisterInput,
    ModelRegisterOutput,
    ModelVersionOutput,
    ModelVersionStatus,
    PagedResponse,
    PropertyInput,
    RequirementOutput,
)
from vectice.api.json.code_version import CodeVersion
from vectice.api.json.dataset_register import DatasetRegisterInput, DatasetRegisterOutput
from vectice.api.json.dataset_representation import DatasetRepresentationOutput
from vectice.api.json.dataset_version import DatasetVersionOutput
from vectice.api.json.dataset_version_representation import DatasetVersionRepresentationOutput
from vectice.api.json.iteration import (
    IterationContextInput,
    IterationStatus,
    IterationUpdateInput,
    RetrieveIterationOutput,
)
from vectice.api.json.metric import MetricInput
from vectice.api.json.model_representation import ModelRepresentationOutput
from vectice.api.json.model_version_representation import ModelVersionRepresentationOutput, ModelVersionUpdateInput
from vectice.api.json.organization_config import OrgConfigOutput
from vectice.api.phase import PhaseApi
from vectice.api.project import ProjectApi
from vectice.api.version import VersionApi
from vectice.api.workspace import WorkspaceApi
from vectice.models.attachment_container import FILE_PATH_DOES_NOT_EXIST_ERROR_MESSAGE
from vectice.models.dataset import Dataset
from vectice.models.iteration import Iteration
from vectice.models.model import Model
from vectice.models.phase import Phase
from vectice.models.representation.dataset_version_representation import DatasetVersionRepresentation
from vectice.models.representation.model_version_representation import ModelVersionRepresentation
from vectice.models.resource.metadata.base import DatasetSourceType, MetadataSettings
from vectice.models.table import Table
from vectice.types.iteration import IterationInput
from vectice.types.phase import PhaseInput
from vectice.types.project import ProjectInput
from vectice.types.version import TVersion
from vectice.utils.vectice_ids_regex import WORKSPACE_VID_REG

if TYPE_CHECKING:
    from io import BytesIO, IOBase

    from requests import Response

    from vectice.api.json import AttachmentOutput, ProjectOutput, WorkspaceOutput
    from vectice.api.json.compatibility import CompatibilityOutput
    from vectice.api.json.iteration import (
        IterationOutput,
        IterationStepArtifact,
        IterationStepArtifactInput,
    )
    from vectice.api.json.phase import PhaseOutput

_logger = logging.getLogger(__name__)


DISABLED_FEATURE_FLAG_MESSAGE = (
    "This '{}' feature is not enabled. Please contact your sales representative for Beta program access."
)


class Client:
    """Low level Vectice API client."""

    _instance: Client | None = None

    def __init__(
        self,
        token: str,
        api_endpoint: str,
    ):
        self.auth = Auth(api_endpoint=api_endpoint, api_token=token)
        transport = RequestsHTTPTransport(url=self.auth.api_base_url + "/graphql", verify=self.auth.verify_certificate)
        logging.getLogger("gql.transport.requests").setLevel("WARNING")
        self._gql_client = GQLClient(transport=transport)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._org_config = self._get_org_config()

    @staticmethod
    def get_instance(
        token: str | None = None,
        api_endpoint: str | None = None,
    ) -> Client:
        if token or api_endpoint:
            Client._instance = None

        if Client._instance is None:
            if token is None or api_endpoint is None:
                raise VecticeException(
                    "You should login before using this method. See https://api-docs.vectice.com/reference/vectice/connection/#vectice.Connection.connect for more info."
                )

            Client._instance = Client(token, api_endpoint)
        return Client._instance

    @property
    def version_api(self) -> str:
        return __version__

    @property
    def version_backend(self) -> str:
        versions = VersionApi(self._gql_client, self.auth).get_public_config().versions
        for version in versions:
            if version.artifact_name == ArtifactName.BACKEND:
                return version.version
        raise ValueError("No version found for backend.")

    def check_compatibility(self) -> CompatibilityOutput:
        return CompatibilityApi(self.auth).check_version()

    def _get_org_config(self) -> OrgConfigOutput:
        return GqlOrganizationApi(self._gql_client, self.auth).get_organization_config()

    def list_projects(
        self,
        workspace: str,
    ) -> PagedResponse[ProjectOutput]:
        """List the projects in a workspace.

        Parameters:
            workspace: The workspace id.

        Returns:
            The workspace's projects.
        """
        return ProjectApi(self._gql_client, self.auth).list_projects(workspace)

    def get_project(self, project: str, workspace: str | None = None) -> ProjectOutput:
        """Get a project.

        Parameters:
            project: The project name or vectice id.
            workspace: The workspace name or id.

        Returns:
            The project JSON structure.
        """
        if workspace is not None and not re.search(WORKSPACE_VID_REG, workspace):
            workspace = WorkspaceApi(self._gql_client, self.auth).get_workspace(workspace).id
        return ProjectApi(self._gql_client, self.auth).get_project(project, workspace)

    def create_project(self, workspace_id: str, project: ProjectInput) -> ProjectOutput:
        return ProjectApi(self._gql_client, self.auth).create_project(workspace_id, project)

    def get_workspace(self, workspace: str) -> WorkspaceOutput:
        """Get a workspace.

        Parameters:
            workspace: The workspace name or id.

        Returns:
            The workspace JSON structure.
        """
        return WorkspaceApi(self._gql_client, self.auth).get_workspace(workspace)

    def list_workspaces(self) -> PagedResponse[WorkspaceOutput]:
        """List the workspaces.

        Returns:
            The workspaces.
        """
        return WorkspaceApi(self._gql_client, self.auth).list_workspaces()

    def upsert_code_attachments(self, files: list[tuple[str, tuple[str, str]]], code_version_id: int):
        """Create an attachment.

        Parameters:
            files: The paths to the files to attach.
            code_version_id: The code version id to attach files to.

        Returns:
            The JSON structure.
        """
        return AttachmentApi(self.auth).create_attachments(files=files, code_version_id=code_version_id)

    def attach_file_to_lineage(self, lineage_id: int, entity_file_id: int):
        """Attach an attachment to an assets lineage.

        Parameters:
            lineage_id: The lineage id to the file to.
            entity_file_id: The file id to attach

        Returns:
            The JSON structure.
        """
        return GqlAttachmentApi(self._gql_client, self.auth).attach_file_to_lineage(
            lineage_id=lineage_id, entity_file_id=entity_file_id
        )

    def upsert_version_attachments(self, files: list[tuple[str, tuple[str, BinaryIO]]], version: TVersion):
        """Create an attachment.

        Parameters:
            files: The paths to the files to attach.
            version: The version to attach files to.

        Returns:
            The JSON structure.
        """
        return AttachmentApi(self.auth).post_attachment(files, version)

    def upsert_version_tables(self, tables: list[Table], version: TVersion):
        """Upsert a table.

        Parameters:
            tables: The tables to attach.
            version: The version to attach tables to.

        Returns:
            The JSON structure.
        """
        return GqlAttachmentApi(self._gql_client, self.auth).upsert(
            version.id,
            (
                "MODEL_VERSION"
                if isinstance(version, (ModelVersionOutput, ModelVersionRepresentationOutput))
                else "DATASET_VERSION"
            ),
            tables,
        )

    def upsert_iteration_attachments(
        self,
        files: list[tuple[str, tuple[str, BytesIO | IOBase]]],
        iteration_id: str,
        step_name: str | None = None,
    ):
        """Create an attachment.

        Parameters:
            files: The paths to the files to attach.
            iteration_id: The iteration id to attach files to.
            step_name (Optional): The step name to add this attachment as an artifact of the step.

        Returns:
            The JSON structure.
        """
        return AttachmentApi(self.auth).create_attachments(files, iteration_id=iteration_id, step_name=step_name)

    def upsert_lineage_attachments(
        self,
        files: list[tuple[str, tuple[str, BytesIO | IOBase]]],
        lineage_id: int,
    ):
        """Create an attachment.

        Parameters:
            files: The paths to the files to attach.
            lineage_id: The lineage id to attach files to.

        Returns:
            The JSON structure.
        """
        return AttachmentApi(self.auth).create_attachments(files, lineage_id=lineage_id)

    def create_model_predictor(self, model_type: str, model_content: BytesIO, model_version: ModelVersionOutput):
        """Create a predictor.

        Parameters:
            model_type: The type of model to attach.
            model_content: The binary content of the model.
            model_version: The model version to attach files to.

        Returns:
            The JSON structure.
        """
        return AttachmentApi(self.auth).post_model_predictor(model_type, model_content, model_version)

    def list_version_representation_attachments(
        self, version: ModelVersionRepresentation | DatasetVersionRepresentation
    ) -> PagedResponse[AttachmentOutput]:
        """List the attachments of an artifact.

        Parameters:
            version: The version to list attachments from.

        Returns:
            The attachments of an artifact.
        """
        return AttachmentApi(self.auth).list_version_representation_attachments(version=version)

    def list_attachments(self, version: ModelVersionOutput | DatasetVersionOutput) -> PagedResponse[AttachmentOutput]:
        """List the attachments of an artifact.

        Parameters:
            version: The version to list attachments from.

        Returns:
            The attachments of an artifact.
        """
        return AttachmentApi(self.auth).list_attachments(version)

    def get_code_version_attachment(self, code_version_id: int, file_id: int) -> Response:
        """Get the attachment of a code version.

        Parameters:
            code_version_id: The code version id to list attachments from.
            file_id: The file id attached to the code version.

        Returns:
            The file attached to the code version.
        """
        return AttachmentApi(self.auth).get_code_version_attachment(code_version_id=code_version_id, file_id=file_id)

    def list_phases(
        self,
        project: str,
    ) -> PagedResponse[PhaseOutput]:
        return PhaseApi(self._gql_client, self.auth).list_phases(project)

    def get_phase(self, phase: str, project_id: str | None = None) -> PhaseOutput:
        if project_id is None:
            raise MissingReferenceError("project")
        return PhaseApi(self._gql_client, self.auth).get_phase(phase, project_id)

    def create_phase(self, project_id: str, phase: PhaseInput) -> PhaseOutput:
        return PhaseApi(self._gql_client, self.auth).create_phase(project_id, phase)

    def get_full_phase(self, phase: str) -> PhaseOutput:
        return PhaseApi(self._gql_client, self.auth).get_phase(phase=phase, full=True)

    def list_sections(self, iteration_id: str) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).list_sections(iteration_id)

    def list_iterations(
        self, phase: str, only_mine: bool = False, statuses: list[IterationStatus] | None = None
    ) -> PagedResponse[IterationOutput]:
        return IterationApi(self._gql_client, self.auth).list_iterations(phase, only_mine, statuses)

    def list_step_definitions(self, phase: str) -> PagedResponse[RequirementOutput]:
        return PhaseApi(self._gql_client, self.auth).list_step_definitions(phase)

    def get_last_iteration(self, phase_id: str, iteration: IterationInput | None = None) -> RetrieveIterationOutput:
        return IterationApi(self._gql_client, self.auth).get_last_iteration(phase_id, iteration)

    def get_active_iteration_or_create(self, phase_id: str) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).get_active_iteration_or_create(phase_id)

    def get_iteration_by_id(self, iteration_id: str, full: bool = False) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).get_iteration_by_id(iteration_id, full)

    def get_iteration_by_index(self, phase_id: str, index: int) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).get_iteration_by_index(phase_id, index)

    def create_iteration(self, phase_id: str, iteration: IterationInput | None = None) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).create_iteration(phase_id, iteration)

    def update_iteration(self, iteration_id: str, iteration: IterationUpdateInput) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).update_iteration(iteration, iteration_id)

    def delete_iteration(self, iteration_id: str) -> None:
        IterationApi(self._gql_client, self.auth).delete_iteration(iteration_id)

    def add_iteration_artifacts(
        self, iteration_id: str, artifacts: list[IterationStepArtifactInput], section: str | None = None
    ) -> list[IterationStepArtifact]:
        iteration_context = IterationContextInput(iterationId=iteration_id, stepName=section)
        return IterationApi(self._gql_client, self.auth).add_iteration_artifacts(
            artifacts=artifacts, iteration_context=iteration_context
        )

    def remove_iteration_assets(self, iteration_id: str, section: str | None = None, all: bool = False):
        iteration_context = IterationContextInput(iterationId=iteration_id, stepName=section)
        return IterationApi(self._gql_client, self.auth).remove_iteration_assets(
            iteration_context=iteration_context, all=all
        )

    def register_dataset_from_source(
        self,
        dataset: Dataset,
        iteration_id: str,
        code_version: CodeVersion | None = None,
        section: str | None = None,
    ) -> DatasetRegisterOutput:
        if dataset._has_snowflake_resource:  # pyright: ignore[reportPrivateUsage]
            self.assert_feature_flag_or_raise("snowflake-resource")

        if dataset._has_spark_resource:  # pyright: ignore[reportPrivateUsage]
            self.assert_feature_flag_or_raise("spark-table-resource")

        name = self.get_dataset_name(dataset)
        derived_from = self.get_derived_from(dataset)
        metadata_asdict, is_updating_columns = self._transform_resource_to_metadata_dict(dataset)
        properties, _ = self.get_properties_and_metrics(dataset)

        dataset_register_input = DatasetRegisterInput(
            name=name,
            type=dataset.type.value,
            datasetSources=metadata_asdict,
            inputs=derived_from,
            codeVersion=code_version.asdict() if code_version is not None else None,
            properties=properties,
        )

        iteration_context = IterationContextInput(iterationId=iteration_id, stepName=section)
        dataset_register_output = self.register_dataset(dataset_register_input, iteration_context=iteration_context)
        dtv_id = dataset_register_output["datasetVersion"]["vecticeId"]

        if is_updating_columns:
            self.warn_if_dataset_version_columns_are_missing_description(dtv_id)

        dataset.latest_version_id = dtv_id
        return dataset_register_output

    def warn_if_dataset_version_columns_are_missing_description(self, dataset_version_id: str):
        has_columns_without_description = GqlDatasetApi(
            self._gql_client, self.auth
        ).get_dataset_version_has_columns_without_description(dataset_version_id)
        if has_columns_without_description is True:
            _logger.warning(
                "Some column descriptions are missing. Consider adding descriptions for improved data clarity."
            )

    def get_dataset(self, id: str) -> DatasetRepresentationOutput:
        return GqlDatasetApi(self._gql_client, self.auth).get_dataset(id)

    def get_dataset_version(self, id: str) -> DatasetVersionRepresentationOutput:
        return GqlDatasetApi(self._gql_client, self.auth).get_dataset_version(id)

    def update_dataset_version(self, id: str, columns_description: list[dict[str, str]]):
        return GqlDatasetApi(self._gql_client, self.auth).update_dataset_version(id, columns_description)

    def update_columns_description_via_csv(self, id: str, file_path: str):
        if not os.path.exists(file_path):
            raise ValueError(FILE_PATH_DOES_NOT_EXIST_ERROR_MESSAGE % file_path)
        curr_file = ("file", (file_path, open(file_path, "rb")))
        ColumnsDescriptionApi(self.auth).post_columns_description(id, curr_file)
        curr_file[1][1].close()

    def get_model(self, id: str) -> ModelRepresentationOutput:
        return GqlModelApi(self._gql_client, self.auth).get_model(id)

    def get_dataset_version_list(self, id: str, size: int) -> PagedResponse[DatasetVersionRepresentationOutput]:
        return GqlDatasetApi(self._gql_client, self.auth).get_dataset_version_list(id, size)

    def get_model_version_list(self, id: str, size: int) -> PagedResponse[ModelVersionRepresentationOutput]:
        return GqlModelApi(self._gql_client, self.auth).get_model_version_list(id, size)

    def get_model_version(self, id: str) -> ModelVersionRepresentationOutput:
        return GqlModelApi(self._gql_client, self.auth).get_model_version(id)

    def update_model(self, model_version_id: str, model: ModelVersionUpdateInput):
        GqlModelApi(self._gql_client, self.auth).update_model(model_version_id, model)

    @staticmethod
    def get_dataset_name(dataset: Dataset) -> str:
        return (
            f"dataset {datetime.time}"
            if dataset.name is None  # pyright: ignore[reportUnnecessaryComparison]
            else dataset.name
        )

    @staticmethod
    def get_derived_from(obj: Dataset | Model) -> list[str]:
        return [] if obj.derived_from is None else obj.derived_from  # pyright: ignore[reportUnnecessaryComparison]

    @staticmethod
    def get_properties_and_metrics(
        obj: Dataset | Model,
    ) -> tuple[list[dict[str, Any]] | None, list[dict[str, Any]] | None]:
        properties = [vars(PropertyInput(prop.key, prop.value)) for prop in obj.properties] if obj.properties else None
        metrics = (
            [vars(MetricInput(met.key, met.value)) for met in obj.metrics]
            if (isinstance(obj, Model) and obj.metrics)
            else None
        )
        return properties, metrics

    def _transform_resource_to_metadata_dict(self, dataset: Dataset):
        resources = dataset.resource if isinstance(dataset.resource, tuple) else [dataset.resource]
        metadata_asdict = []
        is_updating_columns = False
        for resource in resources:
            if resource is not None and resource.metadata:
                resource.metadata.set_settings(
                    MetadataSettings(
                        minimum_rows_for_statistics=self._org_config.configuration.df_statistics_row_threshold,
                        sample_rows_for_statistics=self._org_config.configuration.df_statistics_row_sample,
                        maximum_columns_for_statistics=self._org_config.configuration.df_statistics_colmns_threshold,
                    )
                )

                metadata, columns_description = resource.metadata, resource.columns_description
                is_updating_columns = is_updating_columns is False and columns_description is not None
                columns = columns_description or {}
                metadata_dict, type = metadata.asdict(), metadata.type
                if type == DatasetSourceType.DB:
                    for db in metadata_dict["dbs"]:
                        db["columns"] = self._combine_source_column_description(db, columns)
                else:
                    for file in metadata_dict["files"]:
                        file["columns"] = self._combine_source_column_description(file, columns)

                metadata_asdict.append(metadata_dict)
        return metadata_asdict, is_updating_columns

    def _combine_source_column_description(self, source: dict, columns_description: dict[str, str] | str):
        def _transform_path_to_dictionary(path: str):
            def _reduce_csv(acc: dict[str, str], curr: list[str]):
                if len(curr) > 1:
                    return {**acc, curr[0]: curr[1]}
                return acc

            with open(path, mode="r", newline="") as csv_file:
                return functools.reduce(_reduce_csv, csv.reader(csv_file), {})

        if isinstance(columns_description, str):
            columns_description = _transform_path_to_dictionary(columns_description)

        def _map_columns(col: dict):
            col_name = col["name"]
            if col_name in columns_description:
                column_desc = columns_description[col_name]
                return {**col, "description": column_desc}
            return col

        return list(map(_map_columns, source["columns"]))

    def register_dataset(
        self,
        dataset_register_input: DatasetRegisterInput,
        iteration_context: IterationContextInput,
    ) -> DatasetRegisterOutput:
        data: DatasetRegisterOutput = GqlDatasetApi(self._gql_client, self.auth).register_dataset(
            dataset_register_input, iteration_context
        )
        _logger.debug(
            f"Successfully registered Dataset("
            f"name='{dataset_register_input.name}', "
            f"id={data['datasetVersion']['vecticeId']}, "
            f"version='{data['datasetVersion']['name']}', "
            f"type={dataset_register_input.type})."
        )
        return data

    def register_model(
        self,
        model: Model,
        iteration: Iteration,
        phase: Phase,
        code_version: CodeVersion | None = None,
        section: str | None = None,
    ) -> ModelRegisterOutput:
        """Register a model.

        Parameters:
            model: The model to register
            iteration: The iteration
            phase: The phase
            code_version_id: The code version ID
            section: The section

        Returns:
            The registered model.
        """
        properties, metrics = self.get_properties_and_metrics(model)
        derived_from = self.get_derived_from(model)
        model.name = (model.name or f"{phase.name} {iteration.index} model")[:60]
        model_register_input = ModelRegisterInput(
            name=model.name,
            modelType="OTHER",
            status=ModelVersionStatus.EXPERIMENTATION.value,
            inputs=derived_from,
            metrics=metrics,
            properties=properties,
            algorithmName=model.technique,
            framework=model.library,
            codeVersion=code_version.asdict() if code_version is not None else None,
            context=model.additional_info.asdict() if model.additional_info is not None else None,
        )
        iteration_context = IterationContextInput(iterationId=iteration.id, stepName=section)

        model_output = GqlModelApi(self._gql_client, self.auth).register_model(
            model_register_input, iteration_context=iteration_context
        )
        model.latest_version_id = model_output["modelVersion"]["vecticeId"]
        return model_output

    def upsert_properties(self, type: str, id: str, properties: list[dict[str, str | int]]):
        return GqlPropertyApi(self._gql_client, self.auth).upsert(type, id, properties)

    def upsert_metrics(self, type: str, id: str, metrics: list[dict[str, str | float | int]]):
        return GqlMetricApi(self._gql_client, self.auth).upsert(type, id, metrics)

    def get_user_and_default_workspace(self):
        return UserAndDefaultWorkspaceApi(self._gql_client, self.auth).get_user_and_default_workspace()

    def get_entity_file_by_id(self, id: int):
        return GqlEntityFileApi(self._gql_client, self.auth).get_entity_file_by_id(id)

    def assert_feature_flag_or_raise(self, code: str) -> None:
        enabled = self.is_feature_flag_enabled(code)
        if enabled is False:
            raise VecticeException(DISABLED_FEATURE_FLAG_MESSAGE.format(code))

    def is_feature_flag_enabled(self, code: str) -> bool:
        enabled = GqlFeatureFlagApi(self._gql_client, self.auth).is_feature_flag_enabled(code)
        if enabled is False:
            _logger.info(DISABLED_FEATURE_FLAG_MESSAGE.format(code))
        return enabled
