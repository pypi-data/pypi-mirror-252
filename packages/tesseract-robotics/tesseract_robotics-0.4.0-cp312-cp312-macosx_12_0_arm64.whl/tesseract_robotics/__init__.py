def _tesseract_dll_path_():
    import sys
    import os
    if sys.platform == "win32" and sys.version_info[:2] >= (3, 8):
        tesseract_env_path = os.environ.get("TESSERACT_PYTHON_DLL_PATH",None)
        if tesseract_env_path:
            for p in tesseract_env_path.split(os.pathsep):
                os.add_dll_directory(p)

_tesseract_dll_path_()
del _tesseract_dll_path_
