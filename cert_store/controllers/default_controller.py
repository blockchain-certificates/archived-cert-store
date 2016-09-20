import os
from pymongo import MongoClient

from cert_store import config
from cert_store.certificate_store import CertificateStore
import gridfs

mongo_connection_string = os.environ.get('MONGODB_URI', config.mongo_connection_string_default)
print(mongo_connection_string)
mongo_client = MongoClient(host=mongo_connection_string)
db_name = mongo_connection_string[mongo_connection_string.rfind('/') + 1:len(mongo_connection_string)]
print(db_name)
db = mongo_client.get_database(db_name)
gfs = gridfs.GridFS(db)
store = CertificateStore(mongo_client, gfs, db)


def find_certificate_by_id_uid(uid):
    return store.get_certificate(uid)


