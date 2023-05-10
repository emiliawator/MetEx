from PyPDF2 import PdfReader, PdfWriter


# read file metadata
def read(path):
    reader = PdfReader(path)
    metadata = reader.metadata
    metadata = [(key, value) for key, value in metadata.items()]
    for i in range(len(metadata)):
        metadata[i] = (metadata[i][0].replace('/', ''), metadata[i][1])
    return metadata

# save file with new metadata
def save(path, metadata):
    errors = []
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    for key, value in metadata:
        key = '/' + key
        try: writer.add_metadata({key: value})
        except: errors.append(key)
    with open(path, 'wb') as f:
        writer.write(f)
    return errors

# erase metadata
def erase(path):
    errors = []
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    metadata = reader.metadata
    metadata = [(key, value) for key, value in metadata.items()]
    print(metadata)
    for key, value in metadata:
        try: writer.add_metadata({key: ''})
        except: errors.append(key)
    with open(path, 'wb') as f:
        writer.write(f)
    return errors