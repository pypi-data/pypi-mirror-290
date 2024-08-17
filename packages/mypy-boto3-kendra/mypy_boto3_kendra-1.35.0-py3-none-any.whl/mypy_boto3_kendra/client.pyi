"""
Type annotations for kendra service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kendra.client import KendraClient

    session = Session()
    client: KendraClient = session.client("kendra")
    ```
"""

from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import (
    DataSourceSyncJobStatusType,
    DataSourceTypeType,
    FaqFileFormatType,
    FeaturedResultsSetStatusType,
    IndexEditionType,
    IntervalType,
    MetricTypeType,
    ModeType,
    QueryResultTypeType,
    SuggestionTypeType,
    UserContextPolicyType,
)
from .type_defs import (
    AssociateEntitiesToExperienceResponseTypeDef,
    AssociatePersonasToEntitiesResponseTypeDef,
    AttributeFilterTypeDef,
    AttributeSuggestionsGetConfigTypeDef,
    AttributeSuggestionsUpdateConfigTypeDef,
    BatchDeleteDocumentResponseTypeDef,
    BatchDeleteFeaturedResultsSetResponseTypeDef,
    BatchGetDocumentStatusResponseTypeDef,
    BatchPutDocumentResponseTypeDef,
    CapacityUnitsConfigurationTypeDef,
    ClickFeedbackTypeDef,
    CollapseConfigurationTypeDef,
    CreateAccessControlConfigurationResponseTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateExperienceResponseTypeDef,
    CreateFaqResponseTypeDef,
    CreateFeaturedResultsSetResponseTypeDef,
    CreateIndexResponseTypeDef,
    CreateQuerySuggestionsBlockListResponseTypeDef,
    CreateThesaurusResponseTypeDef,
    CustomDocumentEnrichmentConfigurationUnionTypeDef,
    DataSourceConfigurationUnionTypeDef,
    DataSourceSyncJobMetricTargetTypeDef,
    DataSourceVpcConfigurationUnionTypeDef,
    DescribeAccessControlConfigurationResponseTypeDef,
    DescribeDataSourceResponseTypeDef,
    DescribeExperienceResponseTypeDef,
    DescribeFaqResponseTypeDef,
    DescribeFeaturedResultsSetResponseTypeDef,
    DescribeIndexResponseTypeDef,
    DescribePrincipalMappingResponseTypeDef,
    DescribeQuerySuggestionsBlockListResponseTypeDef,
    DescribeQuerySuggestionsConfigResponseTypeDef,
    DescribeThesaurusResponseTypeDef,
    DisassociateEntitiesFromExperienceResponseTypeDef,
    DisassociatePersonasFromEntitiesResponseTypeDef,
    DocumentInfoTypeDef,
    DocumentMetadataConfigurationUnionTypeDef,
    DocumentRelevanceConfigurationTypeDef,
    DocumentTypeDef,
    EmptyResponseMetadataTypeDef,
    EntityConfigurationTypeDef,
    EntityPersonaConfigurationTypeDef,
    ExperienceConfigurationUnionTypeDef,
    FacetTypeDef,
    FeaturedDocumentTypeDef,
    GetQuerySuggestionsResponseTypeDef,
    GetSnapshotsResponseTypeDef,
    GroupMembersTypeDef,
    HierarchicalPrincipalUnionTypeDef,
    ListAccessControlConfigurationsResponseTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDataSourceSyncJobsResponseTypeDef,
    ListEntityPersonasResponseTypeDef,
    ListExperienceEntitiesResponseTypeDef,
    ListExperiencesResponseTypeDef,
    ListFaqsResponseTypeDef,
    ListFeaturedResultsSetsResponseTypeDef,
    ListGroupsOlderThanOrderingIdResponseTypeDef,
    ListIndicesResponseTypeDef,
    ListQuerySuggestionsBlockListsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListThesauriResponseTypeDef,
    PrincipalTypeDef,
    QueryResultTypeDef,
    RelevanceFeedbackTypeDef,
    RetrieveResultTypeDef,
    S3PathTypeDef,
    ServerSideEncryptionConfigurationTypeDef,
    SortingConfigurationTypeDef,
    SpellCorrectionConfigurationTypeDef,
    StartDataSourceSyncJobResponseTypeDef,
    TagTypeDef,
    TimeRangeUnionTypeDef,
    UpdateFeaturedResultsSetResponseTypeDef,
    UserContextTypeDef,
    UserGroupResolutionConfigurationTypeDef,
    UserTokenConfigurationTypeDef,
)

__all__ = ("KendraClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    FeaturedResultsConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceAlreadyExistException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class KendraClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KendraClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#exceptions)
        """

    def associate_entities_to_experience(
        self, *, Id: str, IndexId: str, EntityList: Sequence[EntityConfigurationTypeDef]
    ) -> AssociateEntitiesToExperienceResponseTypeDef:
        """
        Grants users or groups in your IAM Identity Center identity source access to
        your Amazon Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.associate_entities_to_experience)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#associate_entities_to_experience)
        """

    def associate_personas_to_entities(
        self, *, Id: str, IndexId: str, Personas: Sequence[EntityPersonaConfigurationTypeDef]
    ) -> AssociatePersonasToEntitiesResponseTypeDef:
        """
        Defines the specific permissions of users or groups in your IAM Identity Center
        identity source with access to your Amazon Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.associate_personas_to_entities)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#associate_personas_to_entities)
        """

    def batch_delete_document(
        self,
        *,
        IndexId: str,
        DocumentIdList: Sequence[str],
        DataSourceSyncJobMetricTarget: DataSourceSyncJobMetricTargetTypeDef = ...,
    ) -> BatchDeleteDocumentResponseTypeDef:
        """
        Removes one or more documents from an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.batch_delete_document)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#batch_delete_document)
        """

    def batch_delete_featured_results_set(
        self, *, IndexId: str, FeaturedResultsSetIds: Sequence[str]
    ) -> BatchDeleteFeaturedResultsSetResponseTypeDef:
        """
        Removes one or more sets of featured results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.batch_delete_featured_results_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#batch_delete_featured_results_set)
        """

    def batch_get_document_status(
        self, *, IndexId: str, DocumentInfoList: Sequence[DocumentInfoTypeDef]
    ) -> BatchGetDocumentStatusResponseTypeDef:
        """
        Returns the indexing status for one or more documents submitted with the
        [BatchPutDocument](https://docs.aws.amazon.com/kendra/latest/dg/API_BatchPutDocument.html)
        API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.batch_get_document_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#batch_get_document_status)
        """

    def batch_put_document(
        self,
        *,
        IndexId: str,
        Documents: Sequence[DocumentTypeDef],
        RoleArn: str = ...,
        CustomDocumentEnrichmentConfiguration: CustomDocumentEnrichmentConfigurationUnionTypeDef = ...,
    ) -> BatchPutDocumentResponseTypeDef:
        """
        Adds one or more documents to an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.batch_put_document)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#batch_put_document)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#can_paginate)
        """

    def clear_query_suggestions(self, *, IndexId: str) -> EmptyResponseMetadataTypeDef:
        """
        Clears existing query suggestions from an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.clear_query_suggestions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#clear_query_suggestions)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#close)
        """

    def create_access_control_configuration(
        self,
        *,
        IndexId: str,
        Name: str,
        Description: str = ...,
        AccessControlList: Sequence[PrincipalTypeDef] = ...,
        HierarchicalAccessControlList: Sequence[HierarchicalPrincipalUnionTypeDef] = ...,
        ClientToken: str = ...,
    ) -> CreateAccessControlConfigurationResponseTypeDef:
        """
        Creates an access configuration for your documents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_access_control_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#create_access_control_configuration)
        """

    def create_data_source(
        self,
        *,
        Name: str,
        IndexId: str,
        Type: DataSourceTypeType,
        Configuration: DataSourceConfigurationUnionTypeDef = ...,
        VpcConfiguration: DataSourceVpcConfigurationUnionTypeDef = ...,
        Description: str = ...,
        Schedule: str = ...,
        RoleArn: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ClientToken: str = ...,
        LanguageCode: str = ...,
        CustomDocumentEnrichmentConfiguration: CustomDocumentEnrichmentConfigurationUnionTypeDef = ...,
    ) -> CreateDataSourceResponseTypeDef:
        """
        Creates a data source connector that you want to use with an Amazon Kendra
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#create_data_source)
        """

    def create_experience(
        self,
        *,
        Name: str,
        IndexId: str,
        RoleArn: str = ...,
        Configuration: ExperienceConfigurationUnionTypeDef = ...,
        Description: str = ...,
        ClientToken: str = ...,
    ) -> CreateExperienceResponseTypeDef:
        """
        Creates an Amazon Kendra experience such as a search application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_experience)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#create_experience)
        """

    def create_faq(
        self,
        *,
        IndexId: str,
        Name: str,
        S3Path: S3PathTypeDef,
        RoleArn: str,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        FileFormat: FaqFileFormatType = ...,
        ClientToken: str = ...,
        LanguageCode: str = ...,
    ) -> CreateFaqResponseTypeDef:
        """
        Creates a set of frequently ask questions (FAQs) using a specified FAQ file
        stored in an Amazon S3
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_faq)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#create_faq)
        """

    def create_featured_results_set(
        self,
        *,
        IndexId: str,
        FeaturedResultsSetName: str,
        Description: str = ...,
        ClientToken: str = ...,
        Status: FeaturedResultsSetStatusType = ...,
        QueryTexts: Sequence[str] = ...,
        FeaturedDocuments: Sequence[FeaturedDocumentTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateFeaturedResultsSetResponseTypeDef:
        """
        Creates a set of featured results to display at the top of the search results
        page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_featured_results_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#create_featured_results_set)
        """

    def create_index(
        self,
        *,
        Name: str,
        RoleArn: str,
        Edition: IndexEditionType = ...,
        ServerSideEncryptionConfiguration: ServerSideEncryptionConfigurationTypeDef = ...,
        Description: str = ...,
        ClientToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        UserTokenConfigurations: Sequence[UserTokenConfigurationTypeDef] = ...,
        UserContextPolicy: UserContextPolicyType = ...,
        UserGroupResolutionConfiguration: UserGroupResolutionConfigurationTypeDef = ...,
    ) -> CreateIndexResponseTypeDef:
        """
        Creates an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#create_index)
        """

    def create_query_suggestions_block_list(
        self,
        *,
        IndexId: str,
        Name: str,
        SourceS3Path: S3PathTypeDef,
        RoleArn: str,
        Description: str = ...,
        ClientToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateQuerySuggestionsBlockListResponseTypeDef:
        """
        Creates a block list to exlcude certain queries from suggestions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_query_suggestions_block_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#create_query_suggestions_block_list)
        """

    def create_thesaurus(
        self,
        *,
        IndexId: str,
        Name: str,
        RoleArn: str,
        SourceS3Path: S3PathTypeDef,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ClientToken: str = ...,
    ) -> CreateThesaurusResponseTypeDef:
        """
        Creates a thesaurus for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_thesaurus)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#create_thesaurus)
        """

    def delete_access_control_configuration(self, *, IndexId: str, Id: str) -> Dict[str, Any]:
        """
        Deletes an access control configuration that you created for your documents in
        an
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_access_control_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#delete_access_control_configuration)
        """

    def delete_data_source(self, *, Id: str, IndexId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Kendra data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#delete_data_source)
        """

    def delete_experience(self, *, Id: str, IndexId: str) -> Dict[str, Any]:
        """
        Deletes your Amazon Kendra experience such as a search application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_experience)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#delete_experience)
        """

    def delete_faq(self, *, Id: str, IndexId: str) -> EmptyResponseMetadataTypeDef:
        """
        Removes an FAQ from an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_faq)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#delete_faq)
        """

    def delete_index(self, *, Id: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#delete_index)
        """

    def delete_principal_mapping(
        self, *, IndexId: str, GroupId: str, DataSourceId: str = ..., OrderingId: int = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a group so that all users and sub groups that belong to the group can
        no longer access documents only available to that
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_principal_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#delete_principal_mapping)
        """

    def delete_query_suggestions_block_list(
        self, *, IndexId: str, Id: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a block list used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_query_suggestions_block_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#delete_query_suggestions_block_list)
        """

    def delete_thesaurus(self, *, Id: str, IndexId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Kendra thesaurus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_thesaurus)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#delete_thesaurus)
        """

    def describe_access_control_configuration(
        self, *, IndexId: str, Id: str
    ) -> DescribeAccessControlConfigurationResponseTypeDef:
        """
        Gets information about an access control configuration that you created for
        your documents in an
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_access_control_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#describe_access_control_configuration)
        """

    def describe_data_source(self, *, Id: str, IndexId: str) -> DescribeDataSourceResponseTypeDef:
        """
        Gets information about an Amazon Kendra data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#describe_data_source)
        """

    def describe_experience(self, *, Id: str, IndexId: str) -> DescribeExperienceResponseTypeDef:
        """
        Gets information about your Amazon Kendra experience such as a search
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_experience)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#describe_experience)
        """

    def describe_faq(self, *, Id: str, IndexId: str) -> DescribeFaqResponseTypeDef:
        """
        Gets information about an FAQ list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_faq)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#describe_faq)
        """

    def describe_featured_results_set(
        self, *, IndexId: str, FeaturedResultsSetId: str
    ) -> DescribeFeaturedResultsSetResponseTypeDef:
        """
        Gets information about a set of featured results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_featured_results_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#describe_featured_results_set)
        """

    def describe_index(self, *, Id: str) -> DescribeIndexResponseTypeDef:
        """
        Gets information about an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#describe_index)
        """

    def describe_principal_mapping(
        self, *, IndexId: str, GroupId: str, DataSourceId: str = ...
    ) -> DescribePrincipalMappingResponseTypeDef:
        """
        Describes the processing of `PUT` and `DELETE` actions for mapping users to
        their
        groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_principal_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#describe_principal_mapping)
        """

    def describe_query_suggestions_block_list(
        self, *, IndexId: str, Id: str
    ) -> DescribeQuerySuggestionsBlockListResponseTypeDef:
        """
        Gets information about a block list used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_query_suggestions_block_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#describe_query_suggestions_block_list)
        """

    def describe_query_suggestions_config(
        self, *, IndexId: str
    ) -> DescribeQuerySuggestionsConfigResponseTypeDef:
        """
        Gets information on the settings of query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_query_suggestions_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#describe_query_suggestions_config)
        """

    def describe_thesaurus(self, *, Id: str, IndexId: str) -> DescribeThesaurusResponseTypeDef:
        """
        Gets information about an Amazon Kendra thesaurus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_thesaurus)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#describe_thesaurus)
        """

    def disassociate_entities_from_experience(
        self, *, Id: str, IndexId: str, EntityList: Sequence[EntityConfigurationTypeDef]
    ) -> DisassociateEntitiesFromExperienceResponseTypeDef:
        """
        Prevents users or groups in your IAM Identity Center identity source from
        accessing your Amazon Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.disassociate_entities_from_experience)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#disassociate_entities_from_experience)
        """

    def disassociate_personas_from_entities(
        self, *, Id: str, IndexId: str, EntityIds: Sequence[str]
    ) -> DisassociatePersonasFromEntitiesResponseTypeDef:
        """
        Removes the specific permissions of users or groups in your IAM Identity Center
        identity source with access to your Amazon Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.disassociate_personas_from_entities)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#disassociate_personas_from_entities)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#generate_presigned_url)
        """

    def get_query_suggestions(
        self,
        *,
        IndexId: str,
        QueryText: str,
        MaxSuggestionsCount: int = ...,
        SuggestionTypes: Sequence[SuggestionTypeType] = ...,
        AttributeSuggestionsConfig: AttributeSuggestionsGetConfigTypeDef = ...,
    ) -> GetQuerySuggestionsResponseTypeDef:
        """
        Fetches the queries that are suggested to your users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.get_query_suggestions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#get_query_suggestions)
        """

    def get_snapshots(
        self,
        *,
        IndexId: str,
        Interval: IntervalType,
        MetricType: MetricTypeType,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> GetSnapshotsResponseTypeDef:
        """
        Retrieves search metrics data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.get_snapshots)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#get_snapshots)
        """

    def list_access_control_configurations(
        self, *, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListAccessControlConfigurationsResponseTypeDef:
        """
        Lists one or more access control configurations for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_access_control_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_access_control_configurations)
        """

    def list_data_source_sync_jobs(
        self,
        *,
        Id: str,
        IndexId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        StartTimeFilter: TimeRangeUnionTypeDef = ...,
        StatusFilter: DataSourceSyncJobStatusType = ...,
    ) -> ListDataSourceSyncJobsResponseTypeDef:
        """
        Gets statistics about synchronizing a data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_data_source_sync_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_data_source_sync_jobs)
        """

    def list_data_sources(
        self, *, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDataSourcesResponseTypeDef:
        """
        Lists the data source connectors that you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_data_sources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_data_sources)
        """

    def list_entity_personas(
        self, *, Id: str, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListEntityPersonasResponseTypeDef:
        """
        Lists specific permissions of users and groups with access to your Amazon
        Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_entity_personas)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_entity_personas)
        """

    def list_experience_entities(
        self, *, Id: str, IndexId: str, NextToken: str = ...
    ) -> ListExperienceEntitiesResponseTypeDef:
        """
        Lists users or groups in your IAM Identity Center identity source that are
        granted access to your Amazon Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_experience_entities)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_experience_entities)
        """

    def list_experiences(
        self, *, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListExperiencesResponseTypeDef:
        """
        Lists one or more Amazon Kendra experiences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_experiences)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_experiences)
        """

    def list_faqs(
        self, *, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListFaqsResponseTypeDef:
        """
        Gets a list of FAQ lists associated with an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_faqs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_faqs)
        """

    def list_featured_results_sets(
        self, *, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListFeaturedResultsSetsResponseTypeDef:
        """
        Lists all your sets of featured results for a given index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_featured_results_sets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_featured_results_sets)
        """

    def list_groups_older_than_ordering_id(
        self,
        *,
        IndexId: str,
        OrderingId: int,
        DataSourceId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListGroupsOlderThanOrderingIdResponseTypeDef:
        """
        Provides a list of groups that are mapped to users before a given ordering or
        timestamp
        identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_groups_older_than_ordering_id)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_groups_older_than_ordering_id)
        """

    def list_indices(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListIndicesResponseTypeDef:
        """
        Lists the Amazon Kendra indexes that you created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_indices)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_indices)
        """

    def list_query_suggestions_block_lists(
        self, *, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListQuerySuggestionsBlockListsResponseTypeDef:
        """
        Lists the block lists used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_query_suggestions_block_lists)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_query_suggestions_block_lists)
        """

    def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of tags associated with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_tags_for_resource)
        """

    def list_thesauri(
        self, *, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListThesauriResponseTypeDef:
        """
        Lists the thesauri for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_thesauri)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#list_thesauri)
        """

    def put_principal_mapping(
        self,
        *,
        IndexId: str,
        GroupId: str,
        GroupMembers: GroupMembersTypeDef,
        DataSourceId: str = ...,
        OrderingId: int = ...,
        RoleArn: str = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Maps users to their groups so that you only need to provide the user ID when
        you issue the
        query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.put_principal_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#put_principal_mapping)
        """

    def query(
        self,
        *,
        IndexId: str,
        QueryText: str = ...,
        AttributeFilter: "AttributeFilterTypeDef" = ...,
        Facets: Sequence["FacetTypeDef"] = ...,
        RequestedDocumentAttributes: Sequence[str] = ...,
        QueryResultTypeFilter: QueryResultTypeType = ...,
        DocumentRelevanceOverrideConfigurations: Sequence[
            DocumentRelevanceConfigurationTypeDef
        ] = ...,
        PageNumber: int = ...,
        PageSize: int = ...,
        SortingConfiguration: SortingConfigurationTypeDef = ...,
        SortingConfigurations: Sequence[SortingConfigurationTypeDef] = ...,
        UserContext: UserContextTypeDef = ...,
        VisitorId: str = ...,
        SpellCorrectionConfiguration: SpellCorrectionConfigurationTypeDef = ...,
        CollapseConfiguration: CollapseConfigurationTypeDef = ...,
    ) -> QueryResultTypeDef:
        """
        Searches an index given an input query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#query)
        """

    def retrieve(
        self,
        *,
        IndexId: str,
        QueryText: str,
        AttributeFilter: "AttributeFilterTypeDef" = ...,
        RequestedDocumentAttributes: Sequence[str] = ...,
        DocumentRelevanceOverrideConfigurations: Sequence[
            DocumentRelevanceConfigurationTypeDef
        ] = ...,
        PageNumber: int = ...,
        PageSize: int = ...,
        UserContext: UserContextTypeDef = ...,
    ) -> RetrieveResultTypeDef:
        """
        Retrieves relevant passages or text excerpts given an input query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.retrieve)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#retrieve)
        """

    def start_data_source_sync_job(
        self, *, Id: str, IndexId: str
    ) -> StartDataSourceSyncJobResponseTypeDef:
        """
        Starts a synchronization job for a data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.start_data_source_sync_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#start_data_source_sync_job)
        """

    def stop_data_source_sync_job(self, *, Id: str, IndexId: str) -> EmptyResponseMetadataTypeDef:
        """
        Stops a synchronization job that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.stop_data_source_sync_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#stop_data_source_sync_job)
        """

    def submit_feedback(
        self,
        *,
        IndexId: str,
        QueryId: str,
        ClickFeedbackItems: Sequence[ClickFeedbackTypeDef] = ...,
        RelevanceFeedbackItems: Sequence[RelevanceFeedbackTypeDef] = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables you to provide feedback to Amazon Kendra to improve the performance of
        your
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.submit_feedback)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#submit_feedback)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tag to the specified index, FAQ, or data source resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from an index, FAQ, or a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#untag_resource)
        """

    def update_access_control_configuration(
        self,
        *,
        IndexId: str,
        Id: str,
        Name: str = ...,
        Description: str = ...,
        AccessControlList: Sequence[PrincipalTypeDef] = ...,
        HierarchicalAccessControlList: Sequence[HierarchicalPrincipalUnionTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Updates an access control configuration for your documents in an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_access_control_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#update_access_control_configuration)
        """

    def update_data_source(
        self,
        *,
        Id: str,
        IndexId: str,
        Name: str = ...,
        Configuration: DataSourceConfigurationUnionTypeDef = ...,
        VpcConfiguration: DataSourceVpcConfigurationUnionTypeDef = ...,
        Description: str = ...,
        Schedule: str = ...,
        RoleArn: str = ...,
        LanguageCode: str = ...,
        CustomDocumentEnrichmentConfiguration: CustomDocumentEnrichmentConfigurationUnionTypeDef = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon Kendra data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#update_data_source)
        """

    def update_experience(
        self,
        *,
        Id: str,
        IndexId: str,
        Name: str = ...,
        RoleArn: str = ...,
        Configuration: ExperienceConfigurationUnionTypeDef = ...,
        Description: str = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates your Amazon Kendra experience such as a search application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_experience)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#update_experience)
        """

    def update_featured_results_set(
        self,
        *,
        IndexId: str,
        FeaturedResultsSetId: str,
        FeaturedResultsSetName: str = ...,
        Description: str = ...,
        Status: FeaturedResultsSetStatusType = ...,
        QueryTexts: Sequence[str] = ...,
        FeaturedDocuments: Sequence[FeaturedDocumentTypeDef] = ...,
    ) -> UpdateFeaturedResultsSetResponseTypeDef:
        """
        Updates a set of featured results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_featured_results_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#update_featured_results_set)
        """

    def update_index(
        self,
        *,
        Id: str,
        Name: str = ...,
        RoleArn: str = ...,
        Description: str = ...,
        DocumentMetadataConfigurationUpdates: Sequence[
            DocumentMetadataConfigurationUnionTypeDef
        ] = ...,
        CapacityUnits: CapacityUnitsConfigurationTypeDef = ...,
        UserTokenConfigurations: Sequence[UserTokenConfigurationTypeDef] = ...,
        UserContextPolicy: UserContextPolicyType = ...,
        UserGroupResolutionConfiguration: UserGroupResolutionConfigurationTypeDef = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#update_index)
        """

    def update_query_suggestions_block_list(
        self,
        *,
        IndexId: str,
        Id: str,
        Name: str = ...,
        Description: str = ...,
        SourceS3Path: S3PathTypeDef = ...,
        RoleArn: str = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a block list used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_query_suggestions_block_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#update_query_suggestions_block_list)
        """

    def update_query_suggestions_config(
        self,
        *,
        IndexId: str,
        Mode: ModeType = ...,
        QueryLogLookBackWindowInDays: int = ...,
        IncludeQueriesWithoutUserInformation: bool = ...,
        MinimumNumberOfQueryingUsers: int = ...,
        MinimumQueryCount: int = ...,
        AttributeSuggestionsConfig: AttributeSuggestionsUpdateConfigTypeDef = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the settings of query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_query_suggestions_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#update_query_suggestions_config)
        """

    def update_thesaurus(
        self,
        *,
        Id: str,
        IndexId: str,
        Name: str = ...,
        Description: str = ...,
        RoleArn: str = ...,
        SourceS3Path: S3PathTypeDef = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a thesaurus for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_thesaurus)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra/client/#update_thesaurus)
        """
