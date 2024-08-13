# coding: utf-8

"""
    SciCat backend API

    This is the API for the SciCat Backend

    The version of the OpenAPI document: 4.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from Scicat-Python-SDK.models.credentials_dto import CredentialsDto

class TestCredentialsDto(unittest.TestCase):
    """CredentialsDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CredentialsDto:
        """Test CredentialsDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CredentialsDto`
        """
        model = CredentialsDto()
        if include_optional:
            return CredentialsDto(
                username = '',
                password = ''
            )
        else:
            return CredentialsDto(
                username = '',
                password = '',
        )
        """

    def testCredentialsDto(self):
        """Test CredentialsDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
