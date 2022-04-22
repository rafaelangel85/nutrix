from View.base_screen import BaseScreenView
from typing import NoReturn

from kivy.app import App

from kivymd.uix.list import OneLineListItem

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

    def do_the_list_view(self) -> NoReturn:
        for i in range(0, 30):
            self.ids.available_food_list.add_widget(OneLineListItem(text=f"Single-line item {i}"))

