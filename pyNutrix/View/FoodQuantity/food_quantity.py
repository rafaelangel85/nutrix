from kivy.app import App
from typing import NoReturn

from View.base_screen import BaseScreenView
from View.AddFoodScreen.add_food_screen import food_selected


class FoodQuantityScreenView(BaseScreenView):
    """Implements the tracking screen in the user application."""

    def set_screen(self, screen: App) -> NoReturn:
        App.get_running_app().root.current = screen

    def get_food_unit(self):
        return str(food_selected)
