import sys
import os
import time
import warnings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import customtkinter as ctk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hand_tracking import HandTracker
from mouse_controller import MouseController
from gesture_control import GestureController
from config import load_config, save_config
from sound import play_click_sound, play_action_sound

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class VirtualMouseGUI(ctk.CTk):
    """Ventana principal moderna con panel de control, configuración y vista previa."""
    def __init__(self):
        super().__init__()

        self.title("Virtual Mouse Studio • Ignaciobrenas")
        self.geometry("860x780")
        self.minsize(780, 700)

        # Cargar configuración persistente
        self.cfg = load_config()

        # Variables de control
        self.show_preview = True
        self.enable_mouse = False
        self.running = True
        self.app_started = False
        self.cap = None

        # Métricas de rendimiento
        self.prev_frame_time = 0
        self.fps = 0

        # Módulos del sistema
        self.hand_tracker = HandTracker()
        self.mouse = MouseController(
            smoothening=self.cfg.get("smoothening", 4),
            margin=self.cfg.get("margin", 50)
        )
        self.gesture = GestureController(
            click_threshold=self.cfg.get("click_threshold", 35),
            right_click_threshold=self.cfg.get("right_click_threshold", 35),
            click_cooldown=0.3
        )

        self.setup_ui()
        self.bind("<Return>", lambda e: self.start_tracking())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        # 1. Cabecera con título, autor y estado
        header = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12)
        header.pack(fill="x", padx=20, pady=(15, 10))

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left", padx=15, pady=10)

        title = ctk.CTkLabel(
            title_box,
            text="🖱️ Virtual Mouse Studio",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#f8fafc"
        )
        title.pack(anchor="w")

        author = ctk.CTkLabel(
            title_box,
            text="by Ignaciobrenas • Control Gestual Inteligente",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        )
        author.pack(anchor="w")

        # Indicador de FPS y estado
        stats_box = ctk.CTkFrame(header, fg_color="transparent")
        stats_box.pack(side="right", padx=15, pady=10)

        self.fps_badge = ctk.CTkLabel(
            stats_box,
            text="FPS: --",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#1e293b",
            text_color="#94a3b8",
            corner_radius=8,
            padx=10,
            pady=5
        )
        self.fps_badge.pack(side="left", padx=(0, 10))

        self.status_badge = ctk.CTkLabel(
            stats_box,
            text="⏸️ ESPERANDO INICIO",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#1e293b",
            text_color="#94a3b8",
            corner_radius=8,
            padx=14,
            pady=6
        )
        self.status_badge.pack(side="left")

        # 2. Contenedor Central
        self.preview_container = ctk.CTkFrame(
            self,
            fg_color="#0b0f19",
            corner_radius=16,
            border_width=1,
            border_color="#1e293b"
        )
        self.preview_container.pack(fill="both", expand=True, padx=20, pady=10)

        # --- TARJETA DE BIENVENIDA INTEGRADA ---
        self.welcome_card = ctk.CTkFrame(
            self.preview_container,
            fg_color="#131722",
            corner_radius=16,
            border_width=2,
            border_color="#3b82f6"
        )
        self.welcome_card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.75, relheight=0.85)

        icon_label = ctk.CTkLabel(self.welcome_card, text="🖱️", font=ctk.CTkFont(size=44))
        icon_label.pack(pady=(22, 4))

        welcome_title = ctk.CTkLabel(
            self.welcome_card,
            text="Virtual Mouse AI",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#60a5fa"
        )
        welcome_title.pack(pady=(0, 2))

        author_badge = ctk.CTkLabel(
            self.welcome_card,
            text="Desarrollado por Ignaciobrenas",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1e293b",
            corner_radius=8,
            text_color="#38bdf8",
            padx=16,
            pady=6
        )
        author_badge.pack(pady=10)

        desc_label = ctk.CTkLabel(
            self.welcome_card,
            text="Proyecto personal para practicar y aprender\nPython, OpenCV y MediaPipe.",
            font=ctk.CTkFont(size=13),
            text_color="#94a3b8",
            justify="center"
        )
        desc_label.pack(pady=4)

        # Gestos soportados
        gestures_guide = ctk.CTkFrame(self.welcome_card, fg_color="#1a202c", corner_radius=10)
        gestures_guide.pack(padx=30, pady=10, fill="x")

        gestures_text = ctk.CTkLabel(
            gestures_guide,
            text="• ☝️ Dedo índice: Mover cursor suavemente\n• 🤏 Pellizco (índice + pulgar): Clic izquierdo\n• ✌️ Pellizco (medio + pulgar): Clic derecho\n• 📜 Dos dedos arriba (índice + medio): Scroll vertical\n• ✊ Mantener pellizco (>0.5s): Arrastrar y soltar",
            font=ctk.CTkFont(size=12),
            text_color="#cbd5e1",
            justify="left"
        )
        gestures_text.pack(padx=15, pady=10)

        self.btn_start = ctk.CTkButton(
            self.welcome_card,
            text="¡Comenzar ahora! (Enter)",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            height=42,
            corner_radius=12,
            command=self.start_tracking
        )
        self.btn_start.pack(pady=(8, 18), padx=50, fill="x")

        # Label para render de vídeo
        self.video_label = tk.Label(self.preview_container, bg="#0b0f19", borderwidth=0)

        # Panel de vista previa oculta
        self.placeholder_frame = ctk.CTkFrame(self.preview_container, fg_color="transparent")
        ph_icon = ctk.CTkLabel(self.placeholder_frame, text="👁️‍🗨️", font=ctk.CTkFont(size=52))
        ph_icon.pack(pady=(50, 10))
        ph_title = ctk.CTkLabel(
            self.placeholder_frame,
            text="Vista Previa Oculta",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#94a3b8"
        )
        ph_title.pack(pady=5)
        ph_desc = ctk.CTkLabel(
            self.placeholder_frame,
            text="El ratón virtual sigue activo en segundo plano.\nAhorrando recursos de pantalla y GPU.",
            font=ctk.CTkFont(size=13),
            text_color="#64748b",
            justify="center"
        )
        ph_desc.pack(pady=(5, 30))

        # Indicador flotante de acción detectada
        self.action_label = ctk.CTkLabel(
            self.preview_container,
            text="LISTO",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1e293b",
            text_color="#38bdf8",
            corner_radius=8,
            padx=14,
            pady=5
        )

        # 3. Barra de Botones Inferior
        btn_bar = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12)
        btn_bar.pack(fill="x", padx=20, pady=(10, 15))

        self.btn_toggle_preview = ctk.CTkButton(
            btn_bar,
            text="👁️ Ocultar Vista Previa",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#334155",
            hover_color="#475569",
            corner_radius=10,
            height=42,
            command=self.toggle_preview
        )
        self.btn_toggle_preview.pack(side="left", padx=15, pady=12, expand=True, fill="x")

        self.btn_toggle_mouse = ctk.CTkButton(
            btn_bar,
            text="🖱️ Pausar Ratón",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0284c7",
            hover_color="#0369a1",
            corner_radius=10,
            height=42,
            command=self.toggle_mouse
        )
        self.btn_toggle_mouse.pack(side="left", padx=10, pady=12, expand=True, fill="x")

        # Botón para alternar sonido
        self.sound_enabled = self.cfg.get("sound_enabled", True)
        self.btn_toggle_sound = ctk.CTkButton(
            btn_bar,
            text="🔊 Sonido: ON" if self.sound_enabled else "🔇 Sonido: OFF",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1e293b",
            hover_color="#334155",
            corner_radius=10,
            height=42,
            command=self.toggle_sound
        )
        self.btn_toggle_sound.pack(side="left", padx=10, pady=12, expand=True, fill="x")

        btn_exit = ctk.CTkButton(
            btn_bar,
            text="🛑 Salir",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            corner_radius=10,
            height=42,
            command=self.on_close
        )
        btn_exit.pack(side="right", padx=15, pady=12, expand=True, fill="x")

    def start_tracking(self):
        if self.app_started:
            return

        self.app_started = True
        self.enable_mouse = True

        self.welcome_card.place_forget()
        self.video_label.pack(expand=True, fill="both", padx=10, pady=10)
        self.action_label.place(relx=0.03, rely=0.04)

        self.status_badge.configure(text="🟡 CONECTANDO CÁMARA...", fg_color="#78350f", text_color="#fde68a")
        self.update_idletasks()

        if sys.platform.startswith("win"):
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.status_badge.configure(text="❌ CÁMARA NO DISPONIBLE", fg_color="#7f1d1d", text_color="#fca5a5")
            self.video_label.configure(
                text="❌ No se pudo acceder a la cámara web.\nVerifica que esté conectada y que no la esté usando otra app.",
                font=("Arial", 14),
                fg="#fca5a5"
            )
            return

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.update_status_badge()
        self.prev_frame_time = time.time()
        self.update_loop()

    def toggle_preview(self):
        if not self.app_started:
            return
        self.show_preview = not self.show_preview
        if self.show_preview:
            self.btn_toggle_preview.configure(text="👁️ Ocultar Vista Previa")
            self.placeholder_frame.pack_forget()
            self.video_label.pack(expand=True, fill="both", padx=10, pady=10)
            self.action_label.place(relx=0.03, rely=0.04)
        else:
            self.btn_toggle_preview.configure(text="👁️ Ver Vista Previa")
            self.video_label.pack_forget()
            self.action_label.place_forget()
            self.placeholder_frame.pack(expand=True, fill="both")
        self.update_status_badge()

    def toggle_mouse(self):
        if not self.app_started:
            return
        self.enable_mouse = not self.enable_mouse
        if self.enable_mouse:
            self.btn_toggle_mouse.configure(text="🖱️ Pausar Ratón", fg_color="#0284c7", hover_color="#0369a1")
        else:
            self.btn_toggle_mouse.configure(text="▶️ Reanudar Ratón", fg_color="#ca8a04", hover_color="#a16207")
        self.update_status_badge()

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.cfg["sound_enabled"] = self.sound_enabled
        save_config(self.cfg)
        if self.sound_enabled:
            self.btn_toggle_sound.configure(text="🔊 Sonido: ON", fg_color="#1e293b")
        else:
            self.btn_toggle_sound.configure(text="🔇 Sonido: OFF", fg_color="#334155")

    def update_status_badge(self):
        if not self.app_started:
            self.status_badge.configure(text="⏸️ ESPERANDO INICIO", fg_color="#1e293b", text_color="#94a3b8")
        elif not self.enable_mouse:
            self.status_badge.configure(text="⏸️ RATÓN EN PAUSA", fg_color="#451a03", text_color="#fdba74")
        elif self.show_preview:
            self.status_badge.configure(text="🟢 RASTREANDO", fg_color="#064e3b", text_color="#34d399")
        else:
            self.status_badge.configure(text="🟡 VISTA PREVIA OCULTA", fg_color="#78350f", text_color="#fde68a")

    def update_loop(self):
        if not self.running or not self.app_started:
            return

        if self.cap is None or not self.cap.isOpened():
            self.status_badge.configure(text="❌ CÁMARA DESCONECTADA", fg_color="#7f1d1d", text_color="#fca5a5")
            return

        # Medir FPS
        curr_time = time.time()
        time_diff = curr_time - self.prev_frame_time
        if time_diff > 0:
            self.fps = int(1.0 / time_diff)
        self.prev_frame_time = curr_time
        self.fps_badge.configure(text=f"FPS: {self.fps}")

        success, frame = self.cap.read()
        if success and frame is not None:
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            landmarks = self.hand_tracker.find_hand_landmarks(frame, draw=self.show_preview)

            if landmarks and len(landmarks) > 20:
                index_x, index_y = landmarks[8][1], landmarks[8][2]
                thumb_x, thumb_y = landmarks[4][1], landmarks[4][2]
                middle_x, middle_y = landmarks[12][1], landmarks[12][2]

                # Detección de gestos avanzada
                gesture_type, g_data = self.gesture.detect_gesture(landmarks)

                # Procesar acción según el gesto
                if self.enable_mouse:
                    if gesture_type == "MOVE":
                        self.mouse.move_mouse(index_x, index_y, w, h)
                        self.action_label.configure(text="👆 MOVIENDO", fg_color="#1e293b", text_color="#38bdf8")
                    elif gesture_type == "LEFT_CLICK":
                        self.mouse.click()
                        if self.sound_enabled:
                            play_click_sound()
                        self.action_label.configure(text="🖱️ CLIC IZQUIERDO", fg_color="#065f46", text_color="#34d399")
                    elif gesture_type == "RIGHT_CLICK":
                        self.mouse.right_click()
                        if self.sound_enabled:
                            play_action_sound()
                        self.action_label.configure(text="🖱️ CLIC DERECHO", fg_color="#854d0e", text_color="#fde047")
                    elif gesture_type == "DRAG_START":
                        self.mouse.mouse_down()
                        if self.sound_enabled:
                            play_action_sound()
                        self.action_label.configure(text="✊ ARRASTRANDO...", fg_color="#7f1d1d", text_color="#fca5a5")
                    elif gesture_type == "DRAGGING":
                        self.mouse.move_mouse(index_x, index_y, w, h)
                        self.action_label.configure(text="✊ ARRASTRANDO...", fg_color="#7f1d1d", text_color="#fca5a5")
                    elif gesture_type == "DRAG_STOP":
                        self.mouse.mouse_up()
                        self.action_label.configure(text="✋ SOLTADO", fg_color="#1e293b", text_color="#94a3b8")
                    elif gesture_type == "SCROLL_UP":
                        self.mouse.scroll(self.cfg.get("scroll_speed", 20))
                        self.action_label.configure(text="📜 SCROLL ARRIBA", fg_color="#3730a3", text_color="#a5b4fc")
                    elif gesture_type == "SCROLL_DOWN":
                        self.mouse.scroll(-self.cfg.get("scroll_speed", 20))
                        self.action_label.configure(text="📜 SCROLL ABAJO", fg_color="#3730a3", text_color="#a5b4fc")

                # Resaltar puntos de los dedos en la vista previa
                if self.show_preview:
                    fingertips = [
                        (4, (0, 255, 128)),    # Pulgar: Verde Neón
                        (8, (255, 0, 255)),    # Índice: Magenta Neón
                        (12, (255, 230, 0)),   # Medio: Amarillo
                        (16, (0, 165, 255)),   # Anular: Naranja
                        (20, (255, 100, 100))  # Meñique: Rosa
                    ]
                    for f_idx, color in fingertips:
                        if len(landmarks) > f_idx:
                            fx, fy = landmarks[f_idx][1], landmarks[f_idx][2]
                            cv2.circle(frame, (fx, fy), 8, color, cv2.FILLED)
                            cv2.circle(frame, (fx, fy), 11, (255, 255, 255), 1)

                    # Anillo indicador en el cursor índice
                    cv2.circle(frame, (index_x, index_y), 15, (255, 0, 255), 2)

                    # Visualización dinámica según el gesto activo
                    if gesture_type in ["LEFT_CLICK", "DRAG_START", "DRAGGING"]:
                        mid_x = (index_x + thumb_x) // 2
                        mid_y = (index_y + thumb_y) // 2
                        cv2.circle(frame, (mid_x, mid_y), 20, (0, 255, 0), cv2.FILLED)
                        cv2.circle(frame, (mid_x, mid_y), 25, (255, 255, 255), 2)
                        cv2.putText(frame, "CLICK!", (mid_x - 38, mid_y - 28),
                                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2)
                    elif gesture_type == "RIGHT_CLICK":
                        mid_x = (middle_x + thumb_x) // 2
                        mid_y = (middle_y + thumb_y) // 2
                        cv2.circle(frame, (mid_x, mid_y), 20, (0, 215, 255), cv2.FILLED)
                        cv2.circle(frame, (mid_x, mid_y), 25, (255, 255, 255), 2)
                        cv2.putText(frame, "RIGHT CLICK!", (mid_x - 60, mid_y - 28),
                                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 215, 255), 2)

            # Renderizar marco de vídeo
            if self.show_preview:
                margin = self.mouse.margin
                cv2.rectangle(frame, (margin, margin), (w - margin, h - margin), (90, 90, 90), 1)

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                container_w = self.preview_container.winfo_width()
                disp_w = max(480, min(640, container_w - 30 if container_w > 50 else 600))
                disp_h = int(disp_w * (h / w))
                resized = cv2.resize(rgb_frame, (disp_w, disp_h))

                img = Image.fromarray(resized)
                photo = ImageTk.PhotoImage(image=img)
                self.video_label.configure(image=photo)
                self.video_label.image = photo

        self.after(20, self.update_loop)

    def on_close(self):
        self.running = False
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.destroy()


def launch_gui():
    app = VirtualMouseGUI()
    app.mainloop()


if __name__ == "__main__":
    launch_gui()
# Fast video canvas buffer
