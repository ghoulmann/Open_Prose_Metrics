from mutagen.mp3 import MP3
from gtts import gTTS
from os import path, remove
class TTS:
    def __init__(self, plaintext, path_to_file):
        self.speech = gTTS(plaintext, lang='en')
        self.filename = path_to_file
        # with open(self.filename, 'wb') as f:
        #     self.speech.write_to_fp(f)
        self.speech.save(self.filename)
        self.basename = path.basename(self.filename)
    def mp3Confirm(self):
        if path.isfile(self.filename):
            return self.filename
    def mp3Delete(self):
        if path.isfile(self.filename):
            remove(self.filename)
            return path.isfile(self.filename)
    def getMp3Length(self):
        audiofile = MP3(self.filename)
        return audiofile.info.length / 60
