import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "virtual_mouse")))

from gesture_control import GestureController

class TestGestureController(unittest.TestCase):
    def setUp(self):
        self.controller = GestureController(click_threshold=30, right_click_threshold=30, click_cooldown=0.1)

    def test_distance_calculation(self):
        p1 = (0, 0)
        p2 = (3, 4)
        self.assertEqual(self.controller.get_distance(p1, p2), 5.0)

    def test_empty_landmarks(self):
        gesture, data = self.controller.detect_gesture([])
        self.assertEqual(gesture, "NONE")

    def test_left_click_detection(self):
        # Crear 21 puntos dummy donde pulgar (4) e índice (8) están muy juntos
        landmarks = [(i, 100, 100) for i in range(21)]
        landmarks[4] = (4, 100, 100)  # Pulgar
        landmarks[8] = (8, 110, 105)  # Índice (distancia ~11 px < 30)
        landmarks[12] = (12, 200, 200) # Medio lejos

        gesture, data = self.controller.detect_gesture(landmarks)
        self.assertEqual(gesture, "LEFT_CLICK")

if __name__ == "__main__":
    unittest.main()
