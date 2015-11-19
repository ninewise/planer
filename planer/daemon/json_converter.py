
import json

from flask import Response

from pony.orm.serialization import json_converter
from pony.orm.core import Query, Entity

def as_json(obj, status=200):
    return Response(
            json.dumps(_resolve(obj), default=json_converter),
            status=status,
            mimetype='application/json')

def _resolve(obj):
    if isinstance(obj, Entity):
        return obj.to_dict()
    elif isinstance(obj, Query):
        return [_resolve(x) for x in obj]
    else:
        return obj

