from PyPDF2 import PdfReader, PdfWriter


# read file metadata
def read(path):
    reader = PdfReader(path)
    metadata = reader.metadata
    return export_data(metadata)

# edit file metadata
def edit(path, key, new_value):
    reader = PdfReader(path)
    metadata = reader.metadata
    metadata[key] = new_value
    return metadata

# save file with new metadata
def save(path, metadata, datatypes):
    # metadata = import_data(data, datatypes)
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata(metadata)
    with open(path, 'wb') as f:
        writer.write(f)
    return f

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
