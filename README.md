
[![PyPI version](https://badge.fury.io/py/cert-store.svg)](https://badge.fury.io/py/cert-store)


# cert-store

Blockchain certificate storage. This is used as a library in the cert-viewer project.

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

## Legacy options

**Warning**

Most users should ignore these instructions, which are only included as a temporary bridge for earlier users of blockcerts. We recommend migrating to the latest version of Blockcerts. 

### V1 Aware Certificate Store

Warning: avoid this option unless you are sure you need it. Earlier versions of the Blockchain Certificate
required a separate storage of the certificate transaction id. That was managed in a `certificates` mongo db table.

The `--v1_aware` flag allows support for these certificates.


## Unit tests

This project uses tox to validate against several python environments.

1. Ensure you have an python environment. [Recommendations](https://github.com/blockchain-certificates/developer-common-docs/blob/master/virtualenv.md)

2. Run tests
    ```
    ./run_tests.sh
    ```


## Contact

Contact [info@blockcerts.org](mailto:info@blockcerts.org) with questions
