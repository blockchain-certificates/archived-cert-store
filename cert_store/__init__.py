import logging

import connexion
import os

from . import config

app = connexion.App(__name__, specification_dir='./swagger/')
app.add_api('swagger.yaml', arguments={
    'title': 'API Specification for introductions to a Blockchain Certificate issuer.'})


def initialize_logger():
    """Configure logging settings"""
    log_output_dir = config.log_dir
    log_file_name = config.log_file_name
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
