import uuid
import datetime

def get_filename(name):

    return f'{name}/{name}.py'

def get_content(name, directory=None):
    """
    """
    class_name = name.replace('kraken_', '')
    
    class_name = class_name.capitalize()


    dir = ''
    dir = directory.replace('/', '.') + '.' if directory else dir
    
    record_value = {}

    content = f'''
    
import copy
from {dir}{name}.helpers import json
from {dir}{name}.helpers import things
import os
import pkg_resources



"""
Notes:
To access files in data directory, use:
new_path = pkg_resources.resource_filename('{name}', old_path)

"""

        
def method1():
    """
    """
    
    return True


def method2():
    """
    """
    
    return True


def get_request_record(record):
    """Return the value from a request
        Handles, value, object or action record
    """
    if not isinstance(record, dict):
        return record

    if record.get("@type", None) == "action":
        record = record.get("object", None)

    return record
    

def get_instrument():
    """Returns an instrument record for this function
    """
    record = {{
        "@type": "WebAPI",
        "@id": "{str(uuid.uuid4())}",
        "name": "{name}"
    }}

    return record

def get_action(object, name, action=None):
    """Return an action record with instrument
    """

    # If action is provided, updates the info
    if action:
        action['instrument'] = get_instrument()
        action['timeStart'] = datetime.datetime.now()
        return action
        

    record = {{
        "@type": "action",
        "@id": str(uuid.uuid4()),
        "name": name,
        "timeStart": datetime.datetime.now(),
        "timeEnd": None,
        "object": object,
        "instrument": get_instrument(),
        "actionStatus": "potentialActionStatus"
    }}
    return record
    
    '''
    
    return content
    