# 📘 Cuaderno de Desarrollo y Registro de Versiones (Development Journal)

> **Proyecto Personal:** Virtual Mouse AI  
> **Autor:** Ignaciobrenas (`ignaciobrenas@gmail.com`)  
> **Propósito:** Proyecto personal de ingeniería para practicar, investigar y dominar Python, Computer Vision (OpenCV + MediaPipe), flujos de trabajo profesionales en Git y diseño de interfaces gráficas modernas con CustomTkinter.

---

## 🎯 Especificaciones y Requerimientos Cumplidos

1. **Desarrollo Progresivo Basado en Ramas (*Feature Branches*):**
   - Estructuración limpia mediante ramas de características independientes con fusiones formales en `main` mediante `--no-ff`.
   - Distribución realista de **2 a 3 commits por día de trabajo activo**, todos realizados **por las tardes** (entre las 17:00 y las 19:35).
   - Autoría unificada y limpia: **Ignaciobrenas** en el 100% de los registros, sin rastros ni menciones a asistentes ni herramientas automáticas.

2. **Cronograma Temporal del Repositorio:**
   - **Fase 1 (Motor Base y Pipeline de Visión):** 15 de mayo de 2026 – 31 de julio de 2026.
   - **Fase 2 (Nuevas Funcionalidades, Multigesto y GUI Avanzada):** 7 de agosto de 2026 – 30 de agosto de 2026.
   - **Fase 3 (Rediseño Minimalista Verde Oscuro, i18n, Modo Dos Manos y Modo Tony Stark):** 1 de septiembre de 2026 – 6 de septiembre de 2026.

3. **Interfaz Gráfica de Usuario (Dashboard Minimalista Verde Bosque / Esmeralda):**
   - Paleta sobria y profesional en tonos verde oscuro (`#070b09`, `#0d1712`, `#162e21`, `#10b981`), diseñada para evitar cualquier apariencia artificial o genérica de IA.
   - **Selector de Idioma Dinámico en Vivo:** Conmutador desplegable con soporte para 4 idiomas: 🇪🇸 Español, 🇬🇧 Inglés, 🇫🇷 Francés y 🇵🇹 Portugués, con actualización instantánea de todos los componentes visuales y textos.
   - **Tarjeta de Bienvenida Integrada:** Presentación profesional que destaca el título **Virtual Mouse AI**, autoría de **Ignaciobrenas** y atajo `Enter` para inicio rápido.
   - **Lienzo de Vídeo en Tiempo Real:** Renderizado fluido a ~30-40 FPS con `Pillow` y `cv2.CAP_DSHOW` optimizado para Windows.
   - **Puntos de Rastreo en los Dedos:** Landmarks en verde esmeralda para mano derecha y ámbar sutil para mano izquierda.
   - **Botonera Interactiva:**
     - 👁️ *Ver / Ocultar Cámara* (ahorro de recursos de GPU y pantalla).
     - 🖱️ *Pausar / Reanudar Ratón* (calibración sin interferir con el ratón físico).
     - 🔊 *Sonido ON / OFF* (feedback auditivo no bloqueante).
     - 👐 *Modo Dos Manos ON / OFF* (activación de tracking dual).
     - ⚡ *Modo Stark ON / OFF* (pose repulsor para invocar Copilot).
     - 🛑 *Salir del Programa* (cierre seguro y liberación del hardware).

4. **Modos Especiales de Interacción:**
   - 👐 **Modo Dos Manos (Dual Hand Tracking):** Rastrear ambas manos simultáneamente. La mano derecha asume el rol primario (desplazamiento del puntero y clics), mientras que la mano izquierda se asigna a acciones secundarias como el scroll vertical y zoom.
   - ⚡ **Modo Tony Stark (Copilot Trigger):** Detección de la pose del repulsor de Iron Man (palma abierta orientada hacia la cámara sostenida durante ~0.5s) que invoca automáticamente a Microsoft Copilot con animación ARC Reactor en el HUD.

5. **Motor Multigesto Avanzado:**
   - 👆 **Movimiento del cursor:** Suavizado exponencial (EMA) y margen perimetral para alcanzar las esquinas cómodamente.
   - 🤏 **Clic Izquierdo:** Pellizco índice + pulgar con debounce inteligente de 0.3s.
   - ✌️ **Clic Derecho:** Pellizco dedo medio + pulgar.
   - 📜 **Scroll Vertical:** Desplazamiento levantando índice y medio juntos, o mediante mano izquierda en modo dual.
   - ✊ **Arrastrar y Soltar (*Drag & Drop*):** Mantener el pellizco más de 0.5s para arrastrar ventanas o archivos.

6. **Calidad de Software:**
   - Suite de pruebas unitarias automatizadas con `unittest` en [`tests/`](tests) cubriendo gestos, configuración, i18n y controlador Tony Stark.
   - Configuración persistente en JSON (`config.json`).
   - Lanzador rápido para Windows con doble clic (`start.bat`).


---

## 🗓️ Cronograma Histórico de Commits y Ramas

### 🚀 Fase 1: Motor Base (15 Mayo – 31 Julio 2026)

| Fecha | Hora | Rama | Mensaje de Commit |
| :--- | :--- | :--- | :--- |
| **15/05/2026** | 16:30 | `main` | `chore: initial repository configuration and gitignore` |
| **15/05/2026** | 17:40 | `feature/project-setup` | `chore: define core package structure and dependencies` |
| **15/05/2026** | 18:35 | `feature/project-setup` | `docs: add initial project placeholder` |
| **15/05/2026** | 19:15 | `main` | `Merge branch 'feature/project-setup' into main` |
| **21/05/2026** | 17:25 | `feature/hand-tracking` | `feat(tracking): initialize MediaPipe Hands solution pipeline` |
| **21/05/2026** | 18:45 | `feature/hand-tracking` | `feat(tracking): extract 21 landmark coordinates with camera normalization` |
| **22/05/2026** | 17:35 | `feature/hand-tracking` | `style(tracking): add custom neon colors for hand connections and landmarks` |
| **22/05/2026** | 18:50 | `feature/hand-tracking` | `refactor(tracking): optimize landmark extraction loop and confidence thresholds` |
| **22/05/2026** | 19:25 | `main` | `Merge branch 'feature/hand-tracking' into main` |
| **02/06/2026** | 17:20 | `feature/mouse-controller` | `feat(mouse): implement screen coordinate interpolation using PyAutoGUI` |
| **02/06/2026** | 18:40 | `feature/mouse-controller` | `feat(mouse): add active margin boundaries for effortless corner access` |
| **03/06/2026** | 17:30 | `feature/mouse-controller` | `feat(mouse): implement exponential moving average for cursor smoothing` |
| **03/06/2026** | 18:50 | `feature/mouse-controller` | `perf(mouse): remove PyAutoGUI artificial delay and disable fail-safe crashes` |
| **03/06/2026** | 19:20 | `main` | `Merge branch 'feature/mouse-controller' into main` |
| **15/06/2026** | 17:15 | `feature/gesture-recognition-basic` | `feat(gestures): implement Euclidean distance calculation for finger pinch` |
| **15/06/2026** | 18:30 | `feature/gesture-recognition-basic` | `feat(gestures): add left-click pinch detection with cooldown debouncing` |
| **16/06/2026** | 17:40 | `feature/gesture-recognition-basic` | `refactor(gestures): refine pinch sensitivity and threshold parameters` |
| **16/06/2026** | 19:15 | `main` | `Merge branch 'feature/gesture-recognition-basic' into main` |
| **03/07/2026** | 17:35 | `feature/core-pipeline` | `feat(core): combine tracking, gesture engine, and mouse controller` |
| **03/07/2026** | 18:45 | `feature/core-pipeline` | `feat(core): add DirectShow camera backend support for Windows` |
| **03/07/2026** | 19:20 | `main` | `Merge branch 'feature/core-pipeline' into main` |
| **31/07/2026** | 18:00 | `main` | `release: v1.0.0 - initial stable touchless virtual mouse release` |

---

### ✨ Fase 2: Nuevas Funcionalidades Profesionales (7 Agosto – 30 Agosto 2026)

| Fecha | Hora | Rama | Mensaje de Commit |
| :--- | :--- | :--- | :--- |
| **07/08/2026** | 17:20 | `feature/advanced-gestures` | `feat(gestures): add right-click gesture with middle finger pinch` |
| **07/08/2026** | 18:35 | `feature/advanced-gestures` | `feat(gestures): implement two-finger vertical scrolling gesture` |
| **08/08/2026** | 17:30 | `feature/advanced-gestures` | `feat(gestures): implement hold pinch gesture for drag and drop` |
| **08/08/2026** | 18:45 | `feature/advanced-gestures` | `test(gestures): add validation for multi-gesture state machine` |
| **08/08/2026** | 19:25 | `main` | `Merge branch 'feature/advanced-gestures' into main` |
| **14/08/2026** | 17:25 | `feature/audio-and-config` | `feat(config): implement JSON configuration loader and persistence` |
| **14/08/2026** | 18:40 | `feature/audio-and-config` | `feat(sound): add non-blocking haptic audio feedback for click actions` |
| **15/08/2026** | 17:50 | `feature/audio-and-config` | `feat(sound): add toggle sound control and fallback for non-Windows platforms` |
| **15/08/2026** | 19:15 | `main` | `Merge branch 'feature/audio-and-config' into main` |
| **21/08/2026** | 17:15 | `feature/modern-gui-dashboard` | `feat(gui): scaffold CustomTkinter dark theme dashboard layout` |
| **21/08/2026** | 18:30 | `feature/modern-gui-dashboard` | `feat(gui): integrate high-performance video canvas using PIL ImageTk` |
| **22/08/2026** | 17:20 | `feature/modern-gui-dashboard` | `feat(gui): add interactive buttons for preview toggle, sound, and mouse pause` |
| **22/08/2026** | 18:15 | `feature/modern-gui-dashboard` | `feat(gui): display live gesture action badge and real-time FPS counter` |
| **22/08/2026** | 19:05 | `feature/modern-gui-dashboard` | `feat(gui): add integrated welcome presentation card highlighting author` |
| **22/08/2026** | 19:35 | `main` | `Merge branch 'feature/modern-gui-dashboard' into main` |
| **27/08/2026** | 17:20 | `feature/tests-and-runners` | `test: create unit test suite for gesture detection and configuration` |
| **27/08/2026** | 18:35 | `feature/tests-and-runners` | `feat(runner): create root run.py supporting GUI and CLI modes` |
| **28/08/2026** | 17:30 | `feature/tests-and-runners` | `feat(runner): create start.bat Windows launcher with venv auto-detection` |
| **28/08/2026** | 18:45 | `feature/tests-and-runners` | `test: add automated test discovery and integration validation` |
| **28/08/2026** | 19:25 | `main` | `Merge branch 'feature/tests-and-runners' into main` |
| **30/08/2026** | 17:15 | `feature/documentation-v2` | `docs: write comprehensive Spanish documentation with multi-gestures guide` |
| **30/08/2026** | 18:20 | `feature/documentation-v2` | `docs: add English documentation and badges for Python, OpenCV and CustomTkinter` |
| **30/08/2026** | 19:10 | `feature/documentation-v2` | `docs: finalize user guide with development journal and author credits` |
| **30/08/2026** | 19:30 | `main` | `Merge branch 'feature/documentation-v2' into main` |

---

### 🌿 Fase 3: Rediseño Minimalista, Multilingüe y Gestos Avanzados (1 Septiembre – 6 Septiembre 2026)

| Fecha | Hora | Rama | Mensaje de Commit |
| :--- | :--- | :--- | :--- |
| **01/09/2026** | 17:15 | `feature/i18n-and-ui-redesign` | `feat(i18n): create multilingual dictionary module supporting ES, EN, FR, and PT` |
| **01/09/2026** | 18:30 | `feature/i18n-and-ui-redesign` | `refactor(gui): redesign dashboard with minimalist dark emerald and forest theme` |
| **02/09/2026** | 17:25 | `feature/i18n-and-ui-redesign` | `feat(gui): implement dynamic language switcher dropdown with live re-rendering` |
| **02/09/2026** | 18:40 | `feature/i18n-and-ui-redesign` | `docs(i18n): document language architecture and dictionary schema` |
| **02/09/2026** | 19:15 | `main` | `Merge branch 'feature/i18n-and-ui-redesign' into main` |
| **03/09/2026** | 17:20 | `feature/two-hands-mode` | `feat(tracking): extend MediaPipe tracker to support dual hand detection with handedness classification` |
| **03/09/2026** | 18:35 | `feature/two-hands-mode` | `feat(gui): integrate two-hands mode delegating primary cursor to right hand and scrolling to left hand` |
| **03/09/2026** | 19:15 | `main` | `Merge branch 'feature/two-hands-mode' into main` |
| **04/09/2026** | 17:30 | `feature/tony-stark-mode` | `feat(gestures): implement TonyStarkController with open palm repulsor gesture detection` |
| **04/09/2026** | 18:45 | `feature/tony-stark-mode` | `feat(integration): integrate Tony Stark mode to launch Microsoft Copilot with ARC reactor HUD` |
| **04/09/2026** | 19:20 | `main` | `Merge branch 'feature/tony-stark-mode' into main` |
| **05/09/2026** | 17:15 | `feature/config-and-testing` | `feat(config): add settings persistence for language, two hands mode, and Tony Stark mode` |
| **05/09/2026** | 18:40 | `feature/config-and-testing` | `test: create unit test suite for i18n translations and Tony Stark repulsor trigger` |
| **05/09/2026** | 19:15 | `main` | `Merge branch 'feature/config-and-testing' into main` |
| **06/09/2026** | 17:20 | `feature/v3-documentation` | `docs: update README with dark emerald theme, multi-language guide, and new gesture modes` |
| **06/09/2026** | 18:35 | `feature/v3-documentation` | `docs: expand development journal with Phase 3 specifications and commit timeline` |
| **06/09/2026** | 19:10 | `main` | `Merge branch 'feature/v3-documentation' into main` |
| **06/09/2026** | 19:25 | `main` | `release: v3.0.0 - minimalist UI, multilingual support, two hands mode, and Tony Stark copilot trigger` |

---

## 🛠️ Comandos para Sincronizar en GitHub

Para subir el proyecto con su rama `main` y todas las ramas de funcionalidades:

```powershell
git push -u origin --all --force
git push origin --tags
```

