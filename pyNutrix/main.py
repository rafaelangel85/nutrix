"""
The entry point to the application.

The application uses the MVC template. Adhering to the principles of clean
architecture means ensuring that your application is easy to test, maintain,
and modernize.

You can read more about this template at the links below:

https://github.com/HeaTTheatR/LoginAppMVC
https://en.wikipedia.org/wiki/Model–view–controller
"""
import os
from typing import NoReturn
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from View.screens import screens
from kivy.lang import Builder
from View.MainScreen.main_screen import __version__ as major_version

__version__ = major_version


class Nutrix(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        self.manager_screens = ScreenManager()

    def build(self) -> ScreenManager:
        """
        Initializes the application; it will be called only once.
        If this method returns a widget (tree), it will be used as the root
        widget and added to the window.

        :return:
            None or a root :class:`~kivy.uix.widget.Widget` instance
            if no self.root exists.
        """

        self.theme_cls.primary_palette = "Amber"
        self.generate_application_screens()
        return self.manager_screens

    def generate_application_screens(self) -> NoReturn:
        """
        Creating and adding screens to the screen manager.
        You should not change this cycle unnecessarily. He is self-sufficient.

        If you need to add any screen, open the `View.screens.py` module and
        see how new screens are added according to the given application
        architecture.
        """

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

    def load_all_kv_files(self, path_to_directory: str) -> None:
        """
        Recursively loads KV files from the selected directory.
        .. versionadded:: 1.0.0
        """

        for path_to_dir, dirs, files in os.walk(path_to_directory):
            if (
                    "venv" in path_to_dir
                    or ".buildozer" in path_to_dir
                    or "kivymd/tools/patterns/MVC" in path_to_dir
            ):
                continue
            for name_file in files:
                if (
                        os.path.splitext(name_file)[1] == ".kv"
                        and name_file != "style.kv"  # if use PyInstaller
                        and "__MACOS" not in path_to_dir  # if use Mac OS
                ):
                    path_to_kv_file = os.path.join(path_to_dir, name_file)
                    Builder.load_file(path_to_kv_file)


Nutrix().run()
