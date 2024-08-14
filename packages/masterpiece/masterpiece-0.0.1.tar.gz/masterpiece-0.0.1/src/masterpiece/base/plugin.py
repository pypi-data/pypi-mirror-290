from .composite import Composite, MasterPiece


class Plugin(MasterPiece):

    def install(self, app: Composite):
        """Instantiate and install the classes in the plugin module into the application.
        This is an abstract method that the plugin classes must implement. Plugins may
        choose not to do anything here and instead leave it up to the higher level software layers.

        Args:
            app (Composite): application to plug into
        """
