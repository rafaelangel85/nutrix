

from View.MainScreen.main_screen import MainScreenView


class MainScreenController:
    """
    The `MainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.main_screen.MainScreenModel
        self.view = MainScreenView(controller=self, model=self.model)

    def on_tap_button_login(self) -> None:
        """Called when the `LOGIN` button is pressed."""

    def set_user_data(self, key, value) -> None:
        """Called every time the user enters text into the text fields."""

    def get_view(self) -> MainScreenView:
        return self.view
