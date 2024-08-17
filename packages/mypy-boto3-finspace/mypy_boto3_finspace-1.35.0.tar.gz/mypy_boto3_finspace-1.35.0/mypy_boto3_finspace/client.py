"""
Type annotations for finspace service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_finspace.client import FinspaceClient

    session = Session()
    client: FinspaceClient = session.client("finspace")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import FederationModeType, KxAzModeType, KxClusterTypeType
from .paginator import ListKxEnvironmentsPaginator
from .type_defs import (
    AutoScalingConfigurationTypeDef,
    CapacityConfigurationTypeDef,
    ChangeRequestTypeDef,
    CodeConfigurationTypeDef,
    CreateEnvironmentResponseTypeDef,
    CreateKxChangesetResponseTypeDef,
    CreateKxClusterResponseTypeDef,
    CreateKxDatabaseResponseTypeDef,
    CreateKxDataviewResponseTypeDef,
    CreateKxEnvironmentResponseTypeDef,
    CreateKxScalingGroupResponseTypeDef,
    CreateKxUserResponseTypeDef,
    CreateKxVolumeResponseTypeDef,
    CustomDNSServerTypeDef,
    FederationParametersUnionTypeDef,
    GetEnvironmentResponseTypeDef,
    GetKxChangesetResponseTypeDef,
    GetKxClusterResponseTypeDef,
    GetKxConnectionStringResponseTypeDef,
    GetKxDatabaseResponseTypeDef,
    GetKxDataviewResponseTypeDef,
    GetKxEnvironmentResponseTypeDef,
    GetKxScalingGroupResponseTypeDef,
    GetKxUserResponseTypeDef,
    GetKxVolumeResponseTypeDef,
    KxCacheStorageConfigurationTypeDef,
    KxClusterCodeDeploymentConfigurationTypeDef,
    KxCommandLineArgumentTypeDef,
    KxDatabaseConfigurationUnionTypeDef,
    KxDataviewSegmentConfigurationUnionTypeDef,
    KxDeploymentConfigurationTypeDef,
    KxNAS1ConfigurationTypeDef,
    KxSavedownStorageConfigurationTypeDef,
    KxScalingGroupConfigurationTypeDef,
    ListEnvironmentsResponseTypeDef,
    ListKxChangesetsResponseTypeDef,
    ListKxClusterNodesResponseTypeDef,
    ListKxClustersResponseTypeDef,
    ListKxDatabasesResponseTypeDef,
    ListKxDataviewsResponseTypeDef,
    ListKxEnvironmentsResponseTypeDef,
    ListKxScalingGroupsResponseTypeDef,
    ListKxUsersResponseTypeDef,
    ListKxVolumesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    SuperuserParametersTypeDef,
    TickerplantLogConfigurationUnionTypeDef,
    TransitGatewayConfigurationUnionTypeDef,
    UpdateEnvironmentResponseTypeDef,
    UpdateKxDatabaseResponseTypeDef,
    UpdateKxDataviewResponseTypeDef,
    UpdateKxEnvironmentNetworkResponseTypeDef,
    UpdateKxEnvironmentResponseTypeDef,
    UpdateKxUserResponseTypeDef,
    UpdateKxVolumeResponseTypeDef,
    VpcConfigurationUnionTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("FinspaceClient",)


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
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class FinspaceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FinspaceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#close)
        """

    def create_environment(
        self,
        *,
        name: str,
        description: str = ...,
        kmsKeyId: str = ...,
        tags: Mapping[str, str] = ...,
        federationMode: FederationModeType = ...,
        federationParameters: FederationParametersUnionTypeDef = ...,
        superuserParameters: SuperuserParametersTypeDef = ...,
        dataBundles: Sequence[str] = ...,
    ) -> CreateEnvironmentResponseTypeDef:
        """
        Create a new FinSpace environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.create_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#create_environment)
        """

    def create_kx_changeset(
        self,
        *,
        environmentId: str,
        databaseName: str,
        changeRequests: Sequence[ChangeRequestTypeDef],
        clientToken: str,
    ) -> CreateKxChangesetResponseTypeDef:
        """
        Creates a changeset for a kdb database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.create_kx_changeset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#create_kx_changeset)
        """

    def create_kx_cluster(
        self,
        *,
        environmentId: str,
        clusterName: str,
        clusterType: KxClusterTypeType,
        releaseLabel: str,
        vpcConfiguration: VpcConfigurationUnionTypeDef,
        azMode: KxAzModeType,
        clientToken: str = ...,
        tickerplantLogConfiguration: TickerplantLogConfigurationUnionTypeDef = ...,
        databases: Sequence[KxDatabaseConfigurationUnionTypeDef] = ...,
        cacheStorageConfigurations: Sequence[KxCacheStorageConfigurationTypeDef] = ...,
        autoScalingConfiguration: AutoScalingConfigurationTypeDef = ...,
        clusterDescription: str = ...,
        capacityConfiguration: CapacityConfigurationTypeDef = ...,
        initializationScript: str = ...,
        commandLineArguments: Sequence[KxCommandLineArgumentTypeDef] = ...,
        code: CodeConfigurationTypeDef = ...,
        executionRole: str = ...,
        savedownStorageConfiguration: KxSavedownStorageConfigurationTypeDef = ...,
        availabilityZoneId: str = ...,
        tags: Mapping[str, str] = ...,
        scalingGroupConfiguration: KxScalingGroupConfigurationTypeDef = ...,
    ) -> CreateKxClusterResponseTypeDef:
        """
        Creates a new kdb cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.create_kx_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#create_kx_cluster)
        """

    def create_kx_database(
        self,
        *,
        environmentId: str,
        databaseName: str,
        clientToken: str,
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateKxDatabaseResponseTypeDef:
        """
        Creates a new kdb database in the environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.create_kx_database)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#create_kx_database)
        """

    def create_kx_dataview(
        self,
        *,
        environmentId: str,
        databaseName: str,
        dataviewName: str,
        azMode: KxAzModeType,
        clientToken: str,
        availabilityZoneId: str = ...,
        changesetId: str = ...,
        segmentConfigurations: Sequence[KxDataviewSegmentConfigurationUnionTypeDef] = ...,
        autoUpdate: bool = ...,
        readWrite: bool = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateKxDataviewResponseTypeDef:
        """
        Creates a snapshot of kdb database with tiered storage capabilities and a
        pre-warmed cache, ready for mounting on kdb
        clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.create_kx_dataview)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#create_kx_dataview)
        """

    def create_kx_environment(
        self,
        *,
        name: str,
        kmsKeyId: str,
        description: str = ...,
        tags: Mapping[str, str] = ...,
        clientToken: str = ...,
    ) -> CreateKxEnvironmentResponseTypeDef:
        """
        Creates a managed kdb environment for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.create_kx_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#create_kx_environment)
        """

    def create_kx_scaling_group(
        self,
        *,
        clientToken: str,
        environmentId: str,
        scalingGroupName: str,
        hostType: str,
        availabilityZoneId: str,
        tags: Mapping[str, str] = ...,
    ) -> CreateKxScalingGroupResponseTypeDef:
        """
        Creates a new scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.create_kx_scaling_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#create_kx_scaling_group)
        """

    def create_kx_user(
        self,
        *,
        environmentId: str,
        userName: str,
        iamRole: str,
        tags: Mapping[str, str] = ...,
        clientToken: str = ...,
    ) -> CreateKxUserResponseTypeDef:
        """
        Creates a user in FinSpace kdb environment with an associated IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.create_kx_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#create_kx_user)
        """

    def create_kx_volume(
        self,
        *,
        environmentId: str,
        volumeType: Literal["NAS_1"],
        volumeName: str,
        azMode: KxAzModeType,
        availabilityZoneIds: Sequence[str],
        clientToken: str = ...,
        description: str = ...,
        nas1Configuration: KxNAS1ConfigurationTypeDef = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateKxVolumeResponseTypeDef:
        """
        Creates a new volume with a specific amount of throughput and storage capacity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.create_kx_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#create_kx_volume)
        """

    def delete_environment(self, *, environmentId: str) -> Dict[str, Any]:
        """
        Delete an FinSpace environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.delete_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#delete_environment)
        """

    def delete_kx_cluster(
        self, *, environmentId: str, clusterName: str, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a kdb cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.delete_kx_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#delete_kx_cluster)
        """

    def delete_kx_cluster_node(
        self, *, environmentId: str, clusterName: str, nodeId: str
    ) -> Dict[str, Any]:
        """
        Deletes the specified nodes from a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.delete_kx_cluster_node)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#delete_kx_cluster_node)
        """

    def delete_kx_database(
        self, *, environmentId: str, databaseName: str, clientToken: str
    ) -> Dict[str, Any]:
        """
        Deletes the specified database and all of its associated data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.delete_kx_database)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#delete_kx_database)
        """

    def delete_kx_dataview(
        self, *, environmentId: str, databaseName: str, dataviewName: str, clientToken: str
    ) -> Dict[str, Any]:
        """
        Deletes the specified dataview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.delete_kx_dataview)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#delete_kx_dataview)
        """

    def delete_kx_environment(
        self, *, environmentId: str, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes the kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.delete_kx_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#delete_kx_environment)
        """

    def delete_kx_scaling_group(
        self, *, environmentId: str, scalingGroupName: str, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes the specified scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.delete_kx_scaling_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#delete_kx_scaling_group)
        """

    def delete_kx_user(
        self, *, userName: str, environmentId: str, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a user in the specified kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.delete_kx_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#delete_kx_user)
        """

    def delete_kx_volume(
        self, *, environmentId: str, volumeName: str, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.delete_kx_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#delete_kx_volume)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#generate_presigned_url)
        """

    def get_environment(self, *, environmentId: str) -> GetEnvironmentResponseTypeDef:
        """
        Returns the FinSpace environment object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.get_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#get_environment)
        """

    def get_kx_changeset(
        self, *, environmentId: str, databaseName: str, changesetId: str
    ) -> GetKxChangesetResponseTypeDef:
        """
        Returns information about a kdb changeset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.get_kx_changeset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#get_kx_changeset)
        """

    def get_kx_cluster(
        self, *, environmentId: str, clusterName: str
    ) -> GetKxClusterResponseTypeDef:
        """
        Retrieves information about a kdb cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.get_kx_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#get_kx_cluster)
        """

    def get_kx_connection_string(
        self, *, userArn: str, environmentId: str, clusterName: str
    ) -> GetKxConnectionStringResponseTypeDef:
        """
        Retrieves a connection string for a user to connect to a kdb cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.get_kx_connection_string)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#get_kx_connection_string)
        """

    def get_kx_database(
        self, *, environmentId: str, databaseName: str
    ) -> GetKxDatabaseResponseTypeDef:
        """
        Returns database information for the specified environment ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.get_kx_database)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#get_kx_database)
        """

    def get_kx_dataview(
        self, *, environmentId: str, databaseName: str, dataviewName: str
    ) -> GetKxDataviewResponseTypeDef:
        """
        Retrieves details of the dataview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.get_kx_dataview)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#get_kx_dataview)
        """

    def get_kx_environment(self, *, environmentId: str) -> GetKxEnvironmentResponseTypeDef:
        """
        Retrieves all the information for the specified kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.get_kx_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#get_kx_environment)
        """

    def get_kx_scaling_group(
        self, *, environmentId: str, scalingGroupName: str
    ) -> GetKxScalingGroupResponseTypeDef:
        """
        Retrieves details of a scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.get_kx_scaling_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#get_kx_scaling_group)
        """

    def get_kx_user(self, *, userName: str, environmentId: str) -> GetKxUserResponseTypeDef:
        """
        Retrieves information about the specified kdb user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.get_kx_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#get_kx_user)
        """

    def get_kx_volume(self, *, environmentId: str, volumeName: str) -> GetKxVolumeResponseTypeDef:
        """
        Retrieves the information about the volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.get_kx_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#get_kx_volume)
        """

    def list_environments(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListEnvironmentsResponseTypeDef:
        """
        A list of all of your FinSpace environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.list_environments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#list_environments)
        """

    def list_kx_changesets(
        self, *, environmentId: str, databaseName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListKxChangesetsResponseTypeDef:
        """
        Returns a list of all the changesets for a database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.list_kx_changesets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#list_kx_changesets)
        """

    def list_kx_cluster_nodes(
        self, *, environmentId: str, clusterName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListKxClusterNodesResponseTypeDef:
        """
        Lists all the nodes in a kdb cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.list_kx_cluster_nodes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#list_kx_cluster_nodes)
        """

    def list_kx_clusters(
        self,
        *,
        environmentId: str,
        clusterType: KxClusterTypeType = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListKxClustersResponseTypeDef:
        """
        Returns a list of clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.list_kx_clusters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#list_kx_clusters)
        """

    def list_kx_databases(
        self, *, environmentId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListKxDatabasesResponseTypeDef:
        """
        Returns a list of all the databases in the kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.list_kx_databases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#list_kx_databases)
        """

    def list_kx_dataviews(
        self, *, environmentId: str, databaseName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListKxDataviewsResponseTypeDef:
        """
        Returns a list of all the dataviews in the database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.list_kx_dataviews)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#list_kx_dataviews)
        """

    def list_kx_environments(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListKxEnvironmentsResponseTypeDef:
        """
        Returns a list of kdb environments created in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.list_kx_environments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#list_kx_environments)
        """

    def list_kx_scaling_groups(
        self, *, environmentId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListKxScalingGroupsResponseTypeDef:
        """
        Returns a list of scaling groups in a kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.list_kx_scaling_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#list_kx_scaling_groups)
        """

    def list_kx_users(
        self, *, environmentId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListKxUsersResponseTypeDef:
        """
        Lists all the users in a kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.list_kx_users)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#list_kx_users)
        """

    def list_kx_volumes(
        self,
        *,
        environmentId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        volumeType: Literal["NAS_1"] = ...,
    ) -> ListKxVolumesResponseTypeDef:
        """
        Lists all the volumes in a kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.list_kx_volumes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#list_kx_volumes)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        A list of all tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#list_tags_for_resource)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds metadata tags to a FinSpace resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes metadata tags from a FinSpace resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#untag_resource)
        """

    def update_environment(
        self,
        *,
        environmentId: str,
        name: str = ...,
        description: str = ...,
        federationMode: FederationModeType = ...,
        federationParameters: FederationParametersUnionTypeDef = ...,
    ) -> UpdateEnvironmentResponseTypeDef:
        """
        Update your FinSpace environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.update_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#update_environment)
        """

    def update_kx_cluster_code_configuration(
        self,
        *,
        environmentId: str,
        clusterName: str,
        code: CodeConfigurationTypeDef,
        clientToken: str = ...,
        initializationScript: str = ...,
        commandLineArguments: Sequence[KxCommandLineArgumentTypeDef] = ...,
        deploymentConfiguration: KxClusterCodeDeploymentConfigurationTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Allows you to update code configuration on a running cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.update_kx_cluster_code_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#update_kx_cluster_code_configuration)
        """

    def update_kx_cluster_databases(
        self,
        *,
        environmentId: str,
        clusterName: str,
        databases: Sequence[KxDatabaseConfigurationUnionTypeDef],
        clientToken: str = ...,
        deploymentConfiguration: KxDeploymentConfigurationTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Updates the databases mounted on a kdb cluster, which includes the
        `changesetId` and all the dbPaths to be
        cached.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.update_kx_cluster_databases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#update_kx_cluster_databases)
        """

    def update_kx_database(
        self, *, environmentId: str, databaseName: str, clientToken: str, description: str = ...
    ) -> UpdateKxDatabaseResponseTypeDef:
        """
        Updates information for the given kdb database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.update_kx_database)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#update_kx_database)
        """

    def update_kx_dataview(
        self,
        *,
        environmentId: str,
        databaseName: str,
        dataviewName: str,
        clientToken: str,
        description: str = ...,
        changesetId: str = ...,
        segmentConfigurations: Sequence[KxDataviewSegmentConfigurationUnionTypeDef] = ...,
    ) -> UpdateKxDataviewResponseTypeDef:
        """
        Updates the specified dataview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.update_kx_dataview)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#update_kx_dataview)
        """

    def update_kx_environment(
        self, *, environmentId: str, name: str = ..., description: str = ..., clientToken: str = ...
    ) -> UpdateKxEnvironmentResponseTypeDef:
        """
        Updates information for the given kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.update_kx_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#update_kx_environment)
        """

    def update_kx_environment_network(
        self,
        *,
        environmentId: str,
        transitGatewayConfiguration: TransitGatewayConfigurationUnionTypeDef = ...,
        customDNSConfiguration: Sequence[CustomDNSServerTypeDef] = ...,
        clientToken: str = ...,
    ) -> UpdateKxEnvironmentNetworkResponseTypeDef:
        """
        Updates environment network to connect to your internal network by using a
        transit
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.update_kx_environment_network)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#update_kx_environment_network)
        """

    def update_kx_user(
        self, *, environmentId: str, userName: str, iamRole: str, clientToken: str = ...
    ) -> UpdateKxUserResponseTypeDef:
        """
        Updates the user details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.update_kx_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#update_kx_user)
        """

    def update_kx_volume(
        self,
        *,
        environmentId: str,
        volumeName: str,
        description: str = ...,
        clientToken: str = ...,
        nas1Configuration: KxNAS1ConfigurationTypeDef = ...,
    ) -> UpdateKxVolumeResponseTypeDef:
        """
        Updates the throughput or capacity of a volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.update_kx_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#update_kx_volume)
        """

    def get_paginator(
        self, operation_name: Literal["list_kx_environments"]
    ) -> ListKxEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/client/#get_paginator)
        """
