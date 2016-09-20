"""
Swagger/connexion is providing much the API format checking. This uses swagger-parser to inspect our .yaml file
and ensure the definitions are as expected. While the live API supports string pattern checking, it doesn't appear
SwaggerParser is using these to validate, so here we can only check things like missing parameters.
"""
import json
import unittest

import os
import tempfile
import yaml
from swagger_parser import SwaggerParser


class TestCertStore(unittest.TestCase):

    def setUp(self):
        """
        For swagger-parser, we need to convert the yaml file to json. Create a temp file to store the converted json,
        and set up the parser
        :return:
        """
        self.fileTemp = tempfile.NamedTemporaryFile(delete=False)
        with open('../cert_store/swagger/swagger.yaml', 'r') as f:
            doc = yaml.load(f)
        with open(self.fileTemp.name, 'w') as fp:
            json.dump(doc, fp, indent=4)
            self.fileTemp.close()

        self.parser = SwaggerParser(swagger_path=self.fileTemp.name)  # Init with file

    def tearDown(self):
        """
        Delete the temp file we created in setUp
        :return:
        """
        os.remove(self.fileTemp.name)

    def test_todo(self):
        self.assertTrue(True, 'TODO')


if __name__ == '__main__':
    unittest.main()
