import os
import sys

# Ensure the frontend folder is on sys.path so we can import app.py there
project_root = os.path.dirname(__file__)
frontend_path = os.path.join(project_root, "frontend")
if frontend_path not in sys.path:
    sys.path.insert(0, frontend_path)

try:
    import app as frontend_app  # loads frontend/app.py
except Exception as e:
    raise RuntimeError(f"Failed to import frontend/app.py: {e}")

# Call the main() entrypoint from frontend.app
if hasattr(frontend_app, "main"):
    frontend_app.main()
else:
    raise RuntimeError("frontend.app has no main() entrypoint")
