
import json

from pony.orm.serialization import json_converter
from pony.orm.core import Query

def to_json(obj):
    return json.dumps(_resolve(obj), default=json_converter)

def _resolve(obj):
    if isinstance(obj, Query):
        return [x.to_dict() for x in obj]
    else:
        return obj.to_dict()

