import sys
from typing import List, Optional, Type
import importlib.metadata

from .plugin import Plugin
from .composite import Composite
from .masterpiece import MasterPiece


class PlugMaster(MasterPiece):
    """
    The `Plugmaster` class is responsible for managing and loading plugins into an application.

    The `Plugmaster` is designed to work with plugins that are `Masterpiece` objects or subclasses thereof.
    Plugins can optionally be derived from  the `Plugin` class.

    If a plugin implements the `Plugin` interface, it is responsible for determining what objects should be added to the application.

    If a plugin is not a `Plugin` class, it is simply loaded, and it is the responsibility
    of the application configuration file or the application code to determine how to utilize the plugin.


    """

    def __init__(self, name: str) -> None:
        """Instantiates and initializes the Plugmaster for the given application name. This
        name refers to the list of plugins, as defined in the application 'pyproject.toml'.
        For more information on 'pyproject.toml' consult the Python documentation.

        Args:
            name (str): Name determining the plugins to be loaded.
        """
        super().__init__(name)
        self.plugins: List[Type[MasterPiece]] = []

    def load(self) -> None:
        """Fetch the entry points associated with the 'name', call their 'load()' methods
        and insert to the list of plugins.
        Note: Python's 'importlib.metadata' API has been redesigned
        a couple of times in the past. The current implementation has been tested with Python 3.8, 3.9
        and 3.12.
        """

        # TODO: fix Code is unreachablePylance, Instance of 'EntryPoints' has no 'get' memberPylintE1101:no-member false positive.

        if sys.version_info >= (3, 10):
            entry_points = importlib.metadata.entry_points().select(
                group=f"{self.name}.plugins"
            )
        elif sys.version_info >= (3, 9):
            entry_points = importlib.metadata.entry_points().get(
                f"{self.name}.plugins", []
            )
        else:
            # For Python 3.8 and below
            entry_points = importlib.metadata.entry_points()[f"{self.name}.plugins"]

        for entry_point in entry_points:
            entry = entry_point.load()
            print(f"Plugin {entry.__class__}:{entry.__name__} added")
            self.plugins.append(entry)

    def install(self, app: Composite) -> None:
        """Add the plugin instances implementing 'Plugin' interface into the application.
        Plugins that don't implement the 'Plugin' interface are skipped, it is up to the
        application or the configuration files in it to instantiate and add them to the
        application.

        Args:
            app (Composite) : parent object (application), for hosting the instances created by the plugin.

        """
        for entry in self.plugins:
            obj = entry()
            if isinstance(obj, Plugin):
                plugin: Plugin = obj
                plugin.install(app)
                self.info(f"Plugin {obj.name}:{str(type(plugin))} installed")
            elif isinstance(obj, MasterPiece):
                plugin.install(app)
                self.info(f"Plugin {obj.name}:{str(type(plugin))} installed")
            else:
                self.error(f"{type(obj)} is not a MasterPiece, skipped")

    def get(self) -> List[Type[MasterPiece]]:
        """Fetch the list of plugins classes.

        Returns:
            List[Type[MasterPiece]]: List of plugins
        """
        return self.plugins
