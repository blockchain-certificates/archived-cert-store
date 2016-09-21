"""Retrieves certificates from mongodb and stores certificate requests.  """
import logging


class CertificateStore:
    def __init__(self,
                 client=None,
                 gfs=None,
                 db=None):
        """Create a CertificateStore

        :param client: mongo client
        :param gfs: gridfs

        """
        self.client = client
        self.gfs = gfs
        self.db = db

    def get_certificate(self, certificate_uid):
        """
        Returns certificate as byte array. We need this for v1 certs, which compute a binary hash
        :param certificate_uid:
        :return:
        """

        logging.debug('Retrieving certificate for uid=%s', certificate_uid)
        certificate = self.find_certificate_by_uid(uid=certificate_uid)
        if certificate:
            raw_file = self.find_file_in_gridfs(certificate_to_filename(certificate))
        else:
            logging.warning(
                'Certificate metadata not found for certificate uid=%s',
                certificate_uid)

        if certificate and not raw_file:
            logging.error('Problem looking up certificate for certificate uid=%s, '
                          'but certificate metadata was found', certificate_uid)
        return raw_file


    def find_certificate_by_uid(self, uid=None):
        """
        Find certificate by certificate uid
        :param uid: certificate uid
        :return: certificate from certificates collection
        """
        certificate = None
        if uid:
            certificate = self.db.certificates.find_one(
                {'uid': uid})
        return certificate

    def find_file_in_gridfs(self, filename):
        certfile = self.gfs.find_one({'filename': filename})
        if certfile:
            contents = certfile.read()
            if isinstance(contents, (bytes, bytearray)):
                logging.debug('Found certificate for filename=%s', filename)
                return contents
            else:
                logging.error('Found certificate for filename=%s, but contents were not a byte array', filename)
        logging.warning('Did not find certificate for filename=%s', filename)
        return None

    def insert_certificate(self, cert_json):
        """Exposed separately to ease testing"""
        cert_id = CertificateStore.insert_shim(self.db.certificates, cert_json)
        return cert_id.inserted_id

    @staticmethod
    def insert_shim(collection, document):
        """This is an unfortunate workaround for mongo mock. It doesn't support insert, so this allows an easy patch"""
        inserted_id = collection.insert_one(document)
        return inserted_id


def certificate_to_filename(certificate):
    return certificate_uid_to_filename(parse_certificate_uid(certificate))


def certificate_uid_to_filename(uid):
    return uid + '.json'

def parse_standard_id_location(json_obj):
    return str(json_obj['uid'])


def parse_certificate_uid(certificate):
    return parse_standard_id_location(certificate)
