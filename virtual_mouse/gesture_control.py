import math
import time

class GestureController:
    def __init__(self, click_threshold=35, click_cooldown=0.3):
        self.click_threshold = click_threshold
        self.click_cooldown = click_cooldown
        self.last_left_click_time = 0

    def get_distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def is_click(self, landmarks):
        if not landmarks or len(landmarks) < 9:
            return False
        thumb = (landmarks[4][1], landmarks[4][2])
        index = (landmarks[8][1], landmarks[8][2])
        dist = self.get_distance(thumb, index)
        now = time.time()
        if dist < self.click_threshold and (now - self.last_left_click_time > self.click_cooldown):
            self.last_left_click_time = now
            return True
        return False
