"""
Type annotations for iotdeviceadvisor service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iotdeviceadvisor.client import IoTDeviceAdvisorClient

    session = Session()
    client: IoTDeviceAdvisorClient = session.client("iotdeviceadvisor")
    ```
"""

from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import AuthenticationMethodType
from .type_defs import (
    CreateSuiteDefinitionResponseTypeDef,
    GetEndpointResponseTypeDef,
    GetSuiteDefinitionResponseTypeDef,
    GetSuiteRunReportResponseTypeDef,
    GetSuiteRunResponseTypeDef,
    ListSuiteDefinitionsResponseTypeDef,
    ListSuiteRunsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartSuiteRunResponseTypeDef,
    SuiteDefinitionConfigurationUnionTypeDef,
    SuiteRunConfigurationUnionTypeDef,
    UpdateSuiteDefinitionResponseTypeDef,
)

__all__ = ("IoTDeviceAdvisorClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class IoTDeviceAdvisorClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTDeviceAdvisorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#close)
        """

    def create_suite_definition(
        self,
        *,
        suiteDefinitionConfiguration: SuiteDefinitionConfigurationUnionTypeDef,
        tags: Mapping[str, str] = ...,
    ) -> CreateSuiteDefinitionResponseTypeDef:
        """
        Creates a Device Advisor test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.create_suite_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#create_suite_definition)
        """

    def delete_suite_definition(self, *, suiteDefinitionId: str) -> Dict[str, Any]:
        """
        Deletes a Device Advisor test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.delete_suite_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#delete_suite_definition)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#generate_presigned_url)
        """

    def get_endpoint(
        self,
        *,
        thingArn: str = ...,
        certificateArn: str = ...,
        deviceRoleArn: str = ...,
        authenticationMethod: AuthenticationMethodType = ...,
    ) -> GetEndpointResponseTypeDef:
        """
        Gets information about an Device Advisor endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.get_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#get_endpoint)
        """

    def get_suite_definition(
        self, *, suiteDefinitionId: str, suiteDefinitionVersion: str = ...
    ) -> GetSuiteDefinitionResponseTypeDef:
        """
        Gets information about a Device Advisor test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.get_suite_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#get_suite_definition)
        """

    def get_suite_run(
        self, *, suiteDefinitionId: str, suiteRunId: str
    ) -> GetSuiteRunResponseTypeDef:
        """
        Gets information about a Device Advisor test suite run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.get_suite_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#get_suite_run)
        """

    def get_suite_run_report(
        self, *, suiteDefinitionId: str, suiteRunId: str
    ) -> GetSuiteRunReportResponseTypeDef:
        """
        Gets a report download link for a successful Device Advisor qualifying test
        suite
        run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.get_suite_run_report)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#get_suite_run_report)
        """

    def list_suite_definitions(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListSuiteDefinitionsResponseTypeDef:
        """
        Lists the Device Advisor test suites you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.list_suite_definitions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#list_suite_definitions)
        """

    def list_suite_runs(
        self,
        *,
        suiteDefinitionId: str = ...,
        suiteDefinitionVersion: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListSuiteRunsResponseTypeDef:
        """
        Lists runs of the specified Device Advisor test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.list_suite_runs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#list_suite_runs)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags attached to an IoT Device Advisor resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#list_tags_for_resource)
        """

    def start_suite_run(
        self,
        *,
        suiteDefinitionId: str,
        suiteRunConfiguration: SuiteRunConfigurationUnionTypeDef,
        suiteDefinitionVersion: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> StartSuiteRunResponseTypeDef:
        """
        Starts a Device Advisor test suite run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.start_suite_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#start_suite_run)
        """

    def stop_suite_run(self, *, suiteDefinitionId: str, suiteRunId: str) -> Dict[str, Any]:
        """
        Stops a Device Advisor test suite run that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.stop_suite_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#stop_suite_run)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds to and modifies existing tags of an IoT Device Advisor resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from an IoT Device Advisor resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#untag_resource)
        """

    def update_suite_definition(
        self,
        *,
        suiteDefinitionId: str,
        suiteDefinitionConfiguration: SuiteDefinitionConfigurationUnionTypeDef,
    ) -> UpdateSuiteDefinitionResponseTypeDef:
        """
        Updates a Device Advisor test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client.update_suite_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/client/#update_suite_definition)
        """
