import ctypes
import logging
import platform


def is_running_as_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except (AttributeError, OSError):
        logging.exception("Nie udalo sie sprawdzic uprawnien administratora.")
        return False


def get_system_info():
    return {
        "is_admin": is_running_as_admin(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
    }
