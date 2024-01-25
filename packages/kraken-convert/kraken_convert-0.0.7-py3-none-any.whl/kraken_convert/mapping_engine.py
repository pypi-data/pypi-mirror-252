
import copy
from types import SimpleNamespace

from dateutil.parser import *
from datetime import *

def mapping_engine(record, dataset_record):


    actions = dataset_record.get('potentialAction', None)
    actions = actions if isinstance(actions, list) else [actions]
    
    if not actions or actions == [None]:
        actions = [
            {
                '@type': 'createAction',
                'instrument': dataset_record
            }
        ]

    
    new_record = record

    for i in actions:
        if not i:
            continue
            
        action_type = i.get('@type', None)

        if action_type == 'createAction':
            new_i = i.get('instrument', None) if 'instrument' in i.keys() else i
           
            new_record = _create_action(new_record, new_i)
            
        if action_type == 'replaceAction':
            new_record = _replaceAction(new_record, i)
    
    return new_record



def _create_action(record, createAction_record):
    """Given a record and a mapping, evaluates the mapping to build output record
    """

    map = createAction_record

    map = _remove_dots(map, True)
    record = _remove_dots(record, False)
    
    #Initialize r to be accessed with dot notation
    r = _to_dot_notation(record)

    if isinstance(map, dict):

        # Handle presence of base
        base = map.get('_base', None)
        if base:
            try:
                base_records = eval(base)
                base_records = base_records if isinstance(base_records, list) else [base_records]
                results = []
                new_map = copy.deepcopy(map)
                new_map.pop('_base')
                for i in base_records:
                    results.append(_create_action(i, new_map))
                return results
            except Exception as e:
                a=1
        
        # Else
        new_record = {}
        for k, v in map.items():
            if not k.startswith('_'):
                new_record[k] = _create_action(record, v)
        return new_record

    elif isinstance(map, list):
        new_record = []
        for i in map:
            new_record.append(_create_action(record, i))
        return new_record
    else:
        try:
            
            return eval(map)
        except Exception as e:
            
            return ''




def _remove_dots(record, is_map=False):

    if isinstance(record, dict):
        new_record = {}
        for k, v in record.items():
            new_k = k
            if is_map is False:
                new_k = new_k.replace('@', '_____')
                new_k = new_k.replace(':', '____')
                new_k = new_k.replace('#', '___')
            new_record[new_k] = _remove_dots(v, is_map)
        return new_record

    elif isinstance(record, list):
        new_record = []
        for i in record:
            new_record.append(_remove_dots(i, is_map))
        return new_record
    else:
        if isinstance(record, str):
            new_record = record
            if is_map is True:
                new_record = new_record.replace('@', '_____')
                new_record =  new_record.replace(':', '____')
                new_record = new_record.replace('#', '___')
                new_record = new_record.replace('https____', 'https:')
            return new_record
            
        else:
            return record



def _to_dot_notation(data):
    """Transform record into dot notation capable
        r = _to_dot_notation(record)
        value = r.a.b[2].c
    """

    if type(data) is list:
        return list(map(_to_dot_notation, data))
    elif type(data) is dict:
        sns = SimpleNamespace()
        for key, value in data.items():
            setattr(sns, key, _to_dot_notation(value))
        return sns
    else:
        return data



def _set_datetime(data):
    """Transform record into dot notation capable
        r = _to_dot_notation(record)
        value = r.a.b[2].c
    """

    if type(data) is list:
        return list(map(_set_datetime, data))
    elif type(data) is dict:
        for k, v in data.items():
            data[k] = _set_datetime(v)
        return data
    else:
        if isinstance(data, str) and len(data) > 6:
            try:
                data = parse(data)
            except Exception as e:
                a=1
        return data



def _replaceAction(record, replaceAction_record, key=None):
    """Replaces given values by new value. Useful for mapping between status type for example
    ('shipped' - > 'OrderInTransit')
    """

    if isinstance(record, list):
        new_record = [_replaceAction(x, replaceAction_record, key) for x in record]
        return new_record

    elif isinstance(record, dict):
        new_record = {}
        for k, v in record.items():
            new_k = '.'.join([key, k]) if key else k
            new_record[k] = _replaceAction(v, replaceAction_record, new_k)
        return new_record
    else:
        replaceAction_record = replaceAction_record if isinstance(replaceAction_record, list) else [replaceAction_record]
        for i in replaceAction_record:
            replacee_propertyID= i.get('replacee', {}).get('propertyID', None)
            replacee_value= i.get('replacee', {}).get('value', None)
            replacer_value= i.get('replacer', {}).get('value', None)

            if (replacee_propertyID == '*' or replacee_propertyID is None or replacee_propertyID == key) and replacee_value == record:
                return replacer_value

        return record
