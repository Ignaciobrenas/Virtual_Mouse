# 🖱️ AI Virtual Mouse / Ratón Virtual Inteligente

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-10b981?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/CustomTkinter-Emerald%20Dark-047857?style=for-the-badge" alt="CustomTkinter" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/MediaPipe-00A67E?style=for-the-badge&logo=google&logoColor=white" alt="MediaPipe" />
  <img src="https://img.shields.io/badge/PyAutoGUI-F7931E?style=for-the-badge" alt="PyAutoGUI" />
  <img src="https://img.shields.io/badge/Autor-Ignaciobrenas-064e3b?style=for-the-badge&logo=github" alt="Autor" />
</p>

---

## Sobre el Proyecto

**Virtual Mouse** es un sistema profesional de interacción gestual sin contacto físico desarrollado en **Python**. Combina visión artificial con **OpenCV**, rastreo de articulaciones con **MediaPipe**, control del cursor con **PyAutoGUI** y una interfaz moderna y minimalista basada en **CustomTkinter** con una paleta en tonos verde bosque y esmeralda.

> 💡 **Nota del Desarrollador:**
> Proyecto personal desarrollado por **Ignacio Breñas Muñoz** concebido para investigar y dominar **Python**, visión por computadora en tiempo real, ingeniería de interfaces de usuario minimalistas y flujos profesionales en Git.

---

## Características Principales

- 🪟 **Interfaz Minimalista Verde Oscuro:** Diseño sobrio, profesional y sin distracciones, utilizando *CustomTkinter* con estética dark emerald.
- 🖐️ **Rastreo Óptico con MediaPipe:** Detección de 21 puntos anatómicos de la mano en tiempo real con alta tasa de cuadros por segundo.
- 🎯 **Control Preciso del Puntero:** Mapeo suavizado del dedo índice a las coordenadas de la pantalla con filtros de amortiguación para eliminar vibraciones.
- 👆 **Gestos Táctiles Virtuales:**
  - **Clic Izquierdo:** Unir las yemas de los dedos índice y pulgar (pellizco corto).
  - **Clic Derecho:** Unir las yemas de los dedos corazón y pulgar.
  - **Doble Clic:** Dos toques rápidos consecutivos entre índice y pulgar.
  - **Arrastrar y Soltar (Drag & Drop):** Mantener el pellizco entre índice y pulgar.
  - **Scroll:** Desplazamiento vertical levantando índice y corazón juntos.

---

## Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/Ignaciobrenas/Virtual_Mouse.git
cd Virtual_Mouse

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Lanzar la aplicación
python src/main.py
```

---

## Estructura del Código

```
Virtual_Mouse/
├── src/
│   ├── main.py               # Punto de entrada de la aplicación y ciclo de ejecución
│   ├── gui.py                # Interfaz gráfica CustomTkinter
│   ├── hand_tracker.py       # Módulo de visión artificial MediaPipe y OpenCV
│   └── controller.py         # Mapeo de gestos a acciones del ratón (PyAutoGUI)
├── assets/                   # Iconos e imágenes de demostración
└── requirements.txt          # Dependencias del proyecto
```

---

## Licencia

Distribuido bajo la **Licencia MIT**.
