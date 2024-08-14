"""SDK Dashboard Web Component Dependency."""

from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Tuple

from engineai.sdk.dashboard.base import DependencyInterface
from engineai.sdk.dashboard.dependencies.exceptions import WebComponentMinimumPathError


class WebComponentDependency(DependencyInterface):
    """Web Component Dependency."""

    _INPUT_KEY = "webComponent"

    def __init__(self, path: List[str]):
        """Constructor for WebComponentDependency Class.

        Args:
            path: path to the web component. Represents the path to the data injected
                by the web component.
        """
        if len(path) < 2:
            raise WebComponentMinimumPathError()
        self.__field = path.pop(-1)
        self.__path = path
        self.__dependency_id = f"web_component_{'_'.join(path)}"

    def __str__(self) -> str:
        return f"{{{{{self.dependency_id}.{self.__field}}}}}"

    def __iter__(self) -> Generator[Tuple[str, str], None, None]:
        yield "dependency_id", self.__dependency_id

    def __hash__(self) -> int:
        return hash(self.__dependency_id)

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, type(self))
            and self.__dependency_id == other.dependency_id
        )

    @property
    def dependency_id(self) -> str:
        """Returns dependency id."""
        return self.__dependency_id

    @property
    def field(self) -> str:
        """Returns field."""
        return self.__field

    def build_item(self) -> Dict[str, Any]:
        """Build item."""
        return {
            "name": self.__dependency_id,
            "path": ".".join(self.__path),
        }

    def build(self) -> Dict[str, Any]:
        """Method to build specs."""
        return self.build_item()
