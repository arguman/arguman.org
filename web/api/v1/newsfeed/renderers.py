from django.utils.encoding import force_text
from bson import ObjectId

from rest_framework.utils.encoders import JSONEncoder
from rest_framework.renderers import JSONRenderer


class MongoDBJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return force_text(obj)
        return super(MongoDBJSONEncoder, self).default(obj)


class MongoDBJSONRenderer(JSONRenderer):
    encoder_class = MongoDBJSONEncoder
