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
    return export_data(metadata)

# edit file metadata
def edit(path, key, new_value):
    with open(path, 'rb') as image_file:
        my_image = Image(image_file)
    my_image.set(key, new_value)
    metadata = my_image.get_all()
    return metadata

# save file with new metadata
def save(path, metadata, datatypes):
    with open(path, 'rb') as image_file:
        my_image = Image(image_file)
    for key in my_image.get_all():
        my_image.delete(key)
    # metadata = import_data(data, datatypes)
    for key, value in metadata:
        my_image.set(key, value)
    with open(path, 'wb') as new_image:
        new_image.write(my_image.get_file())
    return export_data(new_image)

# convert metadata into dictionary
def export_data(metadata):
    datatypes = [type(item[0]) for item in metadata.items()]
    data = [(key, value) for key, value in metadata.items()]
    return data, datatypes

# convert from dictionary back to original format with correct data types
def import_data(data, datatypes):
    metadata = [(key, value) for key, value in data]
    for i in range(len(metadata)):
        metadata[i] = (metadata[i][0], datatypes[i](metadata[i][1]))
    return metadata
