"""Retrieves certificates from mongodb."""
import json
import logging

def certificate_uid_to_filename(uid):
    return uid + '.json'

class CertificateStore:
    def __init__(self, kv_store=None):
        """Create a CertificateStore
        :param kv_store: key value store; subclass of KeyValueStore
        """
        self.kv_store = kv_store

    def get_certificate(self, certificate_uid):
        """
        Returns certificate as json.
        :param certificate_uid:
        :return:
        """
        logging.debug('Retrieving certificate for uid=%s', certificate_uid)
        cert_file_bytes = self._get_certificate_raw(certificate_uid_to_filename(certificate_uid))
        if not cert_file_bytes:
            logging.warning('Could not find certificate for certificate uid=%s', certificate_uid)
            return None
        cert_string = cert_file_bytes.decode('utf-8')
        return json.loads(cert_string)

    def _get_certificate_raw(self, certificate_uid):
        """
        Returns certificate as raw bytes.
        :param certificate_uid:
        :return:
        """
        logging.debug('Retrieving certificate for uid=%s', certificate_uid)
        cert_file_bytes = self.kv_store.get(certificate_uid_to_filename(certificate_uid))
        if not cert_file_bytes:
            logging.warning('Could not find certificate for certificate uid=%s', certificate_uid)
            return None
        logging.debug('Found certificate for uid=%s', certificate_uid)
        return cert_file_bytes


class CertificateStoreV1(CertificateStore):
    """Retrieves certificates from mongodb."""
    def __init__(self,
                 kv_store=None,
                 db=None):
        """Create a CertificateStore
        :param kv_store: key value store; subclass of KeyValueStore
        :param db: certificates mongodb table (stores txid for verifying v1 certificates)
        """
        super(CertificateStore, self).__init__(kv_store)
        self.db = db

    def get_certificate_v1(self, certificate_uid):
        """
        Returns certificate as byte array. We need this for v1 certs, which compute a binary hash
        :param certificate_uid:
        :return:
        """
        logging.debug('Retrieving certificate for uid=%s', certificate_uid)
        certificate = self._find_certificate_by_uid(uid=certificate_uid)
        if certificate:
            cert_file_bytes = self._get_certificate_raw(certificate_uid_to_filename(certificate_uid))
            if not cert_file_bytes:
                logging.error(
                    'Could not find certificate for certificate uid=%s, but certificate metadata was found',
                    certificate_uid)
                return None, None
        else:
            logging.warning(
                'Certificate metadata not found for certificate uid=%s',
                certificate_uid)
            return None, None

        logging.debug('Found certificate for uid=%s', certificate_uid)
        return certificate, cert_file_bytes

    def _find_certificate_by_uid(self, uid=None):
        """
        Find certificate by certificate uid
        :param uid: certificate uid
        :return: certificate from certificates collection
        """
        certificate = None
        if uid:
            certificate = self.db.certificates.find_one({'uid': uid})
        return certificate