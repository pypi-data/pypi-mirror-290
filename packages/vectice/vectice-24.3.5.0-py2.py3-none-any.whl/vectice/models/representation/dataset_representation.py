from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List

from vectice.api.json.dataset_representation import DatasetRepresentationOutput
from vectice.utils.common_utils import (
    convert_keys_to_snake_case,
    flatten_dict,
    flatten_resources,
    process_versions_list_metrics_and_properties,
    remove_type_name,
    repr_class,
)
from vectice.utils.dataframe_utils import repr_list_as_pd_dataframe

if TYPE_CHECKING:
    from pandas import DataFrame

    from vectice.api.client import Client

_logger = logging.getLogger(__name__)


class DatasetRepresentation:
    """Represents the metadata of a Vectice dataset.

    A Dataset Representation shows information about a specific dataset from the Vectice app. It makes it easier to get and read this information through the API.

    NOTE: **Hint**
        A dataset ID starts with 'DTS-XXX'. Retrieve the ID in the Vectice App, then use the ID with the following methods to get the dataset:
        ```connect.dataset('DTS-XXX')``` or ```connect.browse('DTS-XXX')```
        (see [Connection page](https://api-docs.vectice.com/reference/vectice/connection/#vectice.Connection.dataset)).

    Attributes:
        id (str): The unique identifier of the dataset.
        project_id (str): The identifier of the project to which the dataset belongs.
        name (str): The name of the dataset.
        description (str): The description of the dataset.
        type (str): The type of the dataset.
        origin (str): The source origin of the dataset.
        total_number_of_versions (int): The total number of versions belonging to this dataset.
    """

    def __init__(
        self,
        output: DatasetRepresentationOutput,
        client: "Client",
    ):
        self.id = output.id
        self.project_id = output.project_id
        self.name = output.name
        self.type = output.type
        self.origin = output.origin
        self.description = output.description
        self.total_number_of_versions = output.total_number_of_versions
        self._last_version = output.version
        self._client = client

    def __repr__(self):
        return repr_class(self)

    def _asdict(self):
        return self.asdict()

    def asdict(self) -> Dict[str, Any]:
        """Transform the DatasetRepresentation into a organised dictionary.

        Returns:
            The object represented as a dictionary
        """
        return {
            "id": self.id,
            "name": self.name,
            "project_id": self.project_id,
            "description": self.description,
            "type": self.type,
            "origin": self.origin,
            "total_number_of_versions": self.total_number_of_versions,
        }

    def versions_list(
        self, number_of_versions: int = 30, as_dataframe: bool = True
    ) -> List[Dict[str, Any]] | DataFrame:
        """Retrieve the dataset versions list linked to the dataset. (Maximum of 100 versions).

        Parameters:
            number_of_versions (int): The number of versions to retrieve. Defaults to 30.
            as_dataframe (bool): If set to True, return type will be a pandas DataFrame for easier manipulation (requires pandas to be installed).
                                 If set to False, returns all dataset versions as a list of dictionaries.

        Returns:
            The dataset versions list as either a list of dictionaries or a pandas DataFrame.
        """
        if number_of_versions > 100:
            _logger.warning(
                "Only the first 100 versions will be retrieved. For additional versions, please contact your sales representative or email support@vectice.com"
            )
            number_of_versions = 100

        version_list = self._client.get_dataset_version_list(self.id, number_of_versions).list
        for version in version_list:
            version["datasetSources"] = flatten_resources(version.resources)
        clean_version_list = remove_type_name(version_list)
        converted_version_list = [convert_keys_to_snake_case(versions) for versions in clean_version_list]
        processed_version_list = process_versions_list_metrics_and_properties(converted_version_list)

        if not as_dataframe:
            return processed_version_list

        for versions in processed_version_list:
            versions.update(flatten_dict(versions))
            del versions["dataset_sources"]
            versions["all_properties_dict"] = versions["properties"]
            del versions["properties"]
        try:
            return repr_list_as_pd_dataframe(processed_version_list)
        except ModuleNotFoundError:
            _logger.info(
                "To display the list of versions as a DataFrame, pandas must be installed. Your list of versions will be in the format of a list of dictionaries."
            )
            return processed_version_list
