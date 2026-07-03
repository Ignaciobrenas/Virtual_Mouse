import cv2
import sys
import os

# Asegurar importación de módulos locales sin importar desde qué directorio se ejecute
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar codificación segura de terminal en Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

from hand_tracking import HandTracker
from mouse_controller import MouseController
from gesture_control import GestureController


def main():
    print("=" * 60)
    print("[*] INICIANDO VIRTUAL MOUSE")
    print("------------------------------------------------------------")
    print(" - Dedo indice: Mueve el cursor en pantalla")
    print(" - Pellizco (Indice + Pulgar): Clic izquierdo")
    print(" - Pulsa la tecla 'q' en la ventana de video para salir")
    print("=" * 60)

    if sys.platform.startswith("win"):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(0)


    if not cap.isOpened():
        print("[!] Error: No se pudo acceder a la camara web (indice 0).")
        print("    Verifica que tu camara este conectada y tenga permisos.")
        return


    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    hand_tracker = HandTracker()
    mouse = MouseController(smoothening=4, margin=50)
    gesture = GestureController(click_threshold=35, click_cooldown=0.3)

    while True:
        success, frame = cap.read()
        if not success or frame is None:
            continue

        # Invertir la imagen horizontalmente para efecto espejo natural
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Marco visual de zona activa para el mouse
        margin = mouse.margin
        cv2.rectangle(frame, (margin, margin), (w - margin, h - margin), (200, 200, 200), 1)

        landmarks = hand_tracker.find_hand_landmarks(frame)

        if landmarks and len(landmarks) > 8:
            index_x, index_y = landmarks[8][1], landmarks[8][2]
            thumb_x, thumb_y = landmarks[4][1], landmarks[4][2]

            # Mover el cursor con la punta del dedo índice
            mouse.move_mouse(index_x, index_y, w, h)

            # Resaltar la punta del dedo índice
            cv2.circle(frame, (index_x, index_y), 8, (255, 0, 255), cv2.FILLED)

            # Detección y feedback de clic
            if gesture.is_click(landmarks):
                mouse.click()
                click_mid_x = (index_x + thumb_x) // 2
                click_mid_y = (index_y + thumb_y) // 2
                cv2.circle(frame, (click_mid_x, click_mid_y), 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, "CLICK!", (click_mid_x - 30, click_mid_y - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Instrucción en pantalla para salir
        cv2.putText(frame, "Presiona 'q' para salir", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow("Virtual Mouse - Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Virtual Mouse finalizado correctamente.")


if __name__ == "__main__":
    main()

# DirectShow camera support
