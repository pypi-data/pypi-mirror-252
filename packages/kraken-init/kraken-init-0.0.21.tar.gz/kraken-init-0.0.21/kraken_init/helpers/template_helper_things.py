
import uuid


def get_filename(name):

    return f'{name}/helpers/json.py'


def get_content(name, directory=None):


    dir = ''
    dir = directory.replace('/', '.') + '.' if directory else dir
    
    content = f'''
import datetime


def get_value(key, record):
    """Return value from different types of input records
    Accepts action record, or simple object
    """

    if record.get('@type', None) == 'action':
        record = record.get('object', None)

    value = record.get(key, None)

    return value

def get_instrument_record():
    """
    """
    record = {
        "@type": "WebAPI",
        "@id": "{str(uuid.uuid4())}",
        "name": "{name}",
        "description": "description"
    }

    return record

def get_action_record(object_record, result_record=None):
    """
    """

    action_record = {
        '@type': 'action',
        '@id': str(uuid.uuid4()),
        'name': '{name}',
        'object': object_record,
        'instrument': get_instrument(),
        'startTime': datetime.datetime.now(),
        'actionStatus': 'activeActionStatus'
    }

    if result_record:
        action_record['endTime] = datetime.datetime.now()
        action_record['actionStatus] = 'completedActionStatus'
        action_record['result] = result_record

    return action_record



    '''
    return content

