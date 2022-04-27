from View.base_screen import BaseScreenView
from typing import NoReturn
from kivy.app import App
from kivymd.uix.list import OneLineListItem
from kivymd.uix.behaviors import TouchBehavior
import json
import os
from Model.food_unit import FoodUnit

json_path = os.path.join(os.path.curdir, 'data/data.json')
json_file = json.load(open(json_path))

food_selected = FoodUnit()


class TouchableOneListItem(OneLineListItem, TouchBehavior):

    def on_touch_up(self, touch):
        for food in json_file['food']:
            if food == self.text:
                food_selected.carbohydrates_gr = json_file['food'][food]['nutrition_data']['carbohydrate']
                food_selected.proteins_gr = json_file['food'][food]['nutrition_data']['protein']
                food_selected.fats_gr = json_file['food'][food]['nutrition_data']['fat']
                food_selected.energy_kcal = json_file['food'][food]['nutrition_data']['energy']
                App.get_running_app().root.current = 'food quantity screen'


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
        for food in json_file['food']:
            self.ids.available_food_list.add_widget(TouchableOneListItem(text=food))
