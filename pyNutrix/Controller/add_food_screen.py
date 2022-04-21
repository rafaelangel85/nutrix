from View.AddFoodScreen.add_food_screen import AddFoodScreenView


class AddFoodScreenController:
    """
    The `MainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.main_screen.MainScreenModel
        self.view = AddFoodScreenView(controller=self, model=self.model)

    def get_view(self) -> AddFoodScreenView:
        return self.view