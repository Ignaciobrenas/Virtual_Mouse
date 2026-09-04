import time
import webbrowser
import pyautogui
import threading
import sys

class TonyStarkController:
    """Controlador de gestos especiales Modo Tony Stark / JARVIS."""
    def __init__(self, activation_cooldown=3.0):
        self.activation_cooldown = activation_cooldown
        self.last_activation_time = 0
        self.palm_open_start = 0
        self.is_active = False

    def is_repulsor_pose(self, landmarks):
        """
        Detecta la pose de 'Repulsor' de Iron Man:
        Palma abierta completamente hacia la cámara con los 5 dedos extendidos.
        """
        if not landmarks or len(landmarks) < 21:
            return False

        # Comprobar que los 4 dedos largos (índice, medio, anular, meñique) estén extendidos hacia arriba
        # y que el pulgar esté separado
        wrist = landmarks[0]
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]

        # Puntas deben estar significativamente por encima de sus articulaciones PIP
        index_extended = index_tip[2] < landmarks[6][2]
        middle_extended = middle_tip[2] < landmarks[10][2]
        ring_extended = ring_tip[2] < landmarks[14][2]
        pinky_extended = pinky_tip[2] < landmarks[18][2]

        # Separación entre dedos para confirmar mano completamente abierta
        if index_extended and middle_extended and ring_extended and pinky_extended:
            return True
        return False

    def check_and_trigger(self, landmarks):
        """
        Evalúa si la pose de repulsor se mantiene por ~0.5s para lanzar Copilot.
        Retorna True si se acaba de disparar el evento Copilot.
        """
        now = time.time()
        if now - self.last_activation_time < self.activation_cooldown:
            return False

        if self.is_repulsor_pose(landmarks):
            if self.palm_open_start == 0:
                self.palm_open_start = now
            elif now - self.palm_open_start > 0.5:
                # Mantener pose por 0.5s dispara la llamada a Copilot
                self.last_activation_time = now
                self.palm_open_start = 0
                self.launch_copilot()
                return True
        else:
            self.palm_open_start = 0

        return False

    def launch_copilot(self):
        """Lanza Microsoft Copilot usando el atajo nativo de Windows o navegador."""
        def _launch():
            try:
                # Sonido de alta frecuencia futurista (Estilo repulsor)
                if sys.platform.startswith("win"):
                    import winsound
                    winsound.Beep(1800, 100)
                    winsound.Beep(2400, 150)

                # Intentar atajo nativo de Windows para Copilot (Win + C)
                pyautogui.hotkey('win', 'c')
                time.sleep(0.5)

                # Si el atajo no abre la app dedicada en versiones de Windows sin Copilot preinstalado, abrir web
            except Exception:
                try:
                    webbrowser.open("https://copilot.microsoft.com")
                except Exception:
                    pass

        threading.Thread(target=_launch, daemon=True).start()
