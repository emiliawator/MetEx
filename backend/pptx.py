# pptx extension
import collections # te dwie zaleznosci mega wazne
import collections.abc
from pptx import Presentation
from datetime import datetime

def read(filepath):
    prs = Presentation(filepath)
    prop = prs.core_properties
    metadata = []
    
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


def save(metadata, filepath, newfilepath, datatypes):
    prs = Presentation(filepath)
    prop = prs.core_properties
    notuplelist = [list(i) for i in metadata]

    for item in notuplelist:
        if item[0] == "created" or item[0] == "last_printed" or item[0] == "modified":
            if item[1] != "None":
                    item[1] = datetime.strptime(item[1], "%Y-%m-%d %H:%M:%S")
            else: # if None by default
                continue
            setattr(prop, item[0], item[1])
        if item[0] == "revision": # int
            setattr(prop, item[0], (int)(item[1]))
        else:
            setattr(prop, item[0], item[1])

    prs.save(newfilepath)