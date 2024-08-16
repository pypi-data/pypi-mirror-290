import os
# import asyncio
import urllib.request
import requests
import re
# import json
import toml
# import logging
# import threading
import subprocess
import tempfile
import zipfile
import shutil

from tqdm import tqdm
# from pathlib import Path
# from python_shell import Shell
# from python_shell.util.streaming import decode_stream
# from TTS.utils.manage import ModelManager

from say import CONFIG_PATH, ASSISTANT_PATH, I18N, OS_KERNEL, IS_ROOT
from say import __version__

class InvalidVersionError(Exception):
    
    def __init__(self, version, available_versions):
        message = f"Invalid checkpoint version: {version} is not in {available_versions}."
        super().__init__(message)

class ModelManager:
    """
    OpenVoice Checkpoints Manager.
    """
    
    base_url = "https://myshell-public-repo-hosting.s3.amazonaws.com/openvoice/checkpoints_{file_ver}.zip"
    
    checkpoints_url = {
        '1.0': base_url.format(file_ver="1226"),
        '2.0': base_url.format(file_ver="v2_0417")
    }
    
    available_versions = [
        1.,
        2.
    ]
    
    def __init__(self, version: float) -> None:
        if version not in self.available_versions:
            raise InvalidVersionError(version, self.available_versions)
        self.version = version
    
    def download_checkpoints(self, checkpoint_path, chunk_size=128):
        os.makedirs(checkpoint_path, exist_ok=True)
        checkpoint_url = self.checkpoints_url.get(f"{self.version:.1f}")
        if not checkpoint_url:
            raise Exception(f"Invalid version: {self.version}; Could not find checkpoint url.")
        
        zip_name = checkpoint_url.split("/")[-1]
        checkpoint_dirname = "checkpoints" if self.version == 1.0 else f"checkpoints_v{int(self.version):d}"
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = os.path.join(tmp_dir, zip_name)
            
            r = requests.get(checkpoint_url, stream=True, timeout=60)
            total_size = int(r.headers.get('content-length', 0))
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
            with open(zip_path, 'wb') as zip_file:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    zip_file.write(chunk)
                    progress_bar.update(len(chunk))
                progress_bar.close()
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(tmp_dir, checkpoint_dirname))
            shutil.move(os.path.join(tmp_dir, checkpoint_dirname, checkpoint_dirname), os.path.join(checkpoint_path, checkpoint_dirname))

manager = ModelManager(2.0)

def hide_windir(dir_path):
    import ctypes
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ret = ctypes.windll.kernel32.SetFileAttributesW(dir_path, FILE_ATTRIBUTE_HIDDEN)
    
    return True if ret else False

def get_config_or_default():
    # Check if conf exist

    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as cfg:
            CONFIG = toml.loads(cfg.read())
    else:
        CONFIG = {
            'service': {
                'host': '0.0.0.0',
                'port': '5067'
            },
            'tts': {
                'models': "openvoice_v2",
                'language': I18N,
                'speaker_wav': f"{ASSISTANT_PATH}/data/{I18N}/TTS/styles/default.wav",
                'is_allowed': False
            }
        }
        os.path.mkdirs(os.path(CONFIG_PATH).parent, exist_ok=True)
        if OS_KERNEL == "Windows" and not IS_ROOT:
            # On Windows adding a . to the beginning of a folder name will not hide it.
            # So we use the SetFileAttributesW function to hide the folder.
            hide_windir(os.path(CONFIG_PATH).parent.as_posix().replace('/', '\\'))

        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(toml.dumps(CONFIG))
    
    return CONFIG

def download_speaker(output_file, lang="en", gender="male", name="default"):
    default_speaker = f"https://gitlab.com/waser-technologies/data/tts/{lang}/voices/-/raw/master/{gender}/{name}.wav"
    urllib.request.urlretrieve(default_speaker, output_file)
    return output_file

def get_speaker(idx=None, wav=None, conf=get_config_or_default()):
    # Get a speaker id or speaker wav
    speaker_id = None
    speaker_wav = None

    if idx:
        speaker_id = idx[0]
    elif wav:
        speaker_wav = wav[0]
    elif conf.get('tts'):
        speaker_id = conf['tts'].get('speaker_id', None)
        speaker_wav = conf['tts'].get('speaker_wav', None)
    
    return speaker_id, speaker_wav

def get_models_name(model_name=None, conf=get_config_or_default()):
    """
    Makes sure Config represent loaded models name.
    """
    _tts_conf = conf.get('tts', None)
    if _tts_conf:
        _tts_models_name = _tts_conf.get('models', None)
        if _tts_models_name:
            if model_name != _tts_models_name:
                conf['tts']['models'] = model_name
                os.path.mkdir(os.path(CONFIG_PATH).parent, exist_ok=True)
                with open(CONFIG_PATH, 'w') as f:
                    f.write(toml.dumps(conf))
    return model_name

def is_allowed_to_speak(conf=get_config_or_default()):
    _tts_conf = conf.get('tts', False)
    if _tts_conf:
        return _tts_conf.get('is_allowed', False)
    return False

# def get_loc_model_path():
#     """
#     Get localised models path.
#     """
#     # __TTS_file__ = "~/.local/share/tts/"
#     return f"{HOME}/.local/tts/.models.json"

# manager = ModelManager()

def echo(text="", show_version=False, enable_interpretation=False, disable_interpretation=True, no_newline=False, end="\n", flush=True):
    if text:
        # if enable_interpretation:
        #     e = Shell.echo('-e', text)
        # else:
        #     e = Shell.echo(text)
    
        # p = decode_stream(e.output)
        if no_newline is True and "\n" in end:
            end = end.replace("\n", "")
        elif no_newline is False and "\n" not in end:
            end += "\n"
        print(text, end=end, flush=flush)
        return text

def get_available_cpu_count():
    """Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program
    See this https://stackoverflow.com/a/1006301/13561390"""

    # cpuset
    # cpuset may restrict the number of *available* processors
    try:
        m = re.search(r"(?m)^Cpus_allowed:\s*(.*)$", open("/proc/self/status").read())
        if m:
            res = bin(int(m.group(1).replace(",", ""), 16)).count("1")
            if res > 0:
                return res
    except IOError:
        pass

    # Python 2.6+
    try:
        import multiprocessing

        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # https://github.com/giampaolo/psutil
    try:
        import psutil

        return psutil.cpu_count()  # psutil.NUM_CPUS on old versions
    except (ImportError, AttributeError):
        pass

    # POSIX
    try:
        res = int(os.sysconf("SC_NPROCESSORS_ONLN"))

        if res > 0:
            return res
    except (AttributeError, ValueError):
        pass

    # Windows
    try:
        res = int(os.environ["NUMBER_OF_PROCESSORS"])

        if res > 0:
            return res
    except (KeyError, ValueError):
        pass

    # jython
    try:
        from java.lang import Runtime

        runtime = Runtime.getRuntime()
        res = runtime.availableProcessors()
        if res > 0:
            return res
    except ImportError:
        pass

    # BSD
    try:
        sysctl = subprocess.Popen(["sysctl", "-n", "hw.ncpu"], stdout=subprocess.PIPE)
        scStdout = sysctl.communicate()[0]
        res = int(scStdout)

        if res > 0:
            return res
    except (OSError, ValueError):
        pass

    # Linux
    try:
        res = open("/proc/cpuinfo").read().count("processor\t:")

        if res > 0:
            return res
    except IOError:
        pass

    # Solaris
    try:
        pseudoDevices = os.listdir("/devices/pseudo/")
        res = 0
        for pd in pseudoDevices:
            if re.match(r"^cpuid@[0-9]+$", pd):
                res += 1

        if res > 0:
            return res
    except OSError:
        pass

    # Other UNIXes (heuristic)
    try:
        try:
            dmesg = open("/var/run/dmesg.boot").read()
        except IOError:
            dmesgProcess = subprocess.Popen(["dmesg"], stdout=subprocess.PIPE)
            dmesg = dmesgProcess.communicate()[0]

        res = 0
        while "\ncpu" + str(res) + ":" in dmesg:
            res += 1

        if res > 0:
            return res
    except OSError:
        pass

    raise Exception("Can not determine number of CPUs on this system")

