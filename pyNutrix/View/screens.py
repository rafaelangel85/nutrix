# The screens dictionary contains the objects of the models and controllers
# of the screens of the application.

from Model.main_screen import MainScreenModel
from Model.track_screen import TrackScreenModel
from Model.add_food_screen import AddFoodScreenModel

from Controller.main_screen import MainScreenController
from Controller.track_screen import TrackScreenController
from Controller.add_food_screen import AddFoodScreenController

screens = {
    "main screen": {
        "model": MainScreenModel,
        "controller": MainScreenController,
    },
    "track screen": {
        "model": TrackScreenModel,
        "controller": TrackScreenController,
    },
    "add food screen": {
        "model": AddFoodScreenModel,
        "controller": AddFoodScreenController,
    }
}
