import setuptools

from say import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tts-say",
    version=__version__,
    author="Danny Waser",
    author_email="danny@waser.tech",
    description="echo but with TTS.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/waser-technologies/technologies/say",
    project_urls={
        "Documentation": "https://gitlab.com/waser-technologies/technologies/say/blob/main/README.md",
        "Code": "https://gitlab.com/waser-technologies/technologies/say",
        "Issue tracker": "https://gitlab.com/waser-technologies/technologies/say/issues",
    },
    packages=setuptools.find_packages('.'),
    python_requires=">=3.7,<4",
    install_requires = [
        # 'simpleaudio',
        'pydub',
        # 'num2words',
        'websockets',
        'fastapi',
        # 'sanic',
        'toml',
        'myshell-openvoice', # using upstream for pypi but on py312 you need to use my custom fork on branch py312
        # 'myshell-openvoice @ git+https://github.com/wasertech/OpenVoice.git@py312', #use upstream once #250 is merged
        # https://github.com/myshell-ai/OpenVoice/pull/250
        'melotts', # using upstream for pypi but on py312 you need to use my custom fork on branch py312
        # 'melotts @ git+https://github.com/wasertech/MeloTTS.git@py312', #use upstream once #143 is merged
        # https://github.com/myshell-ai/MeloTTS/pull/143
    ],
    entry_points={
        'console_scripts': [
            'say = say.entry_points.run_say:run',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
