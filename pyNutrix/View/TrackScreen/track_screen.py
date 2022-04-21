from typing import NoReturn
from kivy.app import App

from View.base_screen import BaseScreenView


class TrackScreenView(BaseScreenView):
    """Implements the tracking screen in the user application."""

    def set_screen(self, screen: App) -> NoReturn:
        App.get_running_app().root.current = screen

    def on_press_breakfast(self) -> NoReturn:
        test = 1
        pass
