import logging
import os

import connexion
import gridfs
from pymongo import MongoClient

from cert_store import config
from cert_store.certificate_store import CertificateStore

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
conf = config.get_config()

app = connexion.App(__name__, specification_dir='./swagger/')
app.add_api('swagger.yaml', arguments={
    'title': 'API Specification for introductions to a Blockchain Certificate issuer.'})

def create_cert_store():
    mongo_client = MongoClient(host=conf.mongodb_uri)
    db = mongo_client[conf.mongodb_uri[conf.mongodb_uri.rfind('/') + 1:len(conf.mongodb_uri)]]
    gfs = gridfs.GridFS(db)
    return CertificateStore(mongo_client, gfs, db)

def initialize_logger():
    """Configure logging settings"""
    log_output_dir = conf.log_dir
    log_file_name = conf.log_file_name
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create file handler and set level to info
    handler = logging.FileHandler(
        os.path.join(
            log_output_dir,
            log_file_name),
        "w",
        encoding=None,
        delay="true")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


initialize_logger()
cert_store_connection = create_cert_store()
