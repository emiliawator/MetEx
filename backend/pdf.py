from PyPDF2 import PdfReader, PdfWriter


# read file metadata
def read(path):
    reader = PdfReader(path)
    metadata = reader.metadata
    return metadata

# edit file metadata
def edit(path, key, new_value):
    reader = PdfReader(path)
    metadata = reader.metadata
    metadata[key] = new_value
    return metadata

# save file with new metadata
def save(path, metadata):
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata(metadata)
    with open(path, 'wb') as f:
        writer.write(f)
    return f
