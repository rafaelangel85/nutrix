from typing import NoReturn
from kivy.app import App
from kivy.properties import StringProperty

from View.base_screen import BaseScreenView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase

__version__ = '0.0.3'


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


class MainThreeTab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""
    content_text = StringProperty("")
