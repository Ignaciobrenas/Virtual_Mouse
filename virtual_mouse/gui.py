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
from i18n import t, SUPPORTED_LANGUAGES
from tony_stark import TonyStarkController

# Configuración de tema visual: minimalista, profesional, oscuro
ctk.set_appearance_mode("Dark")


class VirtualMouseGUI(ctk.CTk):
    """
    Panel de control moderno con diseño minimalista en tonos verde bosque/esmeralda.
    Soporta:
    - Modo Dos Manos (Two Hands Mode)
    - Modo Tony Stark (Repulsor pose para invocar Copilot)
    - Selector multiidioma en tiempo real (ES / EN / FR / PT)
    - Ajustes persistentes y renderizado de vídeo de alto rendimiento.
    """
    def __init__(self):
        super().__init__()

        # Cargar configuración persistente
        self.cfg = load_config()
        self.current_lang = self.cfg.get("language", "es")

        # Configuración de ventana
        self.title(f"{t('app_title', self.current_lang)} • Ignaciobrenas")
        self.geometry("900x800")
        self.minsize(820, 720)
        self.configure(fg_color="#070b09")

        # Variables de control
        self.show_preview = True
        self.enable_mouse = False
        self.running = True
        self.app_started = False
        self.cap = None

        # Modos especiales
        self.two_hands_mode = self.cfg.get("two_hands_mode", True)
        self.tony_stark_mode = self.cfg.get("tony_stark_mode", True)
        self.sound_enabled = self.cfg.get("sound_enabled", True)

        # Diagnóstico FPS
        self.prev_frame_time = 0
        self.fps = 0

        # Controladores del sistema
        self.hand_tracker = HandTracker(max_hands=2 if self.two_hands_mode else 1)
        self.mouse = MouseController(
            smoothening=self.cfg.get("smoothening", 4),
            margin=self.cfg.get("margin", 50)
        )
        self.gesture = GestureController(
            click_threshold=self.cfg.get("click_threshold", 35),
            right_click_threshold=self.cfg.get("right_click_threshold", 35),
            click_cooldown=0.3
        )
        self.stark = TonyStarkController(activation_cooldown=3.0)

        # Inicializar interfaz gráfica
        self.setup_ui()
        self.bind("<Return>", lambda e: self.start_tracking())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        # 1. Barra de Cabecera (Matte Dark Forest)
        header = ctk.CTkFrame(self, fg_color="#0d1712", corner_radius=12, border_width=1, border_color="#162e21")
        header.pack(fill="x", padx=20, pady=(15, 10))

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left", padx=16, pady=12)

        self.title_label = ctk.CTkLabel(
            title_box,
            text=t("app_title", self.current_lang),
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#f2fbf6"
        )
        self.title_label.pack(anchor="w")

        self.author_label = ctk.CTkLabel(
            title_box,
            text=t("author_tag", self.current_lang),
            font=ctk.CTkFont(size=12),
            text_color="#6ee7b7"
        )
        self.author_label.pack(anchor="w")

        # Controles superiores derechos (Idioma, FPS, Estado)
        controls_box = ctk.CTkFrame(header, fg_color="transparent")
        controls_box.pack(side="right", padx=16, pady=12)

        # Selector de idioma moderno
        lang_values = [display for code, display in SUPPORTED_LANGUAGES]
        curr_display = next((d for c, d in SUPPORTED_LANGUAGES if c == self.current_lang), lang_values[0])
        self.lang_menu = ctk.CTkOptionMenu(
            controls_box,
            values=lang_values,
            command=self.on_language_change,
            fg_color="#13251c",
            button_color="#1a3528",
            button_hover_color="#254d3a",
            text_color="#a7f3d0",
            dropdown_fg_color="#0e1b14",
            dropdown_hover_color="#1a3528",
            dropdown_text_color="#e2f7ec",
            corner_radius=8,
            width=140,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.lang_menu.set(curr_display)
        self.lang_menu.pack(side="left", padx=(0, 10))

        self.fps_badge = ctk.CTkLabel(
            controls_box,
            text="FPS: --",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#13251c",
            text_color="#6ee7b7",
            corner_radius=8,
            padx=10,
            pady=5
        )
        self.fps_badge.pack(side="left", padx=(0, 10))

        self.status_badge = ctk.CTkLabel(
            controls_box,
            text=t("status_waiting", self.current_lang),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#13251c",
            text_color="#94a3b8",
            corner_radius=8,
            padx=14,
            pady=6
        )
        self.status_badge.pack(side="left")

        # 2. Contenedor Central de Vídeo
        self.preview_container = ctk.CTkFrame(
            self,
            fg_color="#080d0a",
            corner_radius=16,
            border_width=1,
            border_color="#15261c"
        )
        self.preview_container.pack(fill="both", expand=True, padx=20, pady=10)

        # --- TARJETA DE BIENVENIDA INTEGRADA ---
        self.welcome_card = ctk.CTkFrame(
            self.preview_container,
            fg_color="#0d1712",
            corner_radius=16,
            border_width=2,
            border_color="#059669"
        )
        self.welcome_card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.78, relheight=0.86)

        welcome_icon = ctk.CTkLabel(self.welcome_card, text="🖱️", font=ctk.CTkFont(size=44))
        welcome_icon.pack(pady=(20, 2))

        self.welcome_title_lbl = ctk.CTkLabel(
            self.welcome_card,
            text=t("welcome_title", self.current_lang),
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#34d399"
        )
        self.welcome_title_lbl.pack(pady=(0, 2))

        self.welcome_author_badge = ctk.CTkLabel(
            self.welcome_card,
            text=t("welcome_badge", self.current_lang),
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#14291e",
            corner_radius=8,
            text_color="#6ee7b7",
            padx=16,
            pady=5
        )
        self.welcome_author_badge.pack(pady=8)

        self.welcome_desc_lbl = ctk.CTkLabel(
            self.welcome_card,
            text=t("welcome_desc", self.current_lang),
            font=ctk.CTkFont(size=13),
            text_color="#94a3b8",
            justify="center"
        )
        self.welcome_desc_lbl.pack(pady=4)

        # Guía de Gestos
        self.guide_box = ctk.CTkFrame(self.welcome_card, fg_color="#111c15", corner_radius=10, border_width=1, border_color="#1b3325")
        self.guide_box.pack(padx=30, pady=10, fill="x")

        self.guide_text_lbl = ctk.CTkLabel(
            self.guide_box,
            text=self.get_guide_text(),
            font=ctk.CTkFont(size=12),
            text_color="#d1fae5",
            justify="left"
        )
        self.guide_text_lbl.pack(padx=16, pady=10, anchor="w")

        self.btn_start = ctk.CTkButton(
            self.welcome_card,
            text=t("btn_start", self.current_lang),
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#059669",
            hover_color="#047857",
            height=44,
            corner_radius=12,
            command=self.start_tracking
        )
        self.btn_start.pack(pady=(6, 16), padx=50, fill="x")

        # Label de renderizado de vídeo (tkinter de alto rendimiento)
        self.video_label = tk.Label(self.preview_container, bg="#080d0a", borderwidth=0)

        # Panel de vista oculta
        self.placeholder_frame = ctk.CTkFrame(self.preview_container, fg_color="transparent")
        ph_icon = ctk.CTkLabel(self.placeholder_frame, text="👁️‍🗨️", font=ctk.CTkFont(size=52))
        ph_icon.pack(pady=(55, 10))
        self.ph_title_lbl = ctk.CTkLabel(
            self.placeholder_frame,
            text=t("ph_title", self.current_lang),
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#6ee7b7"
        )
        self.ph_title_lbl.pack(pady=5)
        self.ph_desc_lbl = ctk.CTkLabel(
            self.placeholder_frame,
            text=t("ph_desc", self.current_lang),
            font=ctk.CTkFont(size=13),
            text_color="#64748b",
            justify="center"
        )
        self.ph_desc_lbl.pack(pady=(5, 30))

        # Badge flotante de acción en tiempo real
        self.action_label = ctk.CTkLabel(
            self.preview_container,
            text=t("action_ready", self.current_lang),
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0d1f16",
            text_color="#34d399",
            corner_radius=8,
            padx=14,
            pady=5
        )

        # 3. Barra de Botones de Control Inferior
        btn_bar = ctk.CTkFrame(self, fg_color="#0d1712", corner_radius=12, border_width=1, border_color="#162e21")
        btn_bar.pack(fill="x", padx=20, pady=(10, 15))

        # Botón 1: Alternar Vista Previa
        self.btn_toggle_preview = ctk.CTkButton(
            btn_bar,
            text=t("btn_hide_preview", self.current_lang),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#162b20",
            hover_color="#224232",
            text_color="#a7f3d0",
            corner_radius=10,
            height=40,
            command=self.toggle_preview
        )
        self.btn_toggle_preview.pack(side="left", padx=8, pady=10, expand=True, fill="x")

        # Botón 2: Pausar Ratón
        self.btn_toggle_mouse = ctk.CTkButton(
            btn_bar,
            text=t("btn_pause_mouse", self.current_lang),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#047857",
            hover_color="#059669",
            text_color="#ecfdf5",
            corner_radius=10,
            height=40,
            command=self.toggle_mouse
        )
        self.btn_toggle_mouse.pack(side="left", padx=8, pady=10, expand=True, fill="x")

        # Botón 3: Modo Tony Stark (Copilot)
        self.btn_toggle_stark = ctk.CTkButton(
            btn_bar,
            text=t("btn_stark_on", self.current_lang) if self.tony_stark_mode else t("btn_stark_off", self.current_lang),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0f2b1d" if self.tony_stark_mode else "#18201a",
            hover_color="#1b4530",
            text_color="#34d399" if self.tony_stark_mode else "#94a3b8",
            corner_radius=10,
            height=40,
            command=self.toggle_stark
        )
        self.btn_toggle_stark.pack(side="left", padx=8, pady=10, expand=True, fill="x")

        # Botón 4: Modo Dos Manos
        self.btn_toggle_two_hands = ctk.CTkButton(
            btn_bar,
            text=t("btn_two_hands_on", self.current_lang) if self.two_hands_mode else t("btn_two_hands_off", self.current_lang),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0f2b1d" if self.two_hands_mode else "#18201a",
            hover_color="#1b4530",
            text_color="#34d399" if self.two_hands_mode else "#94a3b8",
            corner_radius=10,
            height=40,
            command=self.toggle_two_hands
        )
        self.btn_toggle_two_hands.pack(side="left", padx=8, pady=10, expand=True, fill="x")

        # Botón 5: Sonido
        self.btn_toggle_sound = ctk.CTkButton(
            btn_bar,
            text=t("btn_sound_on", self.current_lang) if self.sound_enabled else t("btn_sound_off", self.current_lang),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#162b20",
            hover_color="#224232",
            text_color="#a7f3d0",
            corner_radius=10,
            height=40,
            command=self.toggle_sound
        )
        self.btn_toggle_sound.pack(side="left", padx=8, pady=10, expand=True, fill="x")

        # Botón 6: Salir
        btn_exit = ctk.CTkButton(
            btn_bar,
            text=t("btn_exit", self.current_lang),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#881337",
            hover_color="#9f1239",
            text_color="#ffe4e6",
            corner_radius=10,
            height=40,
            command=self.on_close
        )
        btn_exit.pack(side="right", padx=8, pady=10, expand=True, fill="x")

    def get_guide_text(self):
        return "\n".join([
            t("guide_move", self.current_lang),
            t("guide_left_click", self.current_lang),
            t("guide_right_click", self.current_lang),
            t("guide_scroll", self.current_lang),
            t("guide_drag", self.current_lang),
            t("guide_stark", self.current_lang),
            t("guide_two_hands", self.current_lang)
        ])

    def on_language_change(self, selected_display):
        for code, display in SUPPORTED_LANGUAGES:
            if display == selected_display:
                self.current_lang = code
                self.cfg["language"] = code
                save_config(self.cfg)
                self.apply_language()
                break

    def apply_language(self):
        """Actualiza todas las cadenas de texto visibles al nuevo idioma."""
        self.title(f"{t('app_title', self.current_lang)} • Ignaciobrenas")
        self.title_label.configure(text=t("app_title", self.current_lang))
        self.author_label.configure(text=t("author_tag", self.current_lang))
        self.welcome_title_lbl.configure(text=t("welcome_title", self.current_lang))
        self.welcome_author_badge.configure(text=t("welcome_badge", self.current_lang))
        self.welcome_desc_lbl.configure(text=t("welcome_desc", self.current_lang))
        self.guide_text_lbl.configure(text=self.get_guide_text())
        self.btn_start.configure(text=t("btn_start", self.current_lang))
        self.ph_title_lbl.configure(text=t("ph_title", self.current_lang))
        self.ph_desc_lbl.configure(text=t("ph_desc", self.current_lang))

        # Botones
        self.btn_toggle_preview.configure(
            text=t("btn_hide_preview", self.current_lang) if self.show_preview else t("btn_show_preview", self.current_lang)
        )
        self.btn_toggle_mouse.configure(
            text=t("btn_pause_mouse", self.current_lang) if self.enable_mouse else t("btn_resume_mouse", self.current_lang)
        )
        self.btn_toggle_stark.configure(
            text=t("btn_stark_on", self.current_lang) if self.tony_stark_mode else t("btn_stark_off", self.current_lang)
        )
        self.btn_toggle_two_hands.configure(
            text=t("btn_two_hands_on", self.current_lang) if self.two_hands_mode else t("btn_two_hands_off", self.current_lang)
        )
        self.btn_toggle_sound.configure(
            text=t("btn_sound_on", self.current_lang) if self.sound_enabled else t("btn_sound_off", self.current_lang)
        )
        self.update_status_badge()

    def start_tracking(self):
        if self.app_started:
            return

        self.app_started = True
        self.enable_mouse = True

        self.welcome_card.place_forget()
        self.video_label.pack(expand=True, fill="both", padx=10, pady=10)
        self.action_label.place(relx=0.03, rely=0.04)

        self.status_badge.configure(text=t("status_connecting", self.current_lang), fg_color="#78350f", text_color="#fde68a")
        self.update_idletasks()

        if sys.platform.startswith("win"):
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.status_badge.configure(text=t("status_no_cam", self.current_lang), fg_color="#7f1d1d", text_color="#fca5a5")
            self.video_label.configure(
                text="❌ Cámara no disponible. Verifica que la webcam esté conectada.",
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
            self.btn_toggle_preview.configure(text=t("btn_hide_preview", self.current_lang))
            self.placeholder_frame.pack_forget()
            self.video_label.pack(expand=True, fill="both", padx=10, pady=10)
            self.action_label.place(relx=0.03, rely=0.04)
        else:
            self.btn_toggle_preview.configure(text=t("btn_show_preview", self.current_lang))
            self.video_label.pack_forget()
            self.action_label.place_forget()
            self.placeholder_frame.pack(expand=True, fill="both")
        self.update_status_badge()

    def toggle_mouse(self):
        if not self.app_started:
            return
        self.enable_mouse = not self.enable_mouse
        if self.enable_mouse:
            self.btn_toggle_mouse.configure(text=t("btn_pause_mouse", self.current_lang), fg_color="#047857")
        else:
            self.btn_toggle_mouse.configure(text=t("btn_resume_mouse", self.current_lang), fg_color="#b45309")
        self.update_status_badge()

    def toggle_stark(self):
        self.tony_stark_mode = not self.tony_stark_mode
        self.cfg["tony_stark_mode"] = self.tony_stark_mode
        save_config(self.cfg)
        self.btn_toggle_stark.configure(
            text=t("btn_stark_on", self.current_lang) if self.tony_stark_mode else t("btn_stark_off", self.current_lang),
            fg_color="#0f2b1d" if self.tony_stark_mode else "#18201a",
            text_color="#34d399" if self.tony_stark_mode else "#94a3b8"
        )

    def toggle_two_hands(self):
        self.two_hands_mode = not self.two_hands_mode
        self.cfg["two_hands_mode"] = self.two_hands_mode
        save_config(self.cfg)
        self.btn_toggle_two_hands.configure(
            text=t("btn_two_hands_on", self.current_lang) if self.two_hands_mode else t("btn_two_hands_off", self.current_lang),
            fg_color="#0f2b1d" if self.two_hands_mode else "#18201a",
            text_color="#34d399" if self.two_hands_mode else "#94a3b8"
        )
        self.hand_tracker.max_hands = 2 if self.two_hands_mode else 1
        self.hand_tracker.hands = self.hand_tracker.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2 if self.two_hands_mode else 1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.cfg["sound_enabled"] = self.sound_enabled
        save_config(self.cfg)
        self.btn_toggle_sound.configure(
            text=t("btn_sound_on", self.current_lang) if self.sound_enabled else t("btn_sound_off", self.current_lang)
        )

    def update_status_badge(self):
        if not self.app_started:
            self.status_badge.configure(text=t("status_waiting", self.current_lang), fg_color="#13251c", text_color="#94a3b8")
        elif not self.enable_mouse:
            self.status_badge.configure(text=t("status_paused", self.current_lang), fg_color="#451a03", text_color="#fdba74")
        elif self.show_preview:
            self.status_badge.configure(text=t("status_tracking", self.current_lang), fg_color="#064e3b", text_color="#34d399")
        else:
            self.status_badge.configure(text=t("status_hidden", self.current_lang), fg_color="#78350f", text_color="#fde68a")

    def update_loop(self):
        if not self.running or not self.app_started:
            return

        if self.cap is None or not self.cap.isOpened():
            self.status_badge.configure(text=t("status_no_cam", self.current_lang), fg_color="#7f1d1d", text_color="#fca5a5")
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

            # Detección de manos (1 o 2)
            all_hands = self.hand_tracker.find_all_hands(frame, draw=self.show_preview)

            primary_landmarks = None
            secondary_landmarks = None

            if len(all_hands) > 0:
                primary_landmarks = all_hands[0]["landmarks"]
            if len(all_hands) > 1 and self.two_hands_mode:
                secondary_landmarks = all_hands[1]["landmarks"]

            # --- 1. EVALUAR MODO TONY STARK (COPILOT) ---
            stark_triggered = False
            if self.tony_stark_mode and primary_landmarks:
                if self.stark.check_and_trigger(primary_landmarks):
                    stark_triggered = True
                    self.action_label.configure(text=t("action_copilot", self.current_lang), fg_color="#0f3b26", text_color="#6ee7b7")

            # --- 2. CONTROL DE MOUSE CON MANO PRINCIPAL ---
            if primary_landmarks and len(primary_landmarks) > 20 and not stark_triggered:
                index_x, index_y = primary_landmarks[8][1], primary_landmarks[8][2]
                thumb_x, thumb_y = primary_landmarks[4][1], primary_landmarks[4][2]
                middle_x, middle_y = primary_landmarks[12][1], primary_landmarks[12][2]

                gesture_type, g_data = self.gesture.detect_gesture(primary_landmarks)

                if self.enable_mouse:
                    if gesture_type == "MOVE":
                        self.mouse.move_mouse(index_x, index_y, w, h)
                        self.action_label.configure(text=t("action_moving", self.current_lang), fg_color="#0d1f16", text_color="#34d399")
                    elif gesture_type == "LEFT_CLICK":
                        self.mouse.click()
                        if self.sound_enabled:
                            play_click_sound()
                        self.action_label.configure(text=t("action_left_click", self.current_lang), fg_color="#064e3b", text_color="#34d399")
                    elif gesture_type == "RIGHT_CLICK":
                        self.mouse.right_click()
                        if self.sound_enabled:
                            play_click_sound()
                        self.action_label.configure(text=t("action_right_click", self.current_lang), fg_color="#78350f", text_color="#fde047")
                    elif gesture_type == "DRAG_START":
                        self.mouse.mouse_down()
                        if self.sound_enabled:
                            play_action_sound()
                        self.action_label.configure(text=t("action_dragging", self.current_lang), fg_color="#7f1d1d", text_color="#fca5a5")
                    elif gesture_type == "DRAGGING":
                        self.mouse.move_mouse(index_x, index_y, w, h)
                        self.action_label.configure(text=t("action_dragging", self.current_lang), fg_color="#7f1d1d", text_color="#fca5a5")
                    elif gesture_type == "DRAG_STOP":
                        self.mouse.mouse_up()
                        self.action_label.configure(text=t("action_drag_drop", self.current_lang), fg_color="#0d1f16", text_color="#94a3b8")
                    elif gesture_type == "SCROLL_UP":
                        self.mouse.scroll(self.cfg.get("scroll_speed", 20))
                        self.action_label.configure(text=t("action_scroll_up", self.current_lang), fg_color="#14291e", text_color="#a7f3d0")
                    elif gesture_type == "SCROLL_DOWN":
                        self.mouse.scroll(-self.cfg.get("scroll_speed", 20))
                        self.action_label.configure(text=t("action_scroll_down", self.current_lang), fg_color="#14291e", text_color="#a7f3d0")

            # --- 3. GESTOS CON SEGUNDA MANO (MODO DOS MANOS) ---
            if secondary_landmarks and len(secondary_landmarks) > 20 and self.two_hands_mode and self.enable_mouse:
                sec_index_y = secondary_landmarks[8][2]
                sec_thumb_y = secondary_landmarks[4][2]
                # Scroll rápido con la segunda mano moviendo el índice
                if hasattr(self, "prev_sec_y") and self.prev_sec_y is not None:
                    delta_sec = self.prev_sec_y - sec_index_y
                    if abs(delta_sec) > 6:
                        self.mouse.scroll(int(delta_sec * 3))
                        self.action_label.configure(text=t("two_hands_scroll", self.current_lang), fg_color="#1e3a2b", text_color="#6ee7b7")
                self.prev_sec_y = sec_index_y
            else:
                self.prev_sec_y = None

            # --- 4. RENDERIZADO VISUAL PROFESIONAL EN TONOS VERDES ---
            if self.show_preview:
                # Recuadro delimitador en verde oscuro sutil
                margin = self.mouse.margin
                cv2.rectangle(frame, (margin, margin), (w - margin, h - margin), (22, 46, 33), 1)

                # Si está activo Tony Stark, dibujar HUD en la palma
                if self.tony_stark_mode and primary_landmarks and len(primary_landmarks) > 9:
                    palm_cx = (primary_landmarks[0][1] + primary_landmarks[9][1]) // 2
                    palm_cy = (primary_landmarks[0][2] + primary_landmarks[9][2]) // 2
                    cv2.circle(frame, (palm_cx, palm_cy), 22, (110, 231, 183), 2)
                    cv2.circle(frame, (palm_cx, palm_cy), 8, (16, 185, 129), cv2.FILLED)

                # Resaltar puntas de dedos mano principal (verde esmeralda)
                if primary_landmarks and len(primary_landmarks) > 20:
                    for f_idx in [4, 8, 12, 16, 20]:
                        fx, fy = primary_landmarks[f_idx][1], primary_landmarks[f_idx][2]
                        cv2.circle(frame, (fx, fy), 7, (52, 211, 153), cv2.FILLED)
                    # Diana de puntero en el índice
                    ix, iy = primary_landmarks[8][1], primary_landmarks[8][2]
                    cv2.circle(frame, (ix, iy), 14, (16, 185, 129), 2)

                # Si hay segunda mano, resaltar en ámbar sutil
                if secondary_landmarks and len(secondary_landmarks) > 20:
                    for f_idx in [4, 8, 12, 16, 20]:
                        fx, fy = secondary_landmarks[f_idx][1], secondary_landmarks[f_idx][2]
                        cv2.circle(frame, (fx, fy), 7, (245, 158, 11), cv2.FILLED)

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                container_w = self.preview_container.winfo_width()
                disp_w = max(500, min(660, container_w - 30 if container_w > 50 else 640))
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

# Dynamic language switcher dropdown integrated
