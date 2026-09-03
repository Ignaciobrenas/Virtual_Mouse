import cv2
import mediapipe as mp


class HandTracker:
    """Rastreador de manos con soporte para 1 o 2 manos simultáneas y personalización visual."""
    def __init__(self, max_hands=2, detection_con=0.7, track_con=0.7):
        self.max_hands = max_hands
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con
        )

        # Paleta minimalista profesional: Verde esmeralda y cian sobrio
        self.style_right_points = self.mp_draw.DrawingSpec(color=(16, 185, 129), thickness=3, circle_radius=4)
        self.style_right_conns = self.mp_draw.DrawingSpec(color=(5, 150, 105), thickness=2, circle_radius=2)

        # Paleta mano secundaria (izquierda): Ámbar / Dorado sutil
        self.style_left_points = self.mp_draw.DrawingSpec(color=(245, 158, 11), thickness=3, circle_radius=4)
        self.style_left_conns = self.mp_draw.DrawingSpec(color=(180, 100, 10), thickness=2, circle_radius=2)

    def find_all_hands(self, image, draw=True):
        """
        Detecta hasta 2 manos en la imagen.
        Retorna:
            list[dict]: [{"label": "Right"|"Left", "landmarks": [(idx, cx, cy), ...]}, ...]
        """
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        hands_data = []
        h, w, _ = image.shape

        if results.multi_hand_landmarks:
            for idx_hand, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Obtener etiqueta de mano si está disponible
                label = "Right"
                if results.multi_handedness and len(results.multi_handedness) > idx_hand:
                    label = results.multi_handedness[idx_hand].classification[0].label

                landmarks = []
                for idx, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append((idx, cx, cy))

                hands_data.append({"label": label, "landmarks": landmarks})

                if draw:
                    pts_spec = self.style_right_points if label == "Right" else self.style_left_points
                    con_spec = self.style_right_conns if label == "Right" else self.style_left_conns
                    self.mp_draw.draw_landmarks(
                        image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=pts_spec,
                        connection_drawing_spec=con_spec
                    )

        return hands_data

    def find_hand_landmarks(self, image, draw=True):
        """Compatibilidad con pipeline monomanual: devuelve la primera mano detectada."""
        hands = self.find_all_hands(image, draw=draw)
        if hands:
            return hands[0]["landmarks"]
        return []
