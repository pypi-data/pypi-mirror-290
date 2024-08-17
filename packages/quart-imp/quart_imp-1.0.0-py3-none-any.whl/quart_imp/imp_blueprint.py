import typing as t
from importlib import import_module
from importlib.util import find_spec
from inspect import getmembers
from pathlib import Path

from quart import Blueprint

from .config import ImpBlueprintConfig
from .exceptions import NoConfigProvided
from .utilities import (
    cast_to_import_str,
    slug,
)

ArgT = t.TypeVar("ArgT")
ReturnT = t.TypeVar("ReturnT")


class ImpBlueprint(Blueprint):
    """
    A Class that extends the capabilities of the Quart Blueprint class.
    """

    config: ImpBlueprintConfig

    location: Path
    bp_name: str
    package: str

    models: t.Set[t.Any]
    nested_blueprints: t.Set[t.Union["ImpBlueprint", Blueprint]]

    def __init__(self, dunder_name: str, config: ImpBlueprintConfig) -> None:
        """
        Initializes the ImpBlueprint.

        :param dunder_name: __name__
        :param config: The blueprint's config.
        """

        self.models = set()
        self.nested_blueprints = set()

        self.package = dunder_name

        spec = find_spec(self.package)
        if spec is None:
            raise ImportError(f"Cannot find origin of {self.package}")

        self.location = Path(f"{spec.origin}").parent
        self.bp_name = self.location.name

        if config is None:
            raise NoConfigProvided(f"No config was provided for {self.location}")

        self.config = config

        if not self.config.url_prefix:
            self.config.url_prefix = f"/{slug(self.bp_name)}"

        super().__init__(
            self.bp_name, self.package, **self.config.quart_blueprint_args()
        )

    def _prevent_if_disabled(self: "ImpBlueprint") -> bool:
        if not self.config.enabled:
            return True
        return False

    def as_quart_blueprint(self) -> Blueprint:
        """
        Returns the blueprint as a Quart Blueprint.

        :return: Blueprint
        """
        return self

    def import_resources(self, folder: str = "routes") -> None:
        """
        Will import all the resources (cli, routes, filters, context_processors...) from the given folder.
        Given folder must be relative to the blueprint (in the same folder as the __init__.py file).

        :param folder: Folder to look for resources in. Defaults to "routes". Must be relative.
        :return: None
        """

        if self._prevent_if_disabled():
            return

        resource_path = self.location / folder
        if not resource_path.exists():
            raise NotADirectoryError(f"{resource_path} is not a directory")

        resources = resource_path.glob("*.py")
        for resource in resources:
            try:
                import_module(f"{self.package}.{folder}.{resource.stem}")
            except ImportError as e:
                raise ImportError(
                    f"Error when importing {self.package}.{resource}: {e}"
                )

    def import_nested_blueprint(self, blueprint: t.Union[str, Path]) -> None:
        """
        Imports the specified Quart-Imp Blueprint or a standard Quart Blueprint as a nested blueprint,
        under the current blueprint.

        :param blueprint: The blueprint (folder name) to import. Must be relative.
        :return: None
        """

        if self._prevent_if_disabled():
            return

        if isinstance(blueprint, Path):
            potential_bp = blueprint
        else:
            if isinstance(blueprint, str):
                if Path(blueprint).is_absolute():
                    potential_bp = Path(blueprint)
                else:
                    potential_bp = Path(self.location / blueprint)
            else:
                raise ValueError("Blueprint must be a string or a Path object")

        if potential_bp.exists() and potential_bp.is_dir():
            module = import_module(
                cast_to_import_str(self.package.split(".")[0], potential_bp)
            )
            for name, potential in getmembers(module):
                if isinstance(potential, ImpBlueprint):
                    self.nested_blueprints.add(potential)
                    continue

                if isinstance(potential, Blueprint):
                    self.nested_blueprints.add(potential)

    def import_nested_blueprints(self, folder: str) -> None:
        """
        Imports all blueprints in the given folder.

        :param folder: Folder to look for nested blueprints in.
        :return: None
        """

        if self._prevent_if_disabled():
            return

        folder_path = Path(self.location / folder)

        if not folder_path.exists() or not folder_path.is_dir():
            raise NotADirectoryError(f"{folder_path} is not a directory")

        for potential_bp in folder_path.iterdir():
            self.import_nested_blueprint(blueprint=potential_bp)

    def tmpl(self, template: str) -> str:
        """
        Pushes the blueprint name to the template name.
        This saves time in having to type out the blueprint name when rendering a
        template file from the blueprint's template folder.

        :param template: The template name to push the blueprint name to.
        :return: str - The template name with the blueprint name pushed to it.
        """
        return f"{self.name}/{template}"
