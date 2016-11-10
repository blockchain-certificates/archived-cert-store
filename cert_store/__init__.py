import logging.config
import os

import gridfs
from pymongo import MongoClient

from cert_store.certificate_store import CertificateStore
from cert_store.gridfs_key_value_store import GridfsKeyValueStore

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

cert_store_connection = None
logging.config.fileConfig(os.path.join(BASE_DIR, 'logging.conf'))
log = logging.getLogger(__name__)


def set_cert_store(conf):
    global cert_store_connection
    mongo_client = MongoClient(host=conf.mongodb_uri)
    db = mongo_client[conf.mongodb_uri[conf.mongodb_uri.rfind('/') + 1:len(conf.mongodb_uri)]]
    gfs = gridfs.GridFS(db)
    gfs_conn = GridfsKeyValueStore(gfs)
    cert_store_connection = CertificateStore(gfs_conn)
