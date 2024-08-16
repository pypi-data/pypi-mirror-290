import os
import json

import websockets # not websocket!!!
import asyncio

import re
from datetime import date
from pydub import AudioSegment #, playback
# from num2words import num2words

from say import __version__, playback
from say.TTS import utils


# from TTS import __version__ as __TTS_version__

HOST, PORT = "localhost", "5067"
CONFIG = utils.get_config_or_default()

if CONFIG.get('service'):
    HOST = CONFIG['service'].get('host', HOST)
    PORT = CONFIG['service'].get('port', PORT)

playback_engine = playback.PlaybackEngine()

# def pronounce(wav):
    # pydub.playback.play(wav)
    
    # audio_playback = simpleaudio.play_buffer(
    #     wav.raw_data,
    #     num_channels= wav.channels,
    #     bytes_per_sample= wav.sample_width,
    #     sample_rate= wav.frame_rate
    # )
    # audio_playback.wait_done()
    
    # playback_engine.add_audio_segment(wav)

async def tts(text: str, language, speaker, style_wav="os", host=HOST, port=PORT, save_output=None):
    async with websockets.connect(f"ws://{host}:{port}/api/v1/tts") as ws:
        try:
            j = {
                'text': text,
                'speaker': speaker,
                'style_wav': style_wav,
                'language': language
                }
            await ws.send(json.dumps(j).encode('utf-8', 'ignore'))
            wav = await ws.recv()
            
            # check if wav is an error
            try:
                wav = json.loads(wav)
                if wav.get('error'):
                    raise Exception(wav['error'])
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
            
            try:
                _wav = AudioSegment(data=wav)
                playback_engine.add_audio_segment(_wav)
                if save_output:
                    # Check if the file already exists
                    if os.path.exists(save_output):
                        # Load the file as an AudioSegment
                        _save_output_wav = AudioSegment.from_file(save_output)
                        # Concatenate the two AudioSegments
                        _save_output_wav = _save_output_wav + _wav
                        # Export the concatenated AudioSegment
                        _save_output_wav.export(save_output, format="wav")
                    else:
                        _wav.export(save_output, format="wav")
                # try:
                #     playback_engine.wait_done()
                # except KeyboardInterrupt:
                #     playback_engine.stop()
            except Exception as e:
                # raise Exception(e)
                pass
        except ConnectionRefusedError as e:
            pass
        except Exception:
            # raise e
            pass
        # finally:
        #     await ws.close()

def split_sentences(text: str) -> list[str]:
    """
    Splits text into sentences.
    """
    _text = text.replace("\n", "\n|")
    _text = _text.replace("! ", "!| ")
    _text = _text.replace("? ", "?| ")
    _text = _text.replace(". ", ".| ")
    # _text = _text.replace(", ", ",| ") # Use with caution
    _text = _text.replace("; ", ";| ")
    _text = _text.replace(": ", ":| ")
    _text = _text.replace("(", "|(")
    _text = _text.replace(")", ")|")
    _text = _text.replace("[", "|[")
    _text = _text.replace("]", "]|")
    _text = _text.replace("{", "|{")
    _text = _text.replace("}", "}|")
    # if you find a number that is
    # seprated by spaces or commas (8,847), 
    # remove the spaces and commas (8847)
    _text = re.sub(r'(\d+)[,]+(\d+)', r'\1\2', _text)
    return _text.split("|")
    

async def _say(text: list[str], language: str, speaker: str, style_wav: str = CONFIG['tts'].get('speaker_wav', "os"), save_output: str = "", show_version: bool = False, enable_interpretation: bool = True, disable_interpretation: bool = False, no_newline: bool = False) -> list[str]:
    # lang = 'EN_NEWEST' if language == 'en' else language.upper()
    # speaker = 'en-newest' if speaker == 'en' else language.lower()
    # if style_wav and not os.path.exists(style_wav):
    #     utils.download_speaker(style_wav)
    
    for _text in text:
        t = split_sentences(_text)
        for _t in t:
            utils.echo(text=_t, show_version=show_version, enable_interpretation=enable_interpretation, disable_interpretation=disable_interpretation, no_newline=True)
            try:
                await tts([_t,], language, speaker, style_wav=style_wav, save_output=save_output)
            except (ConnectionRefusedError, OSError) as e:
                pass # Server is not active or something
            except Exception as e:
                raise e
        if no_newline:
            utils.echo(text="", show_version=show_version, enable_interpretation=enable_interpretation, disable_interpretation=disable_interpretation, no_newline=False)
        try:
            playback_engine.wait_done()
        except KeyboardInterrupt:
            playback_engine.stop()
    return text

# def inflect_version(version, lang, dot="dot"):
#     """
#     Uses `num2words` to inflect version numbers to say.
#     """
#     Major, Minor, Bugs = version.split(".")
#     _maj = num2words(int(Major), lang=lang)
#     _min = num2words(int(Minor), lang=lang)
#     _b = num2words(int(Bugs), lang=lang)

#     return f"{_maj} {dot}, {_min} {dot}, {_b}"

def say_version(lang):
    if lang == "en":
        _text = [
            f"Say, version {__version__}.",
        ]
        language = "en"
    elif lang == "fr":
        _text = [
            f"Dit, version {__version__}.",
        ]
        language = "fr"
    else:
        _text = None
        language = lang.lower()
    #     raise NotImplementedError(f"Language {lang} not implemented.")
    
    # _show_version = True
    _enable_interpretation = True
    _disable_interpretation = False
    _no_newline = False
    utils.echo(f"Say: version {str(__version__)}", show_version=False, enable_interpretation=_enable_interpretation, disable_interpretation=_disable_interpretation, no_newline=_no_newline)
    utils.echo(f"Copyright © {str(date.today().year)}, Danny Waser", show_version=False, enable_interpretation=_enable_interpretation, disable_interpretation=_disable_interpretation, no_newline=_no_newline)

    if _text is not None:
        asyncio.run(_say(_text, language, "EN-Newest" if lang.lower() == "en" else lang.upper(), style_wav="os", show_version=False, enable_interpretation=_enable_interpretation, disable_interpretation=_disable_interpretation, no_newline=_no_newline))
    # asyncio.run(_say(_text, language, speaker_idx=speaker_idx, style_wav=style_wav, show_version=False, enable_interpretation=_enable_interpretation, disable_interpretation=_disable_interpretation, no_newline=_no_newline))
