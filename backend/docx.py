# docx extension

# todo - "None" field not supported by datetime type? how to clear date??? (clear all problem)
# save and read method as in xlsx?

import docx
from datetime import datetime

def read(filepath):
    try:
        doc = docx.Document(filepath)
    except Exception as err: # todo - exception handling more detailed
        print(f"Unexpected {err=}, {type(err)=}")

    try:
        prop = doc.core_properties
    except Exception as err2: # todo - exception handling more detailed
        print(f"Unexpected {err2=}, {type(err2)=}")
                
    metadata = [] # list of tuples
    datatypes = [] # helper

    for d in dir(prop):
        if not d.startswith('_'):
            val = getattr(prop, d) # returns a value of a property
            if isinstance(val, datetime):
                val = val.strftime("%Y-%m-%d %H:%M:%S")
                datatypes.append("date")
            elif val is None: # very bad temp solution, better is to just use a position of a field
                datatypes.append("date")
            elif isinstance(val, int):
                datatypes.append("int")
            else:
                datatypes.append("")
            metadata.append(((d,val)))
    
    return metadata, datatypes
 

def save(newlist, filepath, newfilepath, datatypes):
    try:
        doc = docx.Document(filepath)
    except Exception as err: # todo - exception handling more detailed
        print(f"Unexpected {err=}, {type(err)=}")

    try:
        prop = doc.core_properties
    except Exception as err2: # todo - exception handling more detailed
        print(f"Unexpected {err2=}, {type(err2)=}")

    notuplelist = [list(i) for i in newlist]

    i = 0
    for d in dir(prop):
        if not d.startswith('_'):
            if datatypes[i] == "date":
                if notuplelist[i][1] != "None":
                    notuplelist[i][1] = datetime.strptime(notuplelist[i][1], "%Y-%m-%d %H:%M:%S")
                else: # if None by default
                    i+=1 
                    continue
                setattr(prop, d, (notuplelist[i][1]))
            elif datatypes[i] == "int":
                setattr(prop, d, (int)(notuplelist[i][1]))
            else:
                setattr(prop, d, notuplelist[i][1])
            i += 1

    doc.save(newfilepath)

