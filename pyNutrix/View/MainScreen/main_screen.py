from typing import NoReturn
from kivy.app import App

from View.base_screen import BaseScreenView

__version__ = '0.0.2'

class MainScreenView(BaseScreenView):
    """Implements the login start screen in the user application."""

    def model_is_changed(self) -> NoReturn:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

    def set_screen(self, screen: App) -> NoReturn:
        App.get_running_app().root.current = screen

    def get_version(self) -> str:
        return __version__
