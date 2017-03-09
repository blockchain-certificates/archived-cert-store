"""Retrieves certificates from mongodb."""
import json
import logging

from cert_core import helpers, model
from cert_core.model import BlockcertVersion


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
        Returns a certificate. Propagates KeyError if key isn't found
        :param certificate_uid:
        :return:
        """
        certificate_json = self.get_certificate_json(certificate_uid)
        return model.to_certificate_model(certificate_json)

    def get_certificate_json(self, certificate_uid):
        """
        Returns certificate as json. Propagates KeyError if key isn't found
        :param certificate_uid:
        :return:
        """
        logging.debug('Retrieving certificate for uid=%s', certificate_uid)
        certificate_bytes = self._get_certificate_raw(certificate_uid)
        logging.debug('Found certificate for uid=%s', certificate_uid)
        certificate_json = helpers.certificate_bytes_to_json(certificate_bytes)
        return certificate_json

    def _get_certificate_raw(self, certificate_uid):
        """
        Returns certificate as raw bytes. Per kvstore contract, raises an KeyError if key isn't found.
        :param certificate_uid:
        :return:
        """
        cert_file_bytes = self.kv_store.get(certificate_uid_to_filename(certificate_uid))
        return cert_file_bytes


class V1AwareCertificateStore(CertificateStore):
    """Retrieves certificates from mongodb."""

    def __init__(self,
                 kv_store=None,
                 db=None):
        """Create a CertificateStore
        :param kv_store: key value store; subclass of KeyValueStore
        :param db: certificates mongodb table (stores txid for verifying v1 certificates)
        """
        super(V1AwareCertificateStore, self).__init__(kv_store)
        self.db = db

    def get_certificate(self, certificate_uid):
        """
        Returns certificate as byte array. We need this for v1 certs, which compute a binary hash. Raises
        KeyError if not found
        :param certificate_uid:
        :return:
        """
        logging.debug('Retrieving certificate for uid=%s', certificate_uid)

        version = model.detect_version_from_uid(certificate_uid)
        if version == BlockcertVersion.V1_2:
            return super(V1AwareCertificateStore, self).get_certificate(certificate_uid)

        # else it's V1.1 (if not valid, it will throw)
        certificate = self._find_certificate_metadata(uid=certificate_uid)
        if certificate:
            certificate_bytes = self._get_certificate_raw(certificate_uid)
            certificate_json = helpers.certificate_bytes_to_json(certificate_bytes)
            return model.to_certificate_model(certificate_json, certificate['txid'], certificate_bytes)

        message = 'Certificate metadata not found for certificate uid=%s' % certificate_uid
        logging.error(message)
        raise KeyError(message)

    def _find_certificate_metadata(self, uid=None):
        """
        Find certificate by certificate uid
        :param uid: certificate uid
        :return: certificate from certificates collection
        """
        certificate = self.db.certificates.find_one({'uid': uid})
        return certificate
