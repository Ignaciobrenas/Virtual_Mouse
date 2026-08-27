import sys
import os

# Asegurar que el paquete virtual_mouse este disponible en el path
project_root = os.path.dirname(os.path.abspath(__file__))
virtual_mouse_dir = os.path.join(project_root, "virtual_mouse")
if virtual_mouse_dir not in sys.path:
    sys.path.insert(0, virtual_mouse_dir)

if __name__ == "__main__":
    if "--cli" in sys.argv:
        from main import main
        main()
    else:
        from gui import launch_gui
        launch_gui()
