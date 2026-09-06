# 🖱️ AI Virtual Mouse / Ratón Virtual Inteligente

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-10b981?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/CustomTkinter-Emerald%20Dark-047857?style=for-the-badge" alt="CustomTkinter" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/MediaPipe-00A67E?style=for-the-badge&logo=google&logoColor=white" alt="MediaPipe" />
  <img src="https://img.shields.io/badge/PyAutoGUI-F7931E?style=for-the-badge" alt="PyAutoGUI" />
  <img src="https://img.shields.io/badge/Author-Ignaciobrenas-064e3b?style=for-the-badge&logo=github" alt="Author" />
</p>

<p align="center">
  <b>🌐 Idioma / Language / Langue / Idioma:</b><br>
  <a href="#-español"><b>Español</b></a> •
  <a href="#-english"><b>English</b></a> •
  <a href="#-français"><b>Français</b></a> •
  <a href="#-português"><b>Português</b></a>
</p>

---

## 🇪🇸 Español

### 📌 Sobre el Proyecto

**Virtual Mouse** es un sistema profesional de interacción gestual sin contacto físico desarrollado en **Python**. Combina visión artificial con **OpenCV**, rastreo de articulaciones con **MediaPipe**, control del cursor con **PyAutoGUI** y una interfaz moderna y minimalista basada en **CustomTkinter** con una paleta en tonos verde bosque y esmeralda.

> 💡 **Nota del Desarrollador:**
> Este es un **proyecto personal desarrollado por Ignaciobrenas** concebido para practicar, investigar y dominar **Python**, visión por computadora en tiempo real, ingeniería de interfaces de usuario minimalistas y flujos profesionales en Git.

---

### ✨ Características Principales

- 🪟 **Interfaz Minimalista Verde Oscuro:** Diseño sobrio, profesional y sin distracciones, inspirado en herramientas de ingeniería de software de alto nivel.
- 🌐 **Soporte Multiidioma en Vivo:** Selector instantáneo entre **Español**, **Inglés**, **Francés** y **Portugués**, con persistencia en `config.json`.
- ⚡ **Modo Tony Stark (Copilot):** Realiza el gesto del *Repulsor* de Iron Man (palma abierta al frente) para activar inmediatamente **Microsoft Copilot** con feedback visual de reactor ARC.
- 👐 **Modo Dos Manos (Two Hands Mode):** Rastreo simultáneo de ambas manos. La mano derecha controla el cursor y los clics, mientras la mano izquierda gestiona el scroll vertical dinámico y gestos secundarios.
- 🖐️ **Puntos Visuales Neón:** Visualización en tiempo real de los 21 puntos clave de la mano con verde esmeralda (mano principal) y ámbar (mano secundaria).
- 🎯 **Motor Multigesto de Precisión:**
  - 👆 **Mover cursor:** Suavizado exponencial (EMA) y margen activo para alcanzar bordes fácilmente.
  - 🤏 **Clic Izquierdo:** Pellizco índice + pulgar con debounce inteligente.
  - ✌️ **Clic Derecho:** Pellizco medio + pulgar.
  - 📜 **Scroll:** Dos dedos arriba en mano derecha o movimiento vertical de mano izquierda.
  - ✊ **Arrastrar y Soltar (*Drag & Drop*):** Mantener pellizco > 0.5s para arrastrar ventanas o archivos.
- 🔊 **Feedback Auditivo Háptico:** Clics sonoros sutiles no bloqueantes activables/desactivables.
- 👁️ **Alternar Cámara:** Botón para ocultar la imagen y ahorrar recursos de GPU/CPU manteniendo el control activo.

---

### 🎮 Guía de Gestos

| Gesto | Acción | Descripción |
| :--- | :--- | :--- |
| ☝️ **Dedo Índice** | **Mover Cursor** | Mueve la punta del dedo índice para desplazar el ratón. |
| 🤏 **Pellizco (Índice + Pulgar)** | **Clic Izquierdo** | Clic izquierdo con confirmación visual `"CLICK!"`. |
| ✌️ **Pellizco (Medio + Pulgar)** | **Clic Derecho** | Clic secundario / menú contextual. |
| 📜 **Índice + Medio Arriba** | **Scroll Vertical** | Mueve los dos dedos arriba/abajo para navegar documentos. |
| ✊ **Mantener Pellizco (>0.5s)** | **Arrastrar y Soltar** | Arrastra ventanas o archivos hasta soltar el pellizco. |
| 🖐️ **Palma Abierta al Frente** | **Modo Tony Stark** | Pose de repulsor Iron Man: lanza Microsoft Copilot. |
| 👐 **Segunda Mano (Izquierda)** | **Navegación Dual** | Controla el scroll y navegación mientras la derecha mueve el cursor. |

---

## 🇬🇧 English

### 📌 About the Project

**Virtual Mouse** is a professional touchless gesture control system written in **Python**. It integrates **OpenCV** for camera feed, deep learning hand tracking through **MediaPipe**, OS-level mouse simulation via **PyAutoGUI**, and a desktop interface built with **CustomTkinter** sporting a minimalist forest/emerald green palette.

> 💡 **Developer's Note:**
> This is a **personal project crafted by Ignaciobrenas** to practice, innovate, and master **Python**, computer vision architectures, clean UI design, and production-ready Git workflows.

---

### ✨ Key Features

- 🪟 **Minimalist Dark Green Interface:** Serene, high-focus aesthetic engineered for professional daily use.
- 🌐 **Live Multilingual Engine:** Real-time language switching across **English**, **Spanish**, **French**, and **Portuguese**.
- ⚡ **Tony Stark Mode (Copilot):** Make the iconic Iron Man *Repulsor* pose (open palm facing camera) to instantly launch **Microsoft Copilot** with ARC reactor HUD feedback.
- 👐 **Two Hands Mode:** Track both hands simultaneously. Right hand steers cursor and clicks; left hand drives vertical scrolling and secondary gestures.
- 🎯 **Advanced Multi-Gesture Detection:**
  - 👆 **Cursor Motion:** Exponential moving average filtering for jitter-free tracking.
  - 🤏 **Left Click:** Natural pinch between index and thumb.
  - ✌️ **Right Click:** Pinch between middle finger and thumb.
  - 📜 **Vertical Scroll:** Two fingers raised together.
  - ✊ **Drag & Drop:** Hold pinch (>0.5s) to engage drag mode.
- 🔊 **Haptic Audio Feedback:** Non-blocking auditory click confirmations.
- 🧪 **Automated Test Suite:** Built-in unit test suite covering gesture logic and configurations.

---

## 🇫🇷 Français

### 📌 À propos du Projet

**Virtual Mouse** est un système professionnel de contrôle de la souris sans contact physique développé en **Python**. Il associe la vision par ordinateur avec **OpenCV**, l'estimation des repères de la main avec **MediaPipe**, et une interface minimaliste aux teintes vert émeraude conçue avec **CustomTkinter**.

- **Mode Tony Stark:** Ouvrez la paume vers la caméra pour lancer **Microsoft Copilot**.
- **Mode Deux Mains:** Utilisez les deux mains simultanément pour diriger la souris et faire défiler les pages.
- **Multilingue:** Basculez instantanément entre Français, Anglais, Espagnol et Portugais.
- **Développé par Ignaciobrenas** comme projet personnel d'apprentissage et de perfectionnement en Python.

---

## 🇵🇹 Português

### 📌 Sobre o Projeto

**Virtual Mouse** é um sistema profissional de controle de mouse por gestos touchless em **Python**. Utiliza visão computacional com **OpenCV**, rastreamento com **MediaPipe** e uma interface moderna em verde esmeralda com **CustomTkinter**.

- **Modo Tony Stark:** Abra a palma da mão em direção à câmera para iniciar o **Microsoft Copilot**.
- **Modo Duas Mãos:** Rastreie as duas mãos para controle simultâneo de ponteiro e rolagem.
- **Suporte Multilíngue:** Troca rápida entre Português, Espanhol, Inglês e Francês.
- **Desenvolvido por Ignaciobrenas** como projeto pessoal de prática e aprendizado avançado em Python.

---

### 📂 Estructura del Proyecto / Project Structure

```text
Virtual_Mouse/
│
├── virtual_mouse/
│   ├── __init__.py           # Inicializador del paquete
│   ├── gui.py                # Dashboard minimalista verde oscuro (CustomTkinter)
│   ├── main.py               # Modo de ejecución alternativo por consola (CLI)
│   ├── hand_tracking.py      # Tracking con soporte para 1 o 2 manos (MediaPipe)
│   ├── mouse_controller.py   # Control, suavizado y escalado perimetral (PyAutoGUI)
│   ├── gesture_control.py    # Motor multigesto (clic, derecho, scroll, drag)
│   ├── tony_stark.py         # Controlador de modo Tony Stark (activador Copilot)
│   ├── i18n.py               # Motor de internacionalización (ES, EN, FR, PT)
│   ├── sound.py              # Feedback sonoro no bloqueante
│   ├── config.py             # Configuración persistente en JSON
│   └── requirements.txt      # Dependencias del paquete
│
├── tests/
│   ├── __init__.py
│   ├── test_gesture_control.py
│   ├── test_config.py
│   ├── test_mouse_controller.py
│   └── test_new_features.py  # Tests de i18n y Modo Tony Stark
│
├── run.py                    # Entrada principal de ejecución
├── start.bat                 # Lanzador automático para Windows (doble clic)
├── requirements.txt          # Dependencias en la raíz
├── DEVELOPMENT_JOURNAL.md    # Cuaderno de desarrollo e historial de commits
├── .gitignore                # Archivos ignorados por Git
└── README.md                 # Documentación completa y multilingüe
```

---

### 🚀 Instalación y Puesta en Marcha

```powershell
# 1. Clonar el repositorio
git clone https://github.com/Ignaciobrenas/Virtual_Mouse.git
cd Virtual_Mouse

# 2. Entorno virtual e instalación
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Iniciar la aplicación (Doble clic en start.bat o terminal)
.\start.bat

# 4. Ejecutar tests unitarios
python -m unittest discover tests
```

---

## 👤 Author / Autor

- **Ignaciobrenas** (`ignaciobrenas@gmail.com`)
  - Proyecto personal para el aprendizaje y dominio de Python y Computer Vision.
