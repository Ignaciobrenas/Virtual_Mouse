# 🖱️ AI Virtual Mouse / Ratón Virtual Inteligente

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/CustomTkinter-Modern%20UI-blue?style=for-the-badge" alt="CustomTkinter" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/MediaPipe-00A67E?style=for-the-badge&logo=google&logoColor=white" alt="MediaPipe" />
  <img src="https://img.shields.io/badge/PyAutoGUI-F7931E?style=for-the-badge" alt="PyAutoGUI" />
  <img src="https://img.shields.io/badge/Author-Ignaciobrenas-black?style=for-the-badge&logo=github" alt="Author" />
</p>

<p align="center">
  <b>🌐 Idioma / Language:</b><br>
  <a href="#-español"><b>Español</b></a> •
  <a href="#-english"><b>English</b></a>
</p>

---

## 🇪🇸 Español

### 📌 Sobre el Proyecto

**Virtual Mouse** es un sistema profesional de control gestual sin contacto físico desarrollado en **Python**. Combina visión por computadora en tiempo real mediante **OpenCV**, estimación de articulaciones de la mano con **MediaPipe**, automatización del ratón con **PyAutoGUI** y una interfaz de usuario moderna basada en **CustomTkinter**.

> 💡 **Nota del Desarrollador:**
> Este es un **proyecto personal desarrollado por Ignaciobrenas** concebido para practicar, investigar y profundizar en el aprendizaje de **Python**, ingeniería de visión artificial, arquitecturas basadas en ramas y commits profesionales, y diseño de interfaces gráficas reactivas.

---

### ✨ Características Principales

- 🚀 **Pop-up de Bienvenida Integrado:** Pantalla inicial elegante con el título del proyecto y firma de autoría de **Ignaciobrenas**.
- 🖐️ **Rastreo de 21 Puntos de la Mano:** Landmarks con código de color dinámico en tiempo real para cada dedo.
- 🎯 **Control Multigesto:**
  - 👆 **Movimiento del cursor:** Desplazamiento suave guiado por el dedo índice.
  - 🤏 **Clic Izquierdo:** Pellizco entre pulgar e índice con debounce inteligente.
  - ✌️ **Clic Derecho:** Pellizco entre pulgar y dedo medio.
  - 📜 **Scroll Vertical:** Dos dedos levantados juntos (índice y medio) para navegar arriba/abajo.
  - ✊ **Arrastrar y Soltar (Drag & Drop):** Mantén el pellizco más de 0.5s para arrastrar ventanas o elementos y suelta cuando quieras colocarlos.
- 🔊 **Feedback Auditivo Háptico:** Sonidos de clic sutiles configurables con un botón de la interfaz.
- ⚡ **FPS en Vivo:** Monitorización en tiempo real del rendimiento de la cámara y el modelo.
- 👁️ **Alternar Vista Previa:** Muestra u oculta la imagen de la cámara con un clic para ahorrar recursos del sistema mientras el ratón sigue activo.
- 🖱️ **Pausa de Emergencia / Calibración:** Pausa el control del ratón con un solo botón para usar el ratón físico sin cerrar el programa.
- 🧪 **Suite de Pruebas Unitarias:** Cobertura de tests automatizados con `unittest`.

---

### 🎮 Guía de Gestos y Controles

| Gesto / Control | Acción | Descripción |
| :--- | :--- | :--- |
| ☝️ **Dedo Índice** | **Mover Cursor** | Mueve el dedo índice para desplazar el ratón. |
| 🤏 **Pellizco (Índice + Pulgar)** | **Clic Izquierdo** | Clic izquierdo con confirmación visual `"CLICK!"`. |
| ✌️ **Pellizco (Medio + Pulgar)** | **Clic Derecho** | Dispara menú contextual o clic secundario. |
| 📜 **Índice + Medio Arriba** | **Scroll Vertical** | Mueve la mano arriba/abajo para desplazar la pantalla. |
| ✊ **Mantener Pellizco (>0.5s)** | **Arrastrar y Soltar** | Arrastra ventanas, carpetas o selecciones. |
| 🔊 **Botón "Sonido"** | **Alternar Audio** | Activa o silencia el feedback sonoro de clic. |
| 👁️ **Botón "Vista Previa"** | **Alternar Cámara** | Oculta la vista de cámara para ahorrar consumo. |
| 🛑 **Botón "Salir"** | **Cerrar App** | Cierra la aplicación y libera el dispositivo de cámara. |

---

### 📂 Estructura del Proyecto

```text
Virtual_Mouse/
│
├── virtual_mouse/
│   ├── __init__.py           # Paquete de la aplicación
│   ├── gui.py                # Interfaz gráfica moderna (CustomTkinter)
│   ├── main.py               # Bucle alternativo de ejecución por terminal (CLI)
│   ├── hand_tracking.py      # Tracking y landmarks con MediaPipe
│   ├── mouse_controller.py   # Control, suavizado y acciones con PyAutoGUI
│   ├── gesture_control.py    # Motor multigesto (clic, derecho, scroll, drag)
│   ├── sound.py              # Feedback sonoro no bloqueante
│   ├── config.py             # Configuración persistente en JSON
│   └── requirements.txt      # Dependencias del paquete
│
├── tests/
│   ├── __init__.py
│   ├── test_gesture_control.py
│   └── test_config.py
│
├── run.py                    # Script de entrada principal
├── start.bat                 # Lanzador automático para Windows (doble clic)
├── requirements.txt          # Dependencias del repositorio
├── .gitignore                # Reglas de exclusión de Git
└── README.md                 # Documentación bilingüe
```

---

### 🚀 Instalación y Puesta en Marcha

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/Ignaciobrenas/Virtual_Mouse.git
cd Virtual_Mouse
```

#### 2. Entorno Virtual
```powershell
# En Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### 4. Ejecutar la Aplicación
- **Opción recomendada (Doble clic):** Ejecuta [`start.bat`](start.bat) o escribe en la consola:
  ```powershell
  .\start.bat
  ```
- **Desde Python:**
  ```bash
  python run.py
  ```
- **Ejecutar Pruebas Unitarias:**
  ```bash
  python -m unittest discover tests
  ```

---

<br>

## 🇬🇧 English

### 📌 About the Project

**Virtual Mouse** is a touchless, gesture-controlled mouse system developed in **Python**. It combines real-time computer vision via **OpenCV**, deep learning hand tracking through **MediaPipe**, operating system mouse automation with **PyAutoGUI**, and a desktop dashboard created with **CustomTkinter**.

> 💡 **Developer's Note:**
> This is a **personal project designed by Ignaciobrenas** to practice, innovate, and master **Python**, computer vision architectures, professional Git branch workflows, and responsive desktop UI design.

---

### ✨ Key Features

- 🚀 **Integrated Welcome Pop-up:** Features a welcome dashboard acknowledging author credit to **Ignaciobrenas**.
- 🖐️ **21-Point Real-Time Hand Landmark Tracking:** Distinct color-coded points identifying fingertips and finger joints.
- 🎯 **Advanced Multi-Gesture Engine:**
  - 👆 **Cursor Motion:** Smooth, jitter-free cursor gliding guided by index fingertip.
  - 🤏 **Left Click:** Natural pinch between index and thumb fingertips.
  - ✌️ **Right Click:** Pinch between middle finger and thumb.
  - 📜 **Vertical Scroll:** Raise both index and middle fingers together to scroll web pages.
  - ✊ **Drag & Drop:** Hold pinch gesture (>0.5s) to engage drag mode; release to drop.
- 🔊 **Audio Haptic Feedback:** Optional subtle click sounds.
- ⚡ **Live FPS Counter:** Real-time diagnostics for video throughput.
- 👁️ **Toggle Camera Preview:** Hide camera feed on demand to save CPU/GPU overhead while mouse control remains active.
- 🖱️ **One-Click Mouse Pause:** Freeze virtual mouse control instantly to interact with physical mouse.
- 🧪 **Automated Unit Testing:** Includes test suite runnable with Python's native `unittest`.

---

### 🎮 Gestures & Controls

| Gesture / Control | Action | Description |
| :--- | :--- | :--- |
| ☝️ **Index Fingertip** | **Move Pointer** | Move index finger across camera frame to move mouse. |
| 🤏 **Index + Thumb Pinch** | **Left Click** | Quick pinch executes a left click with audio/visual feedback. |
| ✌️ **Middle + Thumb Pinch** | **Right Click** | Triggers context menu or secondary click. |
| 📜 **Index + Middle Up** | **Vertical Scroll** | Move hand up or down to scroll page content. |
| ✊ **Hold Pinch (>0.5s)** | **Drag & Drop** | Grabs windows or objects until pinch is released. |
| 🔊 **"Sound" Button** | **Toggle Audio** | Enables or mutes click sound effects. |
| 👁️ **"Preview" Button** | **Toggle Camera** | Toggles live video canvas. |
| 🛑 **"Exit" Button** | **Quit App** | Closes app and releases webcam cleanly. |

---

### 🚀 Getting Started

#### 1. Clone & Setup
```bash
git clone https://github.com/Ignaciobrenas/Virtual_Mouse.git
cd Virtual_Mouse
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### 2. Run
```powershell
.\start.bat
# or
python run.py
```

#### 3. Run Tests
```bash
python -m unittest discover tests
```

---

## 🛠️ Tech Stack / Tecnologías

- **[Python](https://www.python.org/)** (v3.10+) - Core programming language
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Modern UI framework
- **[OpenCV](https://opencv.org/)** - Video capture and computer vision
- **[MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide)** - Hand landmark tracking
- **[PyAutoGUI](https://pyautogui.readthedocs.io/)** - Mouse and keyboard automation
- **[Pillow](https://python-pillow.org/)** - Real-time image buffering
- **[NumPy](https://numpy.org/)** - Vector math and coordinate interpolation

---

## 👤 Author / Autor

- **Ignaciobrenas**
  - Personal portfolio / Proyecto personal de aprendizaje en Python y Computer Vision.
