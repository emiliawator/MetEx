from exif import Image
from PIL import Image as PILImage

# read file metadata
def read(path):
    extension = path.split('.')[-1].lower()
    if extension in ['jpg', 'jpeg', 'tiff', 'tif']:
        with open(path, 'rb') as image_file:
            exif_image = Image(image_file)
        metadata = exif_image.get_all()
    elif extension == 'png':
        with open(path, 'rb') as image_file:
            pil_image = PILImage.open(image_file)
        metadata = pil_image.info
    else:
        raise ValueError("File format not supported")
    metadata = [(key, value) for key, value in metadata.items()]
    return metadata

# save file with new metadata
def save(path, metadata):
    extension = path.split('.')[-1].lower()
    if extension in ['jpg', 'jpeg', 'tiff', 'tif']:
        with open(path, 'rb') as image_file:
            exif_image = Image(image_file)
        # for key in my_image.get_all():
        #     my_image.delete(key)
        excluded_tags = ['exif_version']
        for key, value in metadata:
            try: value = eval(value)
            except: value = str(value)
            print(key, value, type(value))
            if key not in excluded_tags:
                try: exif_image.set(key, value)
                except: pass
        with open(path, 'wb') as new_image:
            new_image.write(exif_image.get_file())
    elif extension == 'png':
        with PILImage.open(path) as pil_image:
            for key, value in metadata:
                try: value = eval(value)
                except: value = str(value)
                pil_image.info[key] = value
            pil_image.save(path, "PNG")
    else:
        raise ValueError("File format not supported")
    return
