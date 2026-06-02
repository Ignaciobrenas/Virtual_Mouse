import pyautogui
import numpy as np

class MouseController:
    def __init__(self, margin=50):
        self.screen_w, self.screen_h = pyautogui.size()
        self.margin = margin

    def move_mouse(self, x, y, cam_w, cam_h):
        screen_x = np.interp(x, (self.margin, cam_w - self.margin), (0, self.screen_w))
        screen_y = np.interp(y, (self.margin, cam_h - self.margin), (0, self.screen_h))
        screen_x = np.clip(screen_x, 0, self.screen_w - 1)
        screen_y = np.clip(screen_y, 0, self.screen_h - 1)
        pyautogui.moveTo(screen_x, screen_y)
