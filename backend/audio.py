from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER  


# read metadata
def read(path):
    audio = MP3(path, ID3=EasyID3)
    metadata = audio.tags
    return metadata

# edit metadata
def edit(path, key, new_value):
    audio = MP3(path, ID3=EasyID3)
    audio.tags[key] = new_value
    metadata = audio.tags
    return metadata

# save file with new metadata
def save(path, metadata):
    audio = MP3(path, ID3=EasyID3)
    for key, value in metadata.items():
        audio.tags[key] = value
    audio.save()
    return audio
