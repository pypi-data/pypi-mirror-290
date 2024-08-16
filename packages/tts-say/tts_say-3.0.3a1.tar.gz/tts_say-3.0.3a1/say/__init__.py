import os, platform

__version__ = "3.0.3a1"

class UnsupportedOSError(Exception):
    """Unsupported OS Exception"""
    def __init__(self, os_name):
        self.os_name = os_name
        super().__init__(f"Unsupported OS: {os_name}")

try:
    I18N, L10N = (x for x in os.environ.get('LANG', "en_EN.UTF-8").split(".")[0].split("_"))
except ValueError as e:
    I18N, L10N = ("en", "EN")

OS_KERNEL = platform.system()
USERNAME = os.environ.get("USERNAME", 'root')

if OS_KERNEL in ["Linux", "Darwin", "FreeBSD"]:
    IS_ROOT = os.geteuid() == 0
elif OS_KERNEL == "Windows":
    import ctypes
    IS_ROOT = ctypes.windll.shell32.IsUserAnAdmin() != 0
else:
    raise UnsupportedOSError(OS_KERNEL)

if IS_ROOT and OS_KERNEL == "Windows":
    HOME = "C:\\ProgramData"
    ASSISTANT_PATH = os.path.join(HOME, "Assistant")
elif OS_KERNEL == "Windows":
    HOME = os.path.expanduser("~")
    ASSISTANT_PATH = os.path.join(HOME, ".assistant")
else:
    if IS_ROOT:
        HOME = "/root"
        ASSISTANT_PATH = "/usr/share/assistant"
    else:
        HOME = os.path.expanduser("~")
        ASSISTANT_PATH = os.path.join(HOME, ".assistant")

CONFIG_PATH = os.path.join(ASSISTANT_PATH, "tts.toml")
MODEL_PATH = os.path.join(ASSISTANT_PATH, "models", "multi", "TTS")
