import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "virtual_mouse")))
from mouse_controller import MouseController

class TestMouseController(unittest.TestCase):
    def test_init(self):
        mc = MouseController(smoothening=5, margin=40)
        self.assertEqual(mc.smoothening, 5)
        self.assertEqual(mc.margin, 40)

if __name__ == "__main__":
    unittest.main()
