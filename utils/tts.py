# utils/tts.py
from gtts import gTTS
import os
import tempfile
import platform

def speak_text(text):
    tts = gTTS(text)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp.name)
    if platform.system() == "Windows":
        os.system(f"start {temp.name}")
    else:
        os.system(f"xdg-open {temp.name}")
