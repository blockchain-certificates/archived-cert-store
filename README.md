
[![PyPI version](https://badge.fury.io/py/cert-store.svg)](https://badge.fury.io/py/cert-store)


# cert-store

Blockchain certificate storage. This is used as a library in the  cert-viewer project.

The certificate storage interface is [simplekv](https://pypi.python.org/pypi/simplekv/). The default configurations 
use the FilesystemStore, which is highly recommended if you are getting started. This makes it easier to issue,
copy, and view your Blockchain Certificates.

## Configuration

The certificate storage location can be modified with the following configuration entries in your `conf.ini` file:

- `cert_store_type`: which key-value backing store to use. Current supported values are:
  - `simplekv_fs`: (Default) file system store
  - `simplekv_gridfs`: (Advanced) gridfs store
- `cert_store_path`: file system path if using `simplekv_fs`
- `mongodb_uri`: mongo db uri (including db name) if using `simplekv_gridfs`


Example File System config:

```
cert_store_type = simplekv_fs
cert_store_path = ./cert_data
```

Example GridFS config (Advanced):

```
cert_store_type = simplekv_gridfs
mongodb_uri = mongodb://localhost:27017/test
```

## Advanced

This project is primarily used as a library, but it features a service
endpoint for deployments requiring a standalone certificate REST service.


### Running a Certificate Store Service with Docker 

These steps will start a Docker container running cert-store as a service. This is configured to use `simplekv_fs`
certificate store, and to copy the sample certificates in `cert_data` into the Docker container file system.

1. First ensure you have Docker installed. [See our Docker installation help](https://github.com/blockchain-certificates/developer-common-docs/blob/master/docker_install.md).
    
2. Git clone the repository

    ```
    git clone https://github.com/blockchain-certificates/cert-store.git
    ```

3. From a command line in the cert-store dir, run docker-compose

    ```
    cd cert-store
    docker-compose build
    ```

4. Start the container

    ```
    docker-compose up
    ```

5. You can see cert-store Swagger API specification at this URL:

    ```
    http://0.0.0.0:5003/ui/
    ```
    
The sample certificates can be viewed as follows:
    ```
    http://0.0.0.0:5003/certificates/f813349f-1385-487f-8d89-38a092411fa5
    ```

### Using a GridFS certificate store

`docker-compose-gridfs.yml` is configured to use a simplekv_gridfs certificate store. It uses a Mongo DB image 
image and prepopulates with `mongo-seed` data.

### V1 Aware Certificate Store

Warning: avoid this option unless you are sure you need it. Earlier versions of the Blockchain Certificate
required a separate storage of the certificate transaction id. That was managed in a `certificates` mongo db table.

The `--v1_aware` flag allows support for these certificates.

## Running the service locally

1. Ensure you have an python environment. [Recommendations](https://github.com/blockchain-certificates/developer-common-docs/blob/master/virtualenv.md)

2. Install [mongodb](https://docs.mongodb.com/v3.0/installation/)

3. Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```

4. Setup your config.py file

5. If using gridfs, start mongo database. `--dbpath` can be left off if you used the default location
    ```bash
    mongod --dbpath <path to data directory>
    ```
    
6. To run the server, execute the following:
    ```bash
    python run.py
    ```

You can see the Swagger API specification at this URL:

```
http://localhost:5003/ui/
```

## Unit tests

This project uses tox to validate against several python environments.

1. Ensure you have an python environment. [Recommendations](https://github.com/blockchain-certificates/developer-common-docs/blob/master/virtualenv.md)

2. Run tests
    ```
    ./run_tests.sh
    ```

## Release Docker image

```
docker build -t blockcerts/cert-store:latest .
docker login
docker push blockcerts/cert-store:latest
```


## Contact

Contact [info@blockcerts.org](mailto:info@blockcerts.org) with questions
