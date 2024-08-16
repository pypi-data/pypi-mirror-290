# Say: echo but with TTS

Say uses [OpenVoice v2](https://github.com/myshell-ai/OpenVoice) to create convincing voices for TTS application.

## Installation

```zsh
pip install tts-say
# Or from source
pip install git+https://gitlab.com/waser-technologies/technologies/say.git
```

## Usage

```zsh
❯ say Hello World
Hello World

❯ say --help
usage: say [-h] [-n] [-e] [-E] [-v] [-L LANG] [--out_path OUT_PATH]
           [--debug DEBUG]
           [text ...]

Same as echo but with Text-To-Speech.

positional arguments:
  text                  Text to be said.

options:
  -h, --help            show this help message and exit
  -n, --n               do not output the trailing newline
  -e, --e               enable interpretation of backslash escapes
  -E, --E               disable interpretation of backslash escapes (default)
  -v, --version         output version information and exit
  -L LANG, --lang LANG  Language to be spoken (default: $LANG)
  --out_path OUT_PATH   Output wav file path.
  --debug DEBUG         true to enable debug mode.
```

### Start the server

First you need to load the models in memory.

To do so, start the TTS server using `say` without any `text` argument.

```
say [--debug DEBUG]
No attribute `text`.
say --help
For more information.
Starting server now.
Please wait.
...
```

Or enable its service.

```
cp ./speak.service.example /usr/lib/systemd/user/speak.service
systemctl --user enable --now speak.service
```

#### Get authorization to speak

You need to authorize the system to speak first. Change the service configuration as follows.

```toml
# ~/.assistant/tts.toml
...
[tts]
is_allowed = true
...
```

Then [start the server](#start-the-server) and use `say` with some `text` argument to [say something](#use-the-client).

### Use the client

Before you use the client, make sure :
  1. the system has a valid [authorization to speak](#get-authorization-to-speak), 
  2. the server has correctly loaded the models,
  3. if the server has loaded `YourTTS` (by default); you need to [create a `style_wav` file of your default speaker](#setup-your-own-voice-yourtts-only).


```zsh
say [-n] [-e] [-E] [-v] [-L LANG] [--out_path OUT_PATH] [text ...]

❯ say --version
Say: version 3.0.1a2
Copyright © 2024, Danny Waser
Say, version 3.0.1a2.
...

❯ say Hello, this is a test
Hello, this is a test
```

### Save the audio

To save the resulted speech, use the argument `--out_path`.

```zsh
❯ say "Bonjour." --out_path "say_output.wav"
Bonjour.
❯ soxi say_output.wav

Input File     : 'say_output.wav'
Channels       : 1
Sample Rate    : 16000
Precision      : 16-bit
Duration       : 00:00:01.17 = 18726 samples ~ 87.7781 CDDA sectors
File Size      : 37.5k
Bit Rate       : 256k
Sample Encoding: 16-bit Signed Integer PCM
```

## Setup your own voice

Before saying anything, you need to add a wav file to `~/.assistant/data/${lang}/TTS/styles/${voice_name}/${voice_name}.wav`.

Where `$lang` is your target language (_i.e_ _`en`_, _`fr`_, _etc._) and `$voice_name` is the name of your voice.

This wav file must contain between 5 and 15 seconds of speech.

Make sure it matches with your `tts.toml` configuration. (_i.e_ `voice_name`)


### _Don't want to hunt down a voice?_

Checkout my [collection of high quality TTS voices](https://gitlab.com/waser-technologies/data/tts/en/voices) generated using TTS VTCK/VITS models. 

### Audio samples
<audio src="https://gitlab.com/waser-technologies/data/tts/en/voices/-/raw/master/female/default.wav?inline=false" controls preload></audio>
![](img/default_female.wav)

<audio src="https://gitlab.com/waser-technologies/data/tts/en/voices/-/raw/master/male/default.wav?inline=false" controls preload></audio>
![](img/default_male.wav)

<audio src="https://gitlab.com/waser-technologies/data/tts/en/voices/-/raw/master/female/default_2.wav?inline=false" controls preload></audio>
![](img/default_female_2.wav)

## Yes yes but echo is for text right ?

Yes but you should be able to `alias` `echo` to `say` inside your favorite shell.

Because when you think about it, asking your computer to `say something` is like asking it to `echo something`.

Both cases output `something`.

Where echo repeat what it got in stdin, say as an injonction is used to ask someone to repeat what comes after.

Like so :
```
❯ Assistant, say Hello.
[Assistant] Hello.
```