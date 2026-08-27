import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "virtual_mouse")))

from config import load_config, DEFAULT_CONFIG

class TestConfig(unittest.TestCase):
    def test_default_config_keys(self):
        cfg = load_config()
        self.assertIn("smoothening", cfg)
        self.assertIn("margin", cfg)
        self.assertIn("click_threshold", cfg)
        self.assertIn("sound_enabled", cfg)

if __name__ == "__main__":
    unittest.main()
