from exif import Image
from PIL import Image as PILImage


# read file metadata
def read(path):
    extension = path.split('.')[-1].lower()
    if extension in ['jpg', 'jpeg', 'tiff', 'tif']:
        with open(path, 'rb') as image_file:
            my_image = Image(image_file)
        metadata = my_image.get_all()
    elif extension == 'png':
        with open(path, 'rb') as image_file:
            pil_image = PILImage.open(image_file)
            metadata = pil_image.info
    else:
        raise ValueError("File format not supported")
    return metadata

# edit file metadata
def edit(path, key, new_value):
    with open(path, 'rb') as image_file:
        my_image = Image(image_file)
    my_image.set(key, new_value)
    metadata = my_image.get_all()
    return metadata

# save file with new metadata
def save(path, metadata):
    with open(path, 'rb') as image_file:
        my_image = Image(image_file)
    for key, value in metadata.items():
        my_image.set(key, value)
    with open(path, 'wb') as new_image:
        new_image.write(my_image.get_file())
    return new_image
