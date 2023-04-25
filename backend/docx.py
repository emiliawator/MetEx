# docx extension

# todo - "None" field not supported by datetime type? how to clear date??? (clear all problem)
# save and read method as in xlsx?

import docx
from datetime import datetime

def read(filepath):
    try:
        doc = docx.Document(filepath)
    except:
        return "Supplied filepath is invalid"

    try:
        prop = doc.core_properties
    except: 
        return "An error occured while reading metadata"
                
    metadata = [] # list of tuples

    # str if not date
    metadata.append(tuple(("category", prop.category)))
    metadata.append(tuple(("content_status", prop.content_status)))
    metadata.append(tuple(("created", prop.created))) #date
    metadata.append(tuple(("author", prop.author)))
    metadata.append(tuple(("comments", prop.comments)))
    metadata.append(tuple(("identifier", prop.identifier)))
    metadata.append(tuple(("keywords", prop.keywords)))
    metadata.append(tuple(("language", prop.language)))
    metadata.append(tuple(("last_modified_by", prop.last_modified_by)))
    metadata.append(tuple(("last_printed", prop.last_printed))) #date
    metadata.append(tuple(("modified", prop.modified))) #date
    metadata.append(tuple(("revision", prop.revision))) # int
    metadata.append(tuple(("subject", prop.subject)))
    metadata.append(tuple(("title", prop.title)))
    metadata.append(tuple(("version", prop.version)))
    
    return metadata
 

def save(metadata, filepath, newfilepath):
    errors = None
    try:
        doc = docx.Document(filepath)
    except:
        return "Supplied filepath is invalid"
    try:
        prop = doc.core_properties
    except:
        return "An error occured while reading metadata"

    notuplelist = [list(i) for i in metadata]

    for item in notuplelist:
        if item[0] == "created" or item[0] == "last_printed" or item[0] == "modified": # datetime type
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
            
        if item[0] == "revision": # int
            try:
                setattr(prop, item[0], (int)(item[1]))
            except:
                return "Revision field must be an integer value"
        else:
            try:
                setattr(prop, item[0], item[1])
            except:
                return "An error occured while saving {} field".format(item[0])
    try:
        doc.save(newfilepath)
    except:
        return "Supplied filepath is invalid"