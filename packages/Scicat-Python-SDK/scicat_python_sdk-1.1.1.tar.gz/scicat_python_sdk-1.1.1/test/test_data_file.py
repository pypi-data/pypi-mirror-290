# coding: utf-8

"""
    SciCat backend API

    This is the API for the SciCat Backend

    The version of the OpenAPI document: 4.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from Scicat-Python-SDK.models.data_file import DataFile

class TestDataFile(unittest.TestCase):
    """DataFile unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DataFile:
        """Test DataFile
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DataFile`
        """
        model = DataFile()
        if include_optional:
            return DataFile(
                path = '',
                size = 1.337,
                time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                chk = '',
                uid = '',
                gid = '',
                perm = ''
            )
        else:
            return DataFile(
                path = '',
                size = 1.337,
                time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
        )
        """

    def testDataFile(self):
        """Test DataFile"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
