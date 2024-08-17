"""
Type annotations for timestream-influxdb service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_timestream_influxdb.client import TimestreamInfluxDBClient

    session = Session()
    client: TimestreamInfluxDBClient = session.client("timestream-influxdb")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import DbInstanceTypeType, DbStorageTypeType, DeploymentTypeType
from .paginator import ListDbInstancesPaginator, ListDbParameterGroupsPaginator
from .type_defs import (
    CreateDbInstanceOutputTypeDef,
    CreateDbParameterGroupOutputTypeDef,
    DeleteDbInstanceOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetDbInstanceOutputTypeDef,
    GetDbParameterGroupOutputTypeDef,
    ListDbInstancesOutputTypeDef,
    ListDbParameterGroupsOutputTypeDef,
    ListTagsForResourceResponseTypeDef,
    LogDeliveryConfigurationTypeDef,
    ParametersTypeDef,
    UpdateDbInstanceOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("TimestreamInfluxDBClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class TimestreamInfluxDBClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TimestreamInfluxDBClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#close)
        """

    def create_db_instance(
        self,
        *,
        name: str,
        password: str,
        dbInstanceType: DbInstanceTypeType,
        vpcSubnetIds: Sequence[str],
        vpcSecurityGroupIds: Sequence[str],
        allocatedStorage: int,
        username: str = ...,
        organization: str = ...,
        bucket: str = ...,
        publiclyAccessible: bool = ...,
        dbStorageType: DbStorageTypeType = ...,
        dbParameterGroupIdentifier: str = ...,
        deploymentType: DeploymentTypeType = ...,
        logDeliveryConfiguration: LogDeliveryConfigurationTypeDef = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateDbInstanceOutputTypeDef:
        """
        Creates a new Timestream for InfluxDB DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.create_db_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#create_db_instance)
        """

    def create_db_parameter_group(
        self,
        *,
        name: str,
        description: str = ...,
        parameters: ParametersTypeDef = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateDbParameterGroupOutputTypeDef:
        """
        Creates a new Timestream for InfluxDB DB parameter group to associate with DB
        instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.create_db_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#create_db_parameter_group)
        """

    def delete_db_instance(self, *, identifier: str) -> DeleteDbInstanceOutputTypeDef:
        """
        Deletes a Timestream for InfluxDB DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.delete_db_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#delete_db_instance)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#generate_presigned_url)
        """

    def get_db_instance(self, *, identifier: str) -> GetDbInstanceOutputTypeDef:
        """
        Returns a Timestream for InfluxDB DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.get_db_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#get_db_instance)
        """

    def get_db_parameter_group(self, *, identifier: str) -> GetDbParameterGroupOutputTypeDef:
        """
        Returns a Timestream for InfluxDB DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.get_db_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#get_db_parameter_group)
        """

    def list_db_instances(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListDbInstancesOutputTypeDef:
        """
        Returns a list of Timestream for InfluxDB DB instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.list_db_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#list_db_instances)
        """

    def list_db_parameter_groups(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListDbParameterGroupsOutputTypeDef:
        """
        Returns a list of Timestream for InfluxDB DB parameter groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.list_db_parameter_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#list_db_parameter_groups)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        A list of tags applied to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#list_tags_for_resource)
        """

    def tag_resource(
        self, *, resourceArn: str, tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Tags are composed of a Key/Value pairs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#tag_resource)
        """

    def untag_resource(
        self, *, resourceArn: str, tagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the tag from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#untag_resource)
        """

    def update_db_instance(
        self,
        *,
        identifier: str,
        logDeliveryConfiguration: LogDeliveryConfigurationTypeDef = ...,
        dbParameterGroupIdentifier: str = ...,
    ) -> UpdateDbInstanceOutputTypeDef:
        """
        Updates a Timestream for InfluxDB DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.update_db_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#update_db_instance)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_db_instances"]
    ) -> ListDbInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_db_parameter_groups"]
    ) -> ListDbParameterGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#get_paginator)
        """
