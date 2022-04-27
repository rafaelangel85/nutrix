
class FoodUnit(object):
    def __init__(self):
        self.proteins_gr = 0.0
        self.carbohydrates_gr = 0.0
        self.fats_gr = 0.0
        self.energy_kcal = 0.0

    def __str__(self):
        return f'({self.proteins_gr},{self.carbohydrates_gr},{self.fats_gr},{self.energy_kcal})'
