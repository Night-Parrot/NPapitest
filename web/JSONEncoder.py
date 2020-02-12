import decimal
import flask.json
import json

class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):# pylint: disable=E0202
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return float(obj)
        return super(MyJSONEncoder, self).default(obj)




class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)