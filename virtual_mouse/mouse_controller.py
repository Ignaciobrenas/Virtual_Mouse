import pyautogui
import numpy as np

class MouseController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()

    def move_mouse(self, x, y, cam_w, cam_h):
        screen_x = np.interp(x, (0, cam_w), (0, self.screen_w))
        screen_y = np.interp(y, (0, cam_h), (0, self.screen_h))
        pyautogui.moveTo(screen_x, screen_y)
