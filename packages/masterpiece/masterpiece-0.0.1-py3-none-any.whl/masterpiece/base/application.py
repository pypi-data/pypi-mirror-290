import argparse
from typing import List, Type

from .plugmaster import PlugMaster
from .composite import Composite
from .masterpiece import MasterPiece


class Application(Composite):
    """Masterpiece application. Implements startup argument parsing,
    plugin management and initialization of class attributes through
    class specific JSON configuration files."""

    plugins: List[Type[MasterPiece]] = []
    serialization_file: str = ""
    _plugmaster: PlugMaster

    def __init__(self, name: str) -> None:
        """Instantiates and initializes. By default, the application log
        filename is set to the same as the application name.

        Args:
            name (str): The name of the application, determining the default log filename.
        """
        super().__init__(name)

    @classmethod
    def load_class_attributes(cls) -> None:
        MasterPiece.parse_initial_args()
        for name, ctor in MasterPiece.get_registered_classes().items():
            ctor.load_from_json()

    @classmethod
    def load_plugins(cls) -> None:
        """Loads and initializes all plugins for instantiation. This method
        corresponds to importing Python modules with import clauses."""
        cls._plugmaster.load()

    def install_plugins(self) -> None:
        """Installs plugins into the  application, by calling the
        install() method of each loaded plugin module."""
        self._plugmaster.install(self)

    def deserialize(self) -> None:
        """Deserialize instances from the startup file specified by 'serialization_file' class attribute, or
        '--file' startup argument.
        """
        if self.serialization_file != "":
            self.info(f"Loading masterpieces from {self.serialization_file}")

            with open(self.serialization_file, "r", encoding="utf-8") as f:
                self.deserialize_from_json(f)
                self.info(f"File {self.serialization_file} successfully loaded")

    def serialize(self) -> None:
        """Serialize application state to the file specified by 'serialization_file' class attribute'."""
        if self.serialization_file != "":
            self.info(f"Saving masterpieces to {self.serialization_file}")

            with open(self.serialization_file, "w", encoding="utf-8") as f:
                self.serialize_to_json(f)
                self.info(f"File {self.serialization_file} successfully written")

    @classmethod
    def register_args(cls, parser: argparse.ArgumentParser):
        """Register startup arguments to be parsed.

        Args:
            parser (argparse.ArgumentParser): parser to add the startup arguments.
        """
        parser.add_argument(
            "-f",
            "--file",
            help="Specify the file to load or save application state.",
        )

    @classmethod
    def configure_args(cls, args) -> None:
        if args.file is not None:
            cls.serialization_file = args.file

    @classmethod
    def register(cls):
        cls._plugmaster = PlugMaster(MasterPiece.get_app_name())
