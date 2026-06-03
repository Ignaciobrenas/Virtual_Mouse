import pyautogui
import numpy as np

class MouseController:
    """Controlador de ratón con suavizado, escalado y soporte de múltiples acciones."""
    def __init__(self, smoothening=4, margin=50):
        # Desactivar latencia por defecto de PyAutoGUI para máxima fluidez
        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = False

        self.screen_w, self.screen_h = pyautogui.size()
        self.smoothening = max(1, smoothening)
        self.margin = margin
        self.prev_x = self.screen_w // 2
        self.prev_y = self.screen_h // 2
        self.is_mouse_down = False

    def move_mouse(self, x, y, cam_w, cam_h):
        """Interpola y suaviza el movimiento del cursor hacia las coordenadas de la pantalla."""
        # Interpolación con margen para alcanzar las esquinas del monitor
        screen_x = np.interp(x, (self.margin, cam_w - self.margin), (0, self.screen_w))
        screen_y = np.interp(y, (self.margin, cam_h - self.margin), (0, self.screen_h))

        # Restringir a los límites reales de la pantalla
        screen_x = np.clip(screen_x, 0, self.screen_w - 1)
        screen_y = np.clip(screen_y, 0, self.screen_h - 1)

        # Filtro de media móvil exponencial para eliminar vibraciones
        curr_x = self.prev_x + (screen_x - self.prev_x) / self.smoothening
        curr_y = self.prev_y + (screen_y - self.prev_y) / self.smoothening

        pyautogui.moveTo(curr_x, curr_y)
        self.prev_x, self.prev_y = curr_x, curr_y

    def click(self):
        """Clic izquierdo."""
        pyautogui.click()

    def right_click(self):
        """Clic derecho secundario."""
        pyautogui.rightClick()

    def double_click(self):
        """Doble clic rápido."""
        pyautogui.doubleClick()

    def mouse_down(self):
        """Presionar botón izquierdo sin soltar (arrastrar)."""
        if not self.is_mouse_down:
            pyautogui.mouseDown()
            self.is_mouse_down = True

    def mouse_up(self):
        """Soltar botón izquierdo tras arrastrar."""
        if self.is_mouse_down:
            pyautogui.mouseUp()
            self.is_mouse_down = False

    def scroll(self, amount):
        """Desplazamiento vertical de rueda de ratón."""
        pyautogui.scroll(int(amount))

    def set_smoothening(self, value):
        self.smoothening = max(1, int(value))

    def set_margin(self, value):
        self.margin = max(10, int(value))
# Zero delay configuration enabled
# Zero delay configuration enabled
