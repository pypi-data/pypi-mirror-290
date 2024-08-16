import os, sys
import io
# import glob
import logging
# import json
# import re
import tempfile
import torch
import soundfile as sf, librosa
import numpy as np
from pydub import AudioSegment

from timeit import default_timer as timer

# import TTS Model
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from openvoice.mel_processing import spectrogram_torch
try:
    from melo.api import TTS as MeloTTS
except ImportError:
    os.system("python -m unidic download")
    from melo.api import TTS as MeloTTS

# from num2words import num2words

from say import ASSISTANT_PATH, MODEL_PATH, I18N
from say.TTS import utils

# class ToneConverter(ToneColorConverter):
    
#     def convert_audio(self, audio_in, src_se, tgt_se, output_path=None, tau=0.3, message=None):
#         hps = self.hps
#         # load audio
#         # audio, sample_rate = librosa.load(audio_src_path, sr=hps.data.sampling_rate)
#         audio_in = torch.tensor(audio_in).float()
        
#         with torch.no_grad():
#             y = torch.FloatTensor(audio_in).to(self.device)
#             y = y.unsqueeze(0)
#             spec = spectrogram_torch(y, hps.data.filter_length,
#                                     hps.data.sampling_rate, hps.data.hop_length, hps.data.win_length,
#                                     center=False).to(self.device)
#             spec_lengths = torch.LongTensor([spec.size(-1)]).to(self.device)
#             audio_out = self.model.voice_conversion(spec, spec_lengths, sid_src=src_se, sid_tgt=tgt_se, tau=tau)[0][
#                         0, 0].data.cpu().float().numpy()
#             if message:
#                 audio_out = self.add_watermark(audio_out, message)
#             if output_path is None:
#                 return audio_out
#             else:
#                 sf.write(output_path, audio_out, hps.data.sampling_rate)

def load_models(ckpt_base_path, language, speaker, ckpt_version=2.0):
    """
    Loads TTS models in memory.
    Returns: [toneconverter, synthesizer, source_se]
    """
    
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    ckpt_path = os.path.join(ckpt_base_path, 'checkpoints' if ckpt_version == 1.0 else f'checkpoints_v{int(ckpt_version):d}')
    ckpt_converter = os.path.join(ckpt_path, 'converter')
    config_filepath = os.path.join(ckpt_converter, 'config.json')
    ckpt_filepath = os.path.join(ckpt_converter, 'checkpoint.pth')
    
    if not os.path.exists(ckpt_path):
        logging.warning(f"Checkpoint path {ckpt_path} does not exist. Downloading...")
        utils.manager.download_checkpoints(ckpt_base_path)
        assert os.path.exists(ckpt_path), f"Checkpoint path {ckpt_path} does not exist."
        assert os.path.exists(ckpt_converter), f"Checkpoint converter path {ckpt_converter} does not exist."
        assert os.path.exists(config_filepath), f"Config file {config_filepath} does not exist."
        assert os.path.exists(ckpt_filepath), f"Checkpoint file {ckpt_filepath} does not exist."
    
    logging.debug(f"Checkpoint path has been found at {ckpt_path}.")
    
    toneconverter_load_start = timer()
    toneconverter = ToneColorConverter(config_filepath, device=device)
    toneconverter.load_ckpt(ckpt_filepath)
    toneconverter_load_end = timer() - toneconverter_load_start
    
    logging.debug("Loaded tone converter in %0.3fs." % (toneconverter_load_end))

    model_load_start = timer()
    synthesizer = MeloTTS(language=language, device=device)
    model_load_end = timer() - model_load_start
    
    logging.debug("Loaded synthesizer in %0.3fs." % (model_load_end))

    sse_load_start = timer()
    # if speaker not in list(synthesizer.hps.data.spk2id.keys()):
    #     raise ValueError(f"Speaker {speaker} not found in synthesizer.\n{list(synthesizer.hps.data.spk2id.keys())}")
    # speaker_key = speaker.lower().replace('_', '-')
    source_se = torch.load(os.path.join(ckpt_path, f'base_speakers/ses/{speaker}.pth'), map_location=device)
    sse_load_end = timer() - sse_load_start
    
    logging.debug("Loaded speaker encoder in %0.3fs." % (sse_load_end))

    return [toneconverter, synthesizer, source_se]


class TTS:

    def __init__(self, toneconverter, synthesizer, source_se):
        self.toneconverter = toneconverter
        self.synthesizer = synthesizer
        self.source_se = source_se

    def get_tone_color(self, path_to_ref):
        print(f"{path_to_ref=}")
        target_se, audio_name = se_extractor.get_se(path_to_ref, self.toneconverter, vad=False, target_dir=f"{MODEL_PATH}/processed_se/")
        return target_se, audio_name

    # def fetch_floats_from_str(self, text):
    #     l = []
    #     for t in text.split():
    #         try:
    #             l.append(float(t))
    #         except ValueError:
    #             pass
    #     return l

    # def convert_num2words(self, sentences: str, language: str):
    #     """Convert numbers to words

    #     Args:
    #         sentences (str): text to convert
    #         language (str): language to use for num2word conversion

    #     Returns:
    #         str: converted text
    #     """
    #     def replace_number(match):
    #         num = match.group(0).replace(',', '.').replace("'", '')
    #         w = num2words(float(num), lang=language)
    #         return w

    #     # Use regular expression to find all numbers in the text
    #     pattern = r"\b\d+(?:[.,']\d+)?\b"
    #     converted_sentences = re.sub(pattern, replace_number, sentences)

    #     print(f"Converted {converted_sentences=}")
    #     return converted_sentences

    def get_speaker_id(self, speaker):
        """Returns speaker id"""
        try:
            return self.synthesizer.hps.data.spk2id[speaker]
        except AttributeError:
            print(f"{self.synthesizer.hps.data.spk2id=}")

    def tts(self, text: str, speaker, style_wav, speed = 1.0):
        # Run TTS
        print(f"{text=}")
        print(f"{speaker=}")
        print(f"{style_wav=}")
        print(f"{speed=}")
        target_se, _ = self.get_tone_color(style_wav)
        speaker_idx = self.get_speaker_id(speaker)
        if not speaker_idx:
            if not speaker in self.synthesizer.hps.data.spk2id.keys():
                raise ValueError(f"Speaker {speaker} not found in synthesizer.\n{list(self.synthesizer.hps.data.spk2id.keys())}")
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                date = np.datetime64('now').__str__()
                wav_path = os.path.join(tmpdir, f"{date}.wav")
                self.synthesizer.tts_to_file(text, speaker_idx, speed=speed, quiet=True, output_path=wav_path)
                out = self.toneconverter.convert(wav_path, src_se=self.source_se, tgt_se=target_se)
        except KeyboardInterrupt:
            sys.exit(1)
        
        return out

    def run(self, text, speaker, style_wav="os"):
        # _t = self.convert_num2words(" ".join(text), language.split("-")[0])
        if isinstance(text, list):
            text = " ".join(text)
        ref_wav = os.path.join(ASSISTANT_PATH, "data", I18N.lower(), "TTS/styles", f"{style_wav}/{style_wav}.wav")
        return self.tts(text, speaker, ref_wav)

class Response:
    def __init__(self, audio_bin):
        self.wav_bytes = audio_bin
    
    def to_bytes(self):
        return self.wav_bytes

class Error:
    def __init__(self, message):
        self.message = message
    
    def to_bytes(self):
        return self.message.encode('utf-8')

if __name__ == "__main__":
    engine = TTS(*load_models(MODEL_PATH, "EN_NEWEST", "en-newest"))
    wav_ndarray = engine.run("Hello, world!", "EN-Newest")
    print(f"{wav_ndarray=}")
    # audio = AudioSegment(data=wav_ndarray, sample_width=2, frame_rate=22050, channels=1)
    # pronounce(audio)