import math

class GestureController:
    def __init__(self, click_threshold=35):
        self.click_threshold = click_threshold

    def get_distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
