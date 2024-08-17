"""
Type annotations for cleanroomsml service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cleanroomsml.client import CleanRoomsMLClient

    session = Session()
    client: CleanRoomsMLClient = session.client("cleanroomsml")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import PolicyExistenceConditionType, SharedAudienceMetricsType, TagOnCreatePolicyType
from .paginator import (
    ListAudienceExportJobsPaginator,
    ListAudienceGenerationJobsPaginator,
    ListAudienceModelsPaginator,
    ListConfiguredAudienceModelsPaginator,
    ListTrainingDatasetsPaginator,
)
from .type_defs import (
    AudienceGenerationJobDataSourceUnionTypeDef,
    AudienceSizeConfigUnionTypeDef,
    AudienceSizeTypeDef,
    ConfiguredAudienceModelOutputConfigTypeDef,
    CreateAudienceModelResponseTypeDef,
    CreateConfiguredAudienceModelResponseTypeDef,
    CreateTrainingDatasetResponseTypeDef,
    DatasetUnionTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAudienceGenerationJobResponseTypeDef,
    GetAudienceModelResponseTypeDef,
    GetConfiguredAudienceModelPolicyResponseTypeDef,
    GetConfiguredAudienceModelResponseTypeDef,
    GetTrainingDatasetResponseTypeDef,
    ListAudienceExportJobsResponseTypeDef,
    ListAudienceGenerationJobsResponseTypeDef,
    ListAudienceModelsResponseTypeDef,
    ListConfiguredAudienceModelsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrainingDatasetsResponseTypeDef,
    PutConfiguredAudienceModelPolicyResponseTypeDef,
    StartAudienceGenerationJobResponseTypeDef,
    TimestampTypeDef,
    UpdateConfiguredAudienceModelResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CleanRoomsMLClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CleanRoomsMLClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CleanRoomsMLClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#close)
        """

    def create_audience_model(
        self,
        *,
        name: str,
        trainingDatasetArn: str,
        trainingDataStartTime: TimestampTypeDef = ...,
        trainingDataEndTime: TimestampTypeDef = ...,
        kmsKeyArn: str = ...,
        tags: Mapping[str, str] = ...,
        description: str = ...,
    ) -> CreateAudienceModelResponseTypeDef:
        """
        Defines the information necessary to create an audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.create_audience_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#create_audience_model)
        """

    def create_configured_audience_model(
        self,
        *,
        name: str,
        audienceModelArn: str,
        outputConfig: ConfiguredAudienceModelOutputConfigTypeDef,
        sharedAudienceMetrics: Sequence[SharedAudienceMetricsType],
        description: str = ...,
        minMatchingSeedSize: int = ...,
        audienceSizeConfig: AudienceSizeConfigUnionTypeDef = ...,
        tags: Mapping[str, str] = ...,
        childResourceTagOnCreatePolicy: TagOnCreatePolicyType = ...,
    ) -> CreateConfiguredAudienceModelResponseTypeDef:
        """
        Defines the information necessary to create a configured audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.create_configured_audience_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#create_configured_audience_model)
        """

    def create_training_dataset(
        self,
        *,
        name: str,
        roleArn: str,
        trainingData: Sequence[DatasetUnionTypeDef],
        tags: Mapping[str, str] = ...,
        description: str = ...,
    ) -> CreateTrainingDatasetResponseTypeDef:
        """
        Defines the information necessary to create a training dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.create_training_dataset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#create_training_dataset)
        """

    def delete_audience_generation_job(
        self, *, audienceGenerationJobArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified audience generation job, and removes all data associated
        with the
        job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.delete_audience_generation_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_audience_generation_job)
        """

    def delete_audience_model(self, *, audienceModelArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Specifies an audience model that you want to delete.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.delete_audience_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_audience_model)
        """

    def delete_configured_audience_model(
        self, *, configuredAudienceModelArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified configured audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.delete_configured_audience_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_configured_audience_model)
        """

    def delete_configured_audience_model_policy(
        self, *, configuredAudienceModelArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified configured audience model policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.delete_configured_audience_model_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_configured_audience_model_policy)
        """

    def delete_training_dataset(self, *, trainingDatasetArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Specifies a training dataset that you want to delete.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.delete_training_dataset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_training_dataset)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#generate_presigned_url)
        """

    def get_audience_generation_job(
        self, *, audienceGenerationJobArn: str
    ) -> GetAudienceGenerationJobResponseTypeDef:
        """
        Returns information about an audience generation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.get_audience_generation_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_audience_generation_job)
        """

    def get_audience_model(self, *, audienceModelArn: str) -> GetAudienceModelResponseTypeDef:
        """
        Returns information about an audience model See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/cleanroomsml-2023-09-06/GetAudienceModel).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.get_audience_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_audience_model)
        """

    def get_configured_audience_model(
        self, *, configuredAudienceModelArn: str
    ) -> GetConfiguredAudienceModelResponseTypeDef:
        """
        Returns information about a specified configured audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.get_configured_audience_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_configured_audience_model)
        """

    def get_configured_audience_model_policy(
        self, *, configuredAudienceModelArn: str
    ) -> GetConfiguredAudienceModelPolicyResponseTypeDef:
        """
        Returns information about a configured audience model policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.get_configured_audience_model_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_configured_audience_model_policy)
        """

    def get_training_dataset(self, *, trainingDatasetArn: str) -> GetTrainingDatasetResponseTypeDef:
        """
        Returns information about a training dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.get_training_dataset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_training_dataset)
        """

    def list_audience_export_jobs(
        self, *, nextToken: str = ..., maxResults: int = ..., audienceGenerationJobArn: str = ...
    ) -> ListAudienceExportJobsResponseTypeDef:
        """
        Returns a list of the audience export jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.list_audience_export_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_audience_export_jobs)
        """

    def list_audience_generation_jobs(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        configuredAudienceModelArn: str = ...,
        collaborationId: str = ...,
    ) -> ListAudienceGenerationJobsResponseTypeDef:
        """
        Returns a list of audience generation jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.list_audience_generation_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_audience_generation_jobs)
        """

    def list_audience_models(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListAudienceModelsResponseTypeDef:
        """
        Returns a list of audience models.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.list_audience_models)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_audience_models)
        """

    def list_configured_audience_models(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListConfiguredAudienceModelsResponseTypeDef:
        """
        Returns a list of the configured audience models.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.list_configured_audience_models)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_configured_audience_models)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a provided resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_tags_for_resource)
        """

    def list_training_datasets(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListTrainingDatasetsResponseTypeDef:
        """
        Returns a list of training datasets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.list_training_datasets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_training_datasets)
        """

    def put_configured_audience_model_policy(
        self,
        *,
        configuredAudienceModelArn: str,
        configuredAudienceModelPolicy: str,
        previousPolicyHash: str = ...,
        policyExistenceCondition: PolicyExistenceConditionType = ...,
    ) -> PutConfiguredAudienceModelPolicyResponseTypeDef:
        """
        Create or update the resource policy for a configured audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.put_configured_audience_model_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#put_configured_audience_model_policy)
        """

    def start_audience_export_job(
        self,
        *,
        name: str,
        audienceGenerationJobArn: str,
        audienceSize: AudienceSizeTypeDef,
        description: str = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Export an audience of a specified size after you have generated an audience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.start_audience_export_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#start_audience_export_job)
        """

    def start_audience_generation_job(
        self,
        *,
        name: str,
        configuredAudienceModelArn: str,
        seedAudience: AudienceGenerationJobDataSourceUnionTypeDef,
        includeSeedInOutput: bool = ...,
        collaborationId: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> StartAudienceGenerationJobResponseTypeDef:
        """
        Information necessary to start the audience generation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.start_audience_generation_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#start_audience_generation_job)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds metadata tags to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes metadata tags from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#untag_resource)
        """

    def update_configured_audience_model(
        self,
        *,
        configuredAudienceModelArn: str,
        outputConfig: ConfiguredAudienceModelOutputConfigTypeDef = ...,
        audienceModelArn: str = ...,
        sharedAudienceMetrics: Sequence[SharedAudienceMetricsType] = ...,
        minMatchingSeedSize: int = ...,
        audienceSizeConfig: AudienceSizeConfigUnionTypeDef = ...,
        description: str = ...,
    ) -> UpdateConfiguredAudienceModelResponseTypeDef:
        """
        Provides the information necessary to update a configured audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.update_configured_audience_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#update_configured_audience_model)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audience_export_jobs"]
    ) -> ListAudienceExportJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audience_generation_jobs"]
    ) -> ListAudienceGenerationJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audience_models"]
    ) -> ListAudienceModelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configured_audience_models"]
    ) -> ListConfiguredAudienceModelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_training_datasets"]
    ) -> ListTrainingDatasetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """
