from exif import Image
from exif import *
from PIL import Image as PILImage

# read file metadata
def read(path):
    extension = path.split('.')[-1].lower()
    if extension in ['jpg', 'jpeg', 'tiff', 'tif']:
        with open(path, 'rb') as image_file:
            exif_image = Image(image_file)
        metadata = exif_image.get_all()
    elif extension == 'png':
        raise ValueError("File format not supported")
    else:
        raise ValueError("File format not supported")
    metadata = [(key, str(value)) for key, value in metadata.items()]
    readonly = find_readonly(path, metadata)
    return metadata, readonly

# find read-only metadata
def find_readonly(path, metadata):
    readonly = []
    extension = path.split('.')[-1].lower()
    if extension in ['jpg', 'jpeg', 'tiff', 'tif']:
        with open(path, 'rb') as image_file:
            exif_image = Image(image_file)
        for key, value in metadata:
            try: value = eval(value)
            except: value = str(value)
            try: exif_image.set(key, value)
            except: readonly.append(key)
        with open(path, 'wb') as new_image:
            new_image.write(exif_image.get_file())
    elif extension == 'png':
        raise ValueError("File format not supported")
    else:
        raise ValueError("File format not supported")
    return readonly

# save file with new metadata
def save(path, metadata, readonly):
    errors = []
    extension = path.split('.')[-1].lower()
    if extension in ['jpg', 'jpeg', 'tiff', 'tif']:
        with open(path, 'rb') as image_file:
            exif_image = Image(image_file)
        for key, value in metadata:
            try: value = eval(value)
            except: value = str(value)
            if key not in readonly:
                try: exif_image.set(key, value)
                except: errors.append(key)
        with open(path, 'wb') as new_image:
            new_image.write(exif_image.get_file())
    elif extension == 'png':
        raise ValueError("File format not supported")
    else:
        raise ValueError("File format not supported")
    return errors

# erase metadata
def erase(path):
    errors = []
    extension = path.split('.')[-1].lower()
    if extension in ['jpg', 'jpeg', 'tiff', 'tif']:
        with open(path, 'rb') as image_file:
            exif_image = Image(image_file)
        metadata = exif_image.get_all()
        metadata = [(key, str(value)) for key, value in metadata.items()]
        for key, value in metadata:
            try: 
                exif_image.set(key, "")
                continue
            except: pass
            try: exif_image.set(key, 0)
            except: errors.append(key)
        with open(path, 'wb') as new_image:
            new_image.write(exif_image.get_file())
    elif extension == 'png':
        raise ValueError("File format not supported")
    else:
        raise ValueError("File format not supported")
    return errors