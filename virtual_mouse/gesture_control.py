import math
import time


class GestureController:
    """Controlador avanzado de gestos para Virtual Mouse."""
    def __init__(self, click_threshold=35, right_click_threshold=35, click_cooldown=0.3):
        self.click_threshold = click_threshold
        self.right_click_threshold = right_click_threshold
        self.click_cooldown = click_cooldown

        self.last_left_click_time = 0
        self.last_right_click_time = 0
        self.pinch_start_time = 0
        self.is_dragging = False

        # Seguimiento previo de posición para scroll
        self.prev_scroll_y = None

    def get_distance(self, p1, p2):
        """Calcula la distancia euclidiana entre dos puntos (x, y)."""
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def detect_gesture(self, landmarks):
        """
        Analiza los puntos de la mano y determina el gesto actual.
        Retorna:
            gesture: str ("NONE", "MOVE", "LEFT_CLICK", "RIGHT_CLICK", "DRAG_START", "DRAG_STOP", "SCROLL_UP", "SCROLL_DOWN")
            data: dict con información contextual (ej: distancia, scroll_delta)
        """
        if not landmarks or len(landmarks) < 21:
            return "NONE", {}

        thumb = (landmarks[4][1], landmarks[4][2])
        index = (landmarks[8][1], landmarks[8][2])
        middle = (landmarks[12][1], landmarks[12][2])
        ring = (landmarks[16][1], landmarks[16][2])
        pinky = (landmarks[20][1], landmarks[20][2])

        thumb_index_dist = self.get_distance(thumb, index)
        thumb_middle_dist = self.get_distance(thumb, middle)
        index_middle_dist = self.get_distance(index, middle)

        current_time = time.time()

        # 1. Comprobar Gesto de Scroll: Índice y Corazón levantados juntos, y anular/meñique recogidos
        # Los dedos están levantados si la punta (y) está por encima de la articulación PIP (y del punto 6 y 10)
        index_up = landmarks[8][2] < landmarks[6][2]
        middle_up = landmarks[12][2] < landmarks[10][2]
        ring_down = landmarks[16][2] > landmarks[14][2]
        pinky_down = landmarks[20][2] > landmarks[18][2]

        if index_up and middle_up and ring_down and pinky_down and index_middle_dist < 45:
            avg_y = (index[1] + middle[1]) / 2
            if self.prev_scroll_y is not None:
                diff_y = self.prev_scroll_y - avg_y
                self.prev_scroll_y = avg_y
                if abs(diff_y) > 4:
                    action = "SCROLL_UP" if diff_y > 0 else "SCROLL_DOWN"
                    return action, {"delta": diff_y}
            else:
                self.prev_scroll_y = avg_y
            return "SCROLL_IDLE", {}
        else:
            self.prev_scroll_y = None

        # 2. Comprobar Clic Izquierdo y Arrastrar (Pellizco Pulgar + Índice)
        if thumb_index_dist < self.click_threshold:
            if self.pinch_start_time == 0:
                self.pinch_start_time = current_time

            duration = current_time - self.pinch_start_time

            # Si mantiene el pellizco más de 0.45s, activar Arrastrar y Soltar (Drag)
            if duration > 0.45 and not self.is_dragging:
                self.is_dragging = True
                return "DRAG_START", {"distance": thumb_index_dist}

            # Si es un toque rápido de pellizco, disparar clic izquierdo
            if not self.is_dragging and (current_time - self.last_left_click_time > self.click_cooldown):
                self.last_left_click_time = current_time
                return "LEFT_CLICK", {"distance": thumb_index_dist}

            if self.is_dragging:
                return "DRAGGING", {"distance": thumb_index_dist}
        else:
            # Si soltó el pellizco mientras arrastraba, soltar el clic
            if self.is_dragging:
                self.is_dragging = False
                self.pinch_start_time = 0
                return "DRAG_STOP", {}
            self.pinch_start_time = 0

        # 3. Comprobar Clic Derecho (Pellizco Pulgar + Corazón)
        if thumb_middle_dist < self.right_click_threshold and thumb_index_dist > self.click_threshold:
            if current_time - self.last_right_click_time > self.click_cooldown:
                self.last_right_click_time = current_time
                return "RIGHT_CLICK", {"distance": thumb_middle_dist}

        # Por defecto, mover cursor
        return "MOVE", {"x": index[0], "y": index[1]}

    def is_click(self, landmarks):
        """Compatibilidad con versiones anteriores."""
        gesture, _ = self.detect_gesture(landmarks)
        return gesture == "LEFT_CLICK"
# Vertical scroll support
# Drag and drop hold pinch support
