from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER  


# read metadata
def read(path):
    audio = MP3(path, ID3=EasyID3)
    metadata = audio.tags
    metadata = [(key, value[0]) for key, value in metadata.items()]
    return metadata

# save file with new set of metadata
def save(path, metadata):
    errors = []
    audio = MP3(path, ID3=EasyID3)
    audio.delete()
    for key, value in metadata:
        try: audio.tags[key] = value
        except: errors.append(key)
    audio.save()
    return errors
