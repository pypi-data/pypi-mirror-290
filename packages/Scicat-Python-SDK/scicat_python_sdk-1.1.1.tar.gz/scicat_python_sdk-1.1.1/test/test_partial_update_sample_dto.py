# coding: utf-8

"""
    SciCat backend API

    This is the API for the SciCat Backend

    The version of the OpenAPI document: 4.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from Scicat-Python-SDK.models.partial_update_sample_dto import PartialUpdateSampleDto

class TestPartialUpdateSampleDto(unittest.TestCase):
    """PartialUpdateSampleDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PartialUpdateSampleDto:
        """Test PartialUpdateSampleDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PartialUpdateSampleDto`
        """
        model = PartialUpdateSampleDto()
        if include_optional:
            return PartialUpdateSampleDto(
                owner_group = '',
                access_groups = [
                    ''
                    ],
                instrument_group = '',
                owner = '',
                description = '',
                sample_characteristics = None,
                is_published = True
            )
        else:
            return PartialUpdateSampleDto(
        )
        """

    def testPartialUpdateSampleDto(self):
        """Test PartialUpdateSampleDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
