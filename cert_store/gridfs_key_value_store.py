import logging

from simplekv import KeyValueStore


class GridfsKeyValueStore(KeyValueStore):
    def __init__(self, gfs_connection):
        self.gfs = gfs_connection

    def _delete(self, key):
        pass

    def iter_keys(self):
        pass

    def _open(self, key):
        the_file = self.gfs.find_one({'filename': key})
        if the_file:
            contents = the_file.read()
            if isinstance(contents, (bytes, bytearray)):
                logging.debug('Found content for key=%s', key)
                return contents
            else:
                logging.error('Found content for key=%s, but contents were not a byte array', key)
        logging.warning('Did not find content for key=%s', key)
        return None

    def _put_file(self, key, file):
        self.gfs.put(file, filename=key, encoding='utf-8')
