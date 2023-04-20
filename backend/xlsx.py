from openpyxl import load_workbook
from datetime import datetime

def read(filepath):
    wb = load_workbook(filepath)
    prop = wb.properties

    metadata = []
    
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

    
    # for d in dir(wb.properties):
    #     if not d.startswith('_'):
    #         val = getattr(prop, d)
    #         metadata.append(tuple((d,val)))
    #         print(tuple((d,val)))
    return metadata

def save(metadata, filepath, newfilepath, datatypes):
    wb = load_workbook(filepath)
    prop = wb.properties
    notuplelist = [list(i) for i in metadata]

    i = 0
    for item in notuplelist:
        if item[0] == "created" or item[0] == "lastPrinted" or item[0] == "modified":
            if notuplelist[i][1] != "None":
                    notuplelist[i][1] = datetime.strptime(notuplelist[i][1], "%Y-%m-%d %H:%M:%S")
            else: # if None by default
                i+=1 
                continue
            setattr(prop, item[0], (notuplelist[i][1]))
        else:
            setattr(prop, item[0], (notuplelist[i][1]))
        i += 1

    wb.save(newfilepath)