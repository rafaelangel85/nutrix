from View.base_screen import BaseScreenView
from typing import NoReturn
from kivy.app import App
from kivymd.uix.list import OneLineListItem
import json
import os


class AddFoodScreenView(BaseScreenView):
    """Implements the add food screen in the user application."""

    def model_is_changed(self) -> NoReturn:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

    @staticmethod
    def set_screen(screen: App) -> NoReturn:
        App.get_running_app().root.current = screen

    def do_the_list_view(self) -> NoReturn:
        json_path = os.path.join(os.path.curdir, 'data/data.json')
        json_file = json.load(open(json_path))

        for food in json_file['food']:
            self.ids.available_food_list.add_widget(OneLineListItem(text=food))
