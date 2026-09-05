import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "virtual_mouse")))

from i18n import t, SUPPORTED_LANGUAGES
from tony_stark import TonyStarkController

class TestNewFeatures(unittest.TestCase):
    def test_i18n_languages(self):
        langs = [code for code, name in SUPPORTED_LANGUAGES]
        self.assertIn("es", langs)
        self.assertIn("en", langs)
        self.assertIn("fr", langs)
        self.assertIn("pt", langs)

    def test_i18n_translations(self):
        self.assertEqual(t("btn_start", "es"), "¡Comenzar ahora! (Enter)")
        self.assertEqual(t("btn_start", "en"), "Start Now! (Enter)")
        self.assertEqual(t("btn_start", "fr"), "Démarrer maintenant! (Entrée)")
        self.assertEqual(t("btn_start", "pt"), "Começar agora! (Enter)")

    def test_stark_controller_repulsor(self):
        stark = TonyStarkController()
        # Mano vacía
        self.assertFalse(stark.is_repulsor_pose([]))

        # Crear 21 puntos donde las 4 puntas de los dedos están por encima de las articulaciones PIP
        landmarks = [(i, 100, 100) for i in range(21)]
        # Puntas (y menor = más arriba en la pantalla)
        landmarks[8] = (8, 100, 40)   # Índice punta arriba
        landmarks[6] = (6, 100, 80)   # Índice articulación abajo
        landmarks[12] = (12, 120, 35) # Medio punta arriba
        landmarks[10] = (10, 120, 80) # Medio articulación abajo
        landmarks[16] = (16, 140, 40) # Anular punta arriba
        landmarks[14] = (14, 140, 80) # Anular articulación abajo
        landmarks[20] = (20, 160, 45) # Meñique punta arriba
        landmarks[18] = (18, 160, 80) # Meñique articulación abajo

        self.assertTrue(stark.is_repulsor_pose(landmarks))

if __name__ == "__main__":
    unittest.main()
