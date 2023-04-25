# xlsx extension
from openpyxl import load_workbook
from datetime import datetime

def read(filepath):
    try:
        wb = load_workbook(filepath)
        prop = wb.properties
    except:
        return "Supplied filepath is invalid"

    metadata = []
    
    # str if not date
    metadata.append(tuple(("category", prop.category)))
    metadata.append(tuple(("contentStatus", prop.contentStatus)))
    metadata.append(tuple(("created", prop.created))) #date
    metadata.append(tuple(("creator", prop.creator)))
    metadata.append(tuple(("description", prop.description)))
    metadata.append(tuple(("identifier", prop.identifier)))
    metadata.append(tuple(("keywords", prop.keywords)))
    metadata.append(tuple(("language", prop.language)))
    metadata.append(tuple(("lastModifiedBy", prop.lastModifiedBy)))
    metadata.append(tuple(("lastPrinted", prop.lastPrinted))) #date
    metadata.append(tuple(("modified", prop.modified))) #date
    metadata.append(tuple(("revision", prop.revision)))
    metadata.append(tuple(("subject", prop.subject)))
    metadata.append(tuple(("title", prop.title)))
    metadata.append(tuple(("version", prop.version)))

    return metadata

def save(metadata, filepath, newfilepath):
    try:
        wb = load_workbook(filepath)
        prop = wb.properties
    except:
        return "Supplied filepath is invalid"
    
    notuplelist = [list(i) for i in metadata]

    for item in notuplelist:
        if item[0] == "created" or item[0] == "lastPrinted" or item[0] == "modified": # datetime type
            if item[1] != "None":
                    try:
                        item[1] = datetime.strptime(item[1], "%Y-%m-%d %H:%M:%S")
                    except:
                        return "Correct date format must be supplied: \n %Y-%m-%d %H:%M:%S"
            else: # if None by default
                continue
            try:
                setattr(prop, item[0], item[1])
            except:
                return "An error occured while saving {} field".format(item[0])
        else:
            try:
                setattr(prop, item[0], item[1])
            except:
                return "An error occured while saving {} field".format(item[0])
    try:
        wb.save(newfilepath)
    except:
        return "Supplied filepath is invalid"