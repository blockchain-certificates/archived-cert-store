import os
import unittest

from cert_store import FilesystemStore, CertificateStore

PATH = os.path.join(os.path.abspath(__file__), os.pardir)
TEST_DATA = os.path.join(PATH, 'data', '1.2')


class TestModel(unittest.TestCase):
    def test_basic(self):
        kv_store = FilesystemStore(TEST_DATA)
        cert_store = CertificateStore(kv_store)
        cert = cert_store.get_certificate('609c2989-275f-4f4c-ab02-b245cfb09017')
        self.assertIsNotNone(cert)
        self.assertEquals('Game of thrones issuer', cert.organization)


if __name__ == '__main__':
    unittest.main()
