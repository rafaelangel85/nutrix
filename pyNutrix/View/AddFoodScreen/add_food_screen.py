from View.base_screen import BaseScreenView
from typing import NoReturn

from kivy.app import App

class AddFoodScreenView(BaseScreenView):
    """Implements the add food screen in the user application."""

    def model_is_changed(self) -> NoReturn:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

    def set_screen(self, screen: App) -> NoReturn:
        App.get_running_app().root.current = screen

