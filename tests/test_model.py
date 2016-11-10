import unittest

from cert_store import certificate_store
from cert_store import model
from cert_store.model import BlockcertVersion


class TestModel(unittest.TestCase):
    def test_detect_version_v1_1(self):
        with open('data/1.1/sample_signed_cert-1.1.json', 'rb') as cert_file:
            certificate_bytes = cert_file.read()
            certificate_json = certificate_store.certificate_bytes_to_json(certificate_bytes)
            version = model.detect_version(certificate_json)
            self.assertEquals(version, BlockcertVersion.V1_1)

    def test_detect_version_v1_2(self):
        with open('data/1.2/609c2989-275f-4f4c-ab02-b245cfb09017.json', 'rb') as cert_file:
            certificate_bytes = cert_file.read()
            certificate_json = certificate_store.certificate_bytes_to_json(certificate_bytes)
            version = model.detect_version(certificate_json)
            self.assertEquals(version, BlockcertVersion.V1_2)

    def test_v1_1(self):
        with open('data/1.1/sample_signed_cert-1.1.json', 'rb') as cert_file:
            certificate_bytes = cert_file.read()
            certificate_json = certificate_store.certificate_bytes_to_json(certificate_bytes)
            txid = '1703d2f5d706d495c1c65b40a086991ab755cc0a02bef51cd4aff9ed7a8586aa'
            v1_model = model.to_certificate_model(certificate_json, txid, certificate_bytes)
            self.assertEquals(v1_model.issuer_id, 'http://www.blockcerts.org/mockissuer/issuer/got-issuer.json')
            self.assertEquals(v1_model.transaction_id,
                              '1703d2f5d706d495c1c65b40a086991ab755cc0a02bef51cd4aff9ed7a8586aa')
            self.assertEquals(v1_model.title, 'Game of Thrones Character')

    def test_to_certificate_model_v1_1(self):
        with open('data/1.1/sample_signed_cert-1.1.json', 'rb') as cert_file:
            certificate_bytes = cert_file.read()
            certificate_json = certificate_store.certificate_bytes_to_json(certificate_bytes)
            txid = '1703d2f5d706d495c1c65b40a086991ab755cc0a02bef51cd4aff9ed7a8586aa'
            v1_model = model.to_certificate_model(certificate_json, txid, certificate_bytes)
            self.assertEquals(v1_model.version, BlockcertVersion.V1_1)
            self.assertEquals(v1_model.issuer_id, 'http://www.blockcerts.org/mockissuer/issuer/got-issuer.json')
            self.assertEquals(v1_model.transaction_id,
                              '1703d2f5d706d495c1c65b40a086991ab755cc0a02bef51cd4aff9ed7a8586aa')
            self.assertEquals(v1_model.title, 'Game of Thrones Character')

    def test_to_certificate_model_v1_2(self):
        with open('data/1.2/609c2989-275f-4f4c-ab02-b245cfb09017.json', 'rb') as cert_file:
            certificate_bytes = cert_file.read()
            certificate_json = certificate_store.certificate_bytes_to_json(certificate_bytes)
            v2_model = model.to_certificate_model(certificate_json)
            self.assertEquals(v2_model.version, BlockcertVersion.V1_2)
            self.assertEquals(v2_model.issuer_id, 'http://www.blockcerts.org/mockissuer/issuer/got-issuer_live.json')
            self.assertEquals(v2_model.transaction_id,
                              '8623beadbc7877a9e20fb7f83eda6c1a1fc350171f0714ff6c6c4054018eb54d')
            self.assertEquals(v2_model.title, 'Game of Thrones Character')


if __name__ == '__main__':
    unittest.main()
