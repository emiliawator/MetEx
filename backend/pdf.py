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
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    for key, value in metadata:
        key = '/' + key
        writer.add_metadata({key: value})
    with open(path, 'wb') as f:
        writer.write(f)
    return
