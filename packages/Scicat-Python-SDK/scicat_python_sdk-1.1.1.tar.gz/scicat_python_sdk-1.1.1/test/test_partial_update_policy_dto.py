# coding: utf-8

"""
    SciCat backend API

    This is the API for the SciCat Backend

    The version of the OpenAPI document: 4.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from Scicat-Python-SDK.models.partial_update_policy_dto import PartialUpdatePolicyDto

class TestPartialUpdatePolicyDto(unittest.TestCase):
    """PartialUpdatePolicyDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PartialUpdatePolicyDto:
        """Test PartialUpdatePolicyDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PartialUpdatePolicyDto`
        """
        model = PartialUpdatePolicyDto()
        if include_optional:
            return PartialUpdatePolicyDto(
                owner_group = '',
                access_groups = [
                    ''
                    ],
                instrument_group = '',
                manager = [
                    ''
                    ],
                tape_redundancy = '',
                auto_archive = True,
                auto_archive_delay = 1.337,
                archive_email_notification = True,
                archive_emails_to_be_notified = [
                    ''
                    ],
                retrieve_email_notification = True,
                retrieve_emails_to_be_notified = [
                    ''
                    ],
                embargo_period = 1.337
            )
        else:
            return PartialUpdatePolicyDto(
        )
        """

    def testPartialUpdatePolicyDto(self):
        """Test PartialUpdatePolicyDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
