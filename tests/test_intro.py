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


class TestIntro(unittest.TestCase):

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

    def test_definition_contains_introduction(self):

        # Get an example of dict for the definition Foo
        res = self.parser.definitions_example.get('Introduction')
        self.assertIsNotNone(res, 'Could not find definition of Introduction object')

        test = {
            "bitcoinAddress": "12jukZaXRLLbNRY9SB8KBQ14D1uK1EVKnA",
            "comments": "string",
            "email": "kim@test.com",
            "firstName": "string",
            "lastName": "string"
        }
        result = self.parser.get_dict_definition(test)
        self.assertEquals(result, 'Introduction')

    def test_valid_definition(self):
        test = {
            "bitcoinAddress": "12jukZaXRLLbNRY9SB8KBQ14D1uK1EVKnA",
            "comments": "string",
            "email": "kim@test.com",
            "firstName": "string",
            "lastName": "string"
        }

        result = self.parser.validate_definition('Introduction', test)
        self.assertTrue(result, 'Introduction schema was invalid')

    def test_valid_definition_missing_comments(self):
        """
        ok if comments are missing
        """
        test = {
            "bitcoinAddress": "12jukZaXRLLbNRY9SB8KBQ14D1uK1EVKnA",
            "email": "kim@test.com",
            "firstName": "string",
            "lastName": "string"
        }

        result = self.parser.validate_definition('Introduction', test)
        self.assertTrue(result, 'Introduction schema was invalid')


    def test_invalid_definition(self):
        """
        missing bitcoinAddress
        """
        test_invalid = {
            "comments": "string",
            "email": "kim@test.com",
            "firstName": "string",
            "lastName": "string"
        }
        result = self.parser.validate_definition('Introduction', test_invalid)
        self.assertFalse(result, 'Introduction schema should be invalid')

    def test_invalid_path(self):
        test = {
            "bitcoinAddress": "12jukZaXRLLbNRY9SB8KBQ14D1uK1EVKnA",
            "comments": "string",
            "email": "kim@test.com",
            "firstName": "string",
            "lastName": "string"
        }
        result = self.parser.validate_request('/intro_bad_path', 'post', query=test)
        self.assertFalse(result)


    def test_validate_request(self):
        test = {
            "bitcoinAddress": "12jukZaXRLLbNRY9SB8KBQ14D1uK1EVKnA",
            "comments": "string",
            "email": "kim@test.com",
            "firstName": "string",
            "lastName": "string"
        }
        # Validate that the given data match a path specification
        result = self.parser.validate_request('/intro/', 'post', body=test)
        self.assertTrue(result)

    def test_validate_request_invalid(self):
        test = {
            "bitcoinAddress": "12jukZaXRLLbNRY9SB8KBQ14D1uK1EVKnA",
            "comments": "string",
            "firstName": "string",
            "lastName": "string"
        }
        # Validate that the given data match a path specification
        result = self.parser.validate_request('/intro/', 'post', body=test)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
