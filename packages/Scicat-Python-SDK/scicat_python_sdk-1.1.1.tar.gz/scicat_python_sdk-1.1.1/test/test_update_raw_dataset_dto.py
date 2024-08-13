# coding: utf-8

"""
    SciCat backend API

    This is the API for the SciCat Backend

    The version of the OpenAPI document: 4.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from Scicat-Python-SDK.models.update_raw_dataset_dto import UpdateRawDatasetDto

class TestUpdateRawDatasetDto(unittest.TestCase):
    """UpdateRawDatasetDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UpdateRawDatasetDto:
        """Test UpdateRawDatasetDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UpdateRawDatasetDto`
        """
        model = UpdateRawDatasetDto()
        if include_optional:
            return UpdateRawDatasetDto(
                owner_group = '',
                access_groups = [
                    ''
                    ],
                instrument_group = '',
                owner = '',
                owner_email = '',
                orcid_of_owner = '',
                contact_email = '',
                source_folder = '',
                source_folder_host = '',
                size = 1.337,
                packed_size = 1.337,
                number_of_files = 1.337,
                number_of_files_archived = 1.337,
                creation_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                validation_status = '',
                keywords = [
                    ''
                    ],
                description = '',
                dataset_name = '',
                classification = '',
                license = '',
                is_published = True,
                techniques = [
                    Scicat-Python-SDK.models.technique_class.TechniqueClass(
                        pid = '', 
                        name = '', )
                    ],
                shared_with = [
                    ''
                    ],
                relationships = [
                    Scicat-Python-SDK.models.relationship_class.RelationshipClass(
                        pid = '', 
                        relationship = '', )
                    ],
                datasetlifecycle = Scicat-Python-SDK.models.lifecycle_class.LifecycleClass(
                    archivable = True, 
                    retrievable = True, 
                    publishable = True, 
                    date_of_disk_purging = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    archive_retention_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    date_of_publishing = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    published_on = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    is_on_central_disk = True, 
                    archive_status_message = '', 
                    retrieve_status_message = '', 
                    archive_return_message = Scicat-Python-SDK.models.archive_return_message.archiveReturnMessage(), 
                    retrieve_return_message = Scicat-Python-SDK.models.retrieve_return_message.retrieveReturnMessage(), 
                    exported_to = '', 
                    retrieve_integrity_check = True, ),
                scientific_metadata = None,
                comment = '',
                data_quality_metrics = 1.337,
                principal_investigator = '',
                end_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                creation_location = '',
                data_format = '',
                proposal_id = '',
                sample_id = '',
                instrument_id = '',
                investigator = '',
                input_datasets = [
                    ''
                    ],
                used_software = [
                    ''
                    ],
                job_parameters = None,
                job_log_data = '',
                attachments = [
                    Scicat-Python-SDK.models.attachment.Attachment(
                        created_by = '', 
                        updated_by = '', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        owner_group = '', 
                        access_groups = [
                            ''
                            ], 
                        instrument_group = '', 
                        is_published = True, 
                        id = '', 
                        thumbnail = '', 
                        caption = '', 
                        dataset_id = '', 
                        proposal_id = '', 
                        sample_id = '', )
                    ],
                origdatablocks = [
                    Scicat-Python-SDK.models.orig_datablock.OrigDatablock(
                        created_by = '', 
                        updated_by = '', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        owner_group = '', 
                        access_groups = [
                            ''
                            ], 
                        instrument_group = '', 
                        is_published = True, 
                        _id = '', 
                        dataset_id = '', 
                        size = 1.337, 
                        chk_alg = '', 
                        data_file_list = [
                            Scicat-Python-SDK.models.data_file.DataFile(
                                path = '', 
                                size = 1.337, 
                                time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                chk = '', 
                                uid = '', 
                                gid = '', 
                                perm = '', )
                            ], )
                    ],
                datablocks = [
                    Scicat-Python-SDK.models.datablock.Datablock(
                        created_by = '', 
                        updated_by = '', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        owner_group = '', 
                        access_groups = [
                            ''
                            ], 
                        instrument_group = '', 
                        is_published = True, 
                        _id = '', 
                        dataset_id = '', 
                        archive_id = '', 
                        size = 1.337, 
                        packed_size = 1.337, 
                        chk_alg = '', 
                        version = '', 
                        data_file_list = [
                            Scicat-Python-SDK.models.data_file.DataFile(
                                path = '', 
                                size = 1.337, 
                                time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                chk = '', 
                                uid = '', 
                                gid = '', 
                                perm = '', )
                            ], )
                    ]
            )
        else:
            return UpdateRawDatasetDto(
                owner_group = '',
                owner = '',
                contact_email = '',
                source_folder = '',
                number_of_files_archived = 1.337,
                creation_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                principal_investigator = '',
                creation_location = '',
        )
        """

    def testUpdateRawDatasetDto(self):
        """Test UpdateRawDatasetDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
