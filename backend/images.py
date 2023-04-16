from exif import Image


# read file metadata
def read(path):
    with open(path, 'rb') as image_file:
        my_image = Image(image_file)
    metadata = my_image.get_all()
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
