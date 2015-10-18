from django.conf import settings
from django.utils.functional import SimpleLazyObject
from pymongo import Connection

_connection = None


def get_connection():
    global _connection
    if not _connection:
        _connection = Connection(
            host=getattr(settings, 'MONGODB_HOST', None),
            port=getattr(settings, 'MONGODB_PORT', None)
        )
        username = getattr(settings, 'MONGODB_USERNAME', None)
        password = getattr(settings, 'MONGODB_PASSWORD', None)
        db = _connection[settings.MONGODB_DATABASE]
        if username and password:
            db.authenticate(username, password)
        return db
    return _connection[settings.MONGODB_DATABASE]


connection = SimpleLazyObject(get_connection)


def get_collection(collection_name):
    return getattr(connection, collection_name)
