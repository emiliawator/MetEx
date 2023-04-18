from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER  


# read metadata
def read(path):
    audio = MP3(path, ID3=EasyID3)
    metadata = audio.tags
    return export_data(metadata)

# edit metadata
def edit(path, key, new_value):
    audio = MP3(path, ID3=EasyID3)
    audio.tags[key] = new_value
    metadata = audio.tags
    return export_data(metadata)

# save file with new set of metadata
def save(path, dictionary, datatypes):
    metadata = import_data(dictionary, datatypes)
    audio = MP3(path, ID3=EasyID3)
    audio.delete()
    for key, value in metadata:
        audio.tags[key] = value
    audio.save()
    return audio

# convert metadata into dictionary
def export_data(metadata):
    datatypes = [type(item[0]) for item in metadata.items()]
    data = [(key, value[0]) for key, value in metadata.items()]
    return data, datatypes

# convert from dictionary back to original format with correct data types
def import_data(data, datatypes):
    metadata = [(key, value) for key, value in data]
    for i in range(len(metadata)):
        metadata[i] = (metadata[i][0], datatypes[i](metadata[i][1]))
    return metadata
