import sys
import threading

def play_click_sound():
    """Reproduce un sonido de clic sutil en un hilo secundario para no bloquear."""
    def _beep():
        try:
            if sys.platform.startswith("win"):
                import winsound
                # Beep corto y discreto a 1200 Hz por 35 ms
                winsound.Beep(1200, 35)
        except Exception:
            pass

    threading.Thread(target=_beep, daemon=True).start()


def play_action_sound():
    """Sonido para acciones como clic secundario o arrastrar."""
    def _beep():
        try:
            if sys.platform.startswith("win"):
                import winsound
                winsound.Beep(900, 45)
        except Exception:
            pass

    threading.Thread(target=_beep, daemon=True).start()
