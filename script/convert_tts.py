#!python

from gtts import gTTS
import sys

file_path = sys.argv[1]
out_file = sys.argv[2]

out_file_name = out_file + ".mp3"

with open(file_path, 'r') as file:
    file_content = file.read()

language = 'en'
tts = gTTS(text=file_content, lang=language, slow=False)

tts.save(out_file_name)