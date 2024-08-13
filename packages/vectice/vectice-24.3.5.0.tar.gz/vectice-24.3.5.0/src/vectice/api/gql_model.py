from __future__ import annotations

from typing import TYPE_CHECKING, Any

from gql import gql
from gql.transport.exceptions import TransportQueryError

from vectice.api.gql_api import GqlApi, Parser
from vectice.api.json.model_representation import ModelRepresentationOutput
from vectice.api.json.model_version_representation import ModelVersionRepresentationOutput, ModelVersionUpdateInput
from vectice.api.json.paged_response import PagedResponse
from vectice.utils.api_utils import PAGINATE_OUTPUT, get_page_input

if TYPE_CHECKING:
    from vectice.api.json.iteration import IterationContextInput
    from vectice.api.json.model_register import ModelRegisterInput, ModelRegisterOutput

_RETURNS = """
            modelVersion {
                vecticeId
                name
                version
                description
                algorithmName
                framework
                modelId
                model {
                    name
                    projectId
                }
                origin {
                   id
                  }
            }
            useExistingModel
            __typename
            """

_RETURNS_MODEL = """
            vecticeId
            createdDate
            updatedDate
            name
            description
            type
            versionCount
            versionStats {
                experimentationCount
                productionCount
                stagingCount
                retiredCount
            }
            lastVersion {
                vecticeId
                createdDate
                updatedDate
                name
                description
                status
                algorithmName
                framework
                __typename
            }
            project {
                vecticeId
            }
            __typename
"""

_BASE_MODEL_VERSION = """
            vecticeId
            name
            isStarred
            description
            status
            algorithmName
            framework
            properties {
                key
                value
            }
            metrics {
                key
                value
            }
            __typename
"""
_RETURNS_MODEL_VERSION = f"""
            {_BASE_MODEL_VERSION}
            model {{
                name
                project {{
                    vecticeId
                }}
                vecticeId
                type
                description
                versionCount
                versionStats {{
                    experimentationCount
                    productionCount
                    stagingCount
                    retiredCount
                }}
                lastVersion {{
                    vecticeId
                    __typename
                }}
            }}
"""

_RETURNS_MODEL_UPDATE = """
            vecticeId
            __typename
"""
_RETURNS_PAGINATED_VERSION_LIST = PAGINATE_OUTPUT.format(_BASE_MODEL_VERSION)


class GqlModelApi(GqlApi):
    def get_model(self, id: str) -> ModelRepresentationOutput:
        variable_types = "$modelId:VecticeId!"
        kw = "modelId:$modelId"
        variables = {"modelId": id}
        query = GqlApi.build_query(
            gql_query="getModelById",
            variable_types=variable_types,
            returns=_RETURNS_MODEL,
            keyword_arguments=kw,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            model_output: ModelRepresentationOutput = Parser().parse_item(response["getModelById"])
            return model_output
        except TransportQueryError as e:
            self._error_handler.handle_post_gql_error(e, "model", id)

    def get_model_version_list(self, id: str, size: int) -> PagedResponse[ModelVersionRepresentationOutput]:
        gql_query = "getModelVersionsList"
        variable_types = "$modelId:VecticeId!,$page:PageInput"
        kw = "modelId:$modelId,page:$page"
        variables = {
            "modelId": id,
            "page": get_page_input(size=size),
        }
        query = GqlApi.build_query(
            gql_query=gql_query,
            variable_types=variable_types,
            returns=_RETURNS_PAGINATED_VERSION_LIST,
            keyword_arguments=kw,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            model_output: PagedResponse[ModelVersionRepresentationOutput] = Parser().parse_paged_response(
                response[gql_query]
            )
            return model_output
        except TransportQueryError as e:
            self._error_handler.handle_post_gql_error(e, "model_version", id)

    def get_model_version(self, id: str) -> ModelVersionRepresentationOutput:
        variable_types = "$modelVersionId:VecticeId!"
        kw = "modelVersionId:$modelVersionId"
        variables = {"modelVersionId": id}
        query = GqlApi.build_query(
            gql_query="getModelVersion",
            variable_types=variable_types,
            returns=_RETURNS_MODEL_VERSION,
            keyword_arguments=kw,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            model_output: ModelVersionRepresentationOutput = Parser().parse_item(response["getModelVersion"])
            return model_output
        except TransportQueryError as e:
            self._error_handler.handle_post_gql_error(e, "model_version", id)

    def register_model(
        self,
        data: ModelRegisterInput,
        iteration_context: IterationContextInput,
    ) -> ModelRegisterOutput:
        variables: dict[str, Any] = {"iterationContext": iteration_context, "data": data}
        kw = "iterationContext:$iterationContext,data:$data"
        variable_types = "$iterationContext:IterationContextInput!,$data:ModelRegisterInput!"

        query_name = "registerModel"
        query = GqlApi.build_query(
            gql_query=query_name,
            variable_types=variable_types,
            returns=_RETURNS,
            keyword_arguments=kw,
            query=False,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            model_output: ModelRegisterOutput = Parser().parse_item(response[query_name])
            return model_output
        except TransportQueryError as e:
            self._error_handler.handle_post_gql_error(e, "model", "register model")

    def update_model(self, model_version_id: str, model: ModelVersionUpdateInput):
        variable_types = "$modelVersionId:VecticeId!,$data:ModelVersionUpdateInput!"
        kw = "modelVersionId:$modelVersionId,data:$data"
        variables = {"modelVersionId": model_version_id, "data": model}
        query = GqlApi.build_query(
            gql_query="updateModelVersion",
            variable_types=variable_types,
            returns=_RETURNS_MODEL_UPDATE,
            keyword_arguments=kw,
            query=False,
        )
        query_built = gql(query)
        try:
            self.execute(query_built, variables)
        except TransportQueryError as e:
            self._error_handler.handle_post_gql_error(e, "model", "put")
