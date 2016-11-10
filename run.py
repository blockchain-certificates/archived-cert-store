#!/usr/bin/env python

import os

import connexion

import cert_store
from cert_store import config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def main():
    conf = config.get_config()
    cert_store.configure_app(conf)
    port = int(os.environ.get('PORT', 5003))
    app = connexion.App(__name__, specification_dir=os.path.join(BASE_DIR, 'cert_store', 'swagger'))
    app.add_api('swagger.yaml', arguments={
        'title': 'API Specification for introductions to a Blockchain Certificate issuer.'})
    app.run(port=port)


if __name__ == "__main__":
    main()
