from __future__ import annotations

import logging
from textwrap import dedent
from typing import TYPE_CHECKING, ClassVar

from rich.table import Table

from vectice.models.phase import Phase
from vectice.utils.common_utils import temp_print
from vectice.utils.logging_utils import get_phase_status

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.models import Workspace


_logger = logging.getLogger(__name__)


class Project:
    """Represent a Vectice project.

    A project reflects a typical Data Science project, including
    phases and the associated assets like code, datasets, models, and
    documentation. Multiple projects may be defined within each workspace.

    You can get a project from your [`Workspace`][vectice.models.Workspace]
    object by calling `project()`:

    ```python
    import vectice

    connect = vectice.connect(...)
    workspace = connect.workspace("Iris workspace")
    project = workspace.project("Iris project")
    ```

    Or you can get it directly when connecting to Vectice:

    ```python
    import vectice

    project = vectice.connect(..., workspace="Iris workspace", project="Iris project")
    ```

    See [`Connection.connect`][vectice.Connection.connect] to learn
    how to connect to Vectice.
    """

    __slots__: ClassVar[list[str]] = ["_id", "_workspace", "_name", "_description", "_phase", "_client", "_pointers"]

    def __init__(
        self,
        id: str,
        workspace: Workspace,
        name: str,
        description: str | None = None,
    ):
        self._id = id
        self._workspace = workspace
        self._name = name
        self._description = description
        self._phase: Phase | None = None
        self._client = workspace._client  # pyright: ignore[reportPrivateUsage]

    def __repr__(self):
        description = self._description if self._description else "None"
        return f"Project(name={self.name!r}, id={self._id}, description={description!r}, workspace={self._workspace!r})"

    def __eq__(self, other: object):
        if not isinstance(other, Project):
            return NotImplemented
        return self.id == other.id

    @property
    def id(self) -> str:
        """The project's id.

        Returns:
            The project's id.
        """
        return self._id

    @property
    def workspace(self) -> Workspace:
        """The workspace to which this project belongs.

        Returns:
            The workspace to which this project belongs.
        """
        return self._workspace

    @property
    def connection(self) -> Connection:
        """The Connection to which this project belongs.

        Returns:
            The Connection to which this project belongs.
        """
        return self._workspace.connection

    @property
    def name(self) -> str:
        """The project's name.

        Returns:
            The project's name.
        """
        return self._name

    @property
    def description(self) -> str | None:
        """The project's description.

        Returns:
            The project's description.
        """
        return self._description

    @property
    def properties(self) -> dict:
        """The project's identifiers.

        Returns:
            A dictionary containing the `name`, `id` and `workspace` items.
        """
        return {"name": self.name, "id": self.id, "workspace": self.workspace.id}

    def phase(self, phase: str) -> Phase:
        """Get a phase.

        Parameters:
            phase: The name or id of the phase to get.

        Returns:
            The specified phase.
        """
        item = self._client.get_phase(phase, project_id=self._id)
        phase_object = Phase(item, self, self._client)
        logging_output = dedent(
            f"""
                        Phase {item.name!r} successfully retrieved.

                        For quick access to the Phase in the Vectice web app, visit:
                        {self._client.auth.api_base_url}/browse/phase/{phase_object.id}"""
        ).lstrip()
        _logger.info(logging_output)

        self._phase = phase_object
        return phase_object

    def create_phase(self, name: str, description: str | None = None) -> Phase:
        """Creates a phase.

        Parameters:
            name: The phase's name.
            description: The phase's description.

        Returns:
            The newly created phase.
        """
        self._client.assert_feature_flag_or_raise("create-phase-from-the-api")

        item = self._client.create_phase(
            self.id,
            {"name": name, "description": description},
        )
        logging_output = dedent(
            f"""
                Phase {item.name!r} successfully created.
                For quick access to the Phase in the Vectice web app, visit:
                {self._client.auth.api_base_url}/browse/phase/{item.id}"""
        ).lstrip()
        _logger.info(logging_output)
        phase_object = Phase(item, self, self._client)
        return phase_object

    def list_phases(self) -> None:
        """Prints a list of phases belonging to the project in a tabular format, limited to the first 10 items. A link is provided to view the remaining phases.

        Returns:
            None
        """
        phase_outputs = self._client.list_phases(project=self.id)
        rich_table = Table(expand=True, show_edge=False)

        rich_table.add_column("Phase id", justify="left", no_wrap=True, min_width=3, max_width=5)
        rich_table.add_column("Name", justify="left", no_wrap=True, min_width=5, max_width=10)
        rich_table.add_column("Owner", justify="left", no_wrap=True, min_width=4, max_width=4)
        rich_table.add_column("Status", justify="left", no_wrap=True, min_width=4, max_width=4)
        rich_table.add_column("Iterations", justify="left", no_wrap=True, min_width=4, max_width=4)

        for phase in phase_outputs.list:
            phase_owner = phase["owner"]["name"] if phase.get("owner") else "Unassigned"
            phase_status = get_phase_status(phase.status)
            rich_table.add_row(
                phase.id,
                phase.name,
                phase_owner,
                phase_status,
                f"{phase.active_iterations_count}/{phase.iterations_count}",
            )
        description = f"""There are {phase_outputs.total} phases in the project {self.name!r} and a maximum of 10 phases are displayed in the table below:"""
        tips = dedent(
            """
        To access a specific phase, use \033[1mproject\033[0m.phase(Phase ID)"""
        ).lstrip()
        link = dedent(
            f"""
        For quick access to the list of phases for this project, visit:
        {self._client.auth.api_base_url}/browse/project/{self.id}"""
        ).lstrip()

        temp_print(description)
        temp_print(table=rich_table)
        temp_print(tips)
        temp_print(link)
