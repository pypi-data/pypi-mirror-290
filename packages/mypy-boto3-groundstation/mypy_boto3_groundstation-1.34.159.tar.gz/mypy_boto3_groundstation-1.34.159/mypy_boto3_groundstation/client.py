"""
Type annotations for groundstation service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_groundstation.client import GroundStationClient

    session = Session()
    client: GroundStationClient = session.client("groundstation")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import ConfigCapabilityTypeType, ContactStatusType, EphemerisStatusType
from .paginator import (
    ListConfigsPaginator,
    ListContactsPaginator,
    ListDataflowEndpointGroupsPaginator,
    ListEphemeridesPaginator,
    ListGroundStationsPaginator,
    ListMissionProfilesPaginator,
    ListSatellitesPaginator,
)
from .type_defs import (
    AgentDetailsTypeDef,
    AggregateStatusTypeDef,
    ComponentStatusDataTypeDef,
    ConfigIdResponseTypeDef,
    ConfigTypeDataTypeDef,
    ContactIdResponseTypeDef,
    DataflowEndpointGroupIdResponseTypeDef,
    DescribeContactResponseTypeDef,
    DescribeEphemerisResponseTypeDef,
    DiscoveryDataTypeDef,
    EndpointDetailsUnionTypeDef,
    EphemerisDataTypeDef,
    EphemerisIdResponseTypeDef,
    GetAgentConfigurationResponseTypeDef,
    GetConfigResponseTypeDef,
    GetDataflowEndpointGroupResponseTypeDef,
    GetMinuteUsageResponseTypeDef,
    GetMissionProfileResponseTypeDef,
    GetSatelliteResponseTypeDef,
    KmsKeyTypeDef,
    ListConfigsResponseTypeDef,
    ListContactsResponseTypeDef,
    ListDataflowEndpointGroupsResponseTypeDef,
    ListEphemeridesResponseTypeDef,
    ListGroundStationsResponseTypeDef,
    ListMissionProfilesResponseTypeDef,
    ListSatellitesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    MissionProfileIdResponseTypeDef,
    RegisterAgentResponseTypeDef,
    TimestampTypeDef,
    UpdateAgentStatusResponseTypeDef,
)
from .waiter import ContactScheduledWaiter

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("GroundStationClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    DependencyException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class GroundStationClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GroundStationClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#can_paginate)
        """

    def cancel_contact(self, *, contactId: str) -> ContactIdResponseTypeDef:
        """
        Cancels a contact with a specified contact ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.cancel_contact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#cancel_contact)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#close)
        """

    def create_config(
        self, *, configData: ConfigTypeDataTypeDef, name: str, tags: Mapping[str, str] = ...
    ) -> ConfigIdResponseTypeDef:
        """
        Creates a `Config` with the specified `configData` parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.create_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#create_config)
        """

    def create_dataflow_endpoint_group(
        self,
        *,
        endpointDetails: Sequence[EndpointDetailsUnionTypeDef],
        contactPostPassDurationSeconds: int = ...,
        contactPrePassDurationSeconds: int = ...,
        tags: Mapping[str, str] = ...,
    ) -> DataflowEndpointGroupIdResponseTypeDef:
        """
        Creates a `DataflowEndpoint` group containing the specified list of
        `DataflowEndpoint`
        objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.create_dataflow_endpoint_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#create_dataflow_endpoint_group)
        """

    def create_ephemeris(
        self,
        *,
        name: str,
        satelliteId: str,
        enabled: bool = ...,
        ephemeris: EphemerisDataTypeDef = ...,
        expirationTime: TimestampTypeDef = ...,
        kmsKeyArn: str = ...,
        priority: int = ...,
        tags: Mapping[str, str] = ...,
    ) -> EphemerisIdResponseTypeDef:
        """
        Creates an Ephemeris with the specified `EphemerisData`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.create_ephemeris)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#create_ephemeris)
        """

    def create_mission_profile(
        self,
        *,
        dataflowEdges: Sequence[Sequence[str]],
        minimumViableContactDurationSeconds: int,
        name: str,
        trackingConfigArn: str,
        contactPostPassDurationSeconds: int = ...,
        contactPrePassDurationSeconds: int = ...,
        streamsKmsKey: KmsKeyTypeDef = ...,
        streamsKmsRole: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> MissionProfileIdResponseTypeDef:
        """
        Creates a mission profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.create_mission_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#create_mission_profile)
        """

    def delete_config(
        self, *, configId: str, configType: ConfigCapabilityTypeType
    ) -> ConfigIdResponseTypeDef:
        """
        Deletes a `Config`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.delete_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#delete_config)
        """

    def delete_dataflow_endpoint_group(
        self, *, dataflowEndpointGroupId: str
    ) -> DataflowEndpointGroupIdResponseTypeDef:
        """
        Deletes a dataflow endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.delete_dataflow_endpoint_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#delete_dataflow_endpoint_group)
        """

    def delete_ephemeris(self, *, ephemerisId: str) -> EphemerisIdResponseTypeDef:
        """
        Deletes an ephemeris See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/groundstation-2019-05-23/DeleteEphemeris).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.delete_ephemeris)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#delete_ephemeris)
        """

    def delete_mission_profile(self, *, missionProfileId: str) -> MissionProfileIdResponseTypeDef:
        """
        Deletes a mission profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.delete_mission_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#delete_mission_profile)
        """

    def describe_contact(self, *, contactId: str) -> DescribeContactResponseTypeDef:
        """
        Describes an existing contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.describe_contact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#describe_contact)
        """

    def describe_ephemeris(self, *, ephemerisId: str) -> DescribeEphemerisResponseTypeDef:
        """
        Describes an existing ephemeris.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.describe_ephemeris)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#describe_ephemeris)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#generate_presigned_url)
        """

    def get_agent_configuration(self, *, agentId: str) -> GetAgentConfigurationResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_agent_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_agent_configuration)
        """

    def get_config(
        self, *, configId: str, configType: ConfigCapabilityTypeType
    ) -> GetConfigResponseTypeDef:
        """
        Returns `Config` information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_config)
        """

    def get_dataflow_endpoint_group(
        self, *, dataflowEndpointGroupId: str
    ) -> GetDataflowEndpointGroupResponseTypeDef:
        """
        Returns the dataflow endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_dataflow_endpoint_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_dataflow_endpoint_group)
        """

    def get_minute_usage(self, *, month: int, year: int) -> GetMinuteUsageResponseTypeDef:
        """
        Returns the number of reserved minutes used by account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_minute_usage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_minute_usage)
        """

    def get_mission_profile(self, *, missionProfileId: str) -> GetMissionProfileResponseTypeDef:
        """
        Returns a mission profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_mission_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_mission_profile)
        """

    def get_satellite(self, *, satelliteId: str) -> GetSatelliteResponseTypeDef:
        """
        Returns a satellite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_satellite)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_satellite)
        """

    def list_configs(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListConfigsResponseTypeDef:
        """
        Returns a list of `Config` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.list_configs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#list_configs)
        """

    def list_contacts(
        self,
        *,
        endTime: TimestampTypeDef,
        startTime: TimestampTypeDef,
        statusList: Sequence[ContactStatusType],
        groundStation: str = ...,
        maxResults: int = ...,
        missionProfileArn: str = ...,
        nextToken: str = ...,
        satelliteArn: str = ...,
    ) -> ListContactsResponseTypeDef:
        """
        Returns a list of contacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.list_contacts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#list_contacts)
        """

    def list_dataflow_endpoint_groups(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListDataflowEndpointGroupsResponseTypeDef:
        """
        Returns a list of `DataflowEndpoint` groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.list_dataflow_endpoint_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#list_dataflow_endpoint_groups)
        """

    def list_ephemerides(
        self,
        *,
        endTime: TimestampTypeDef,
        satelliteId: str,
        startTime: TimestampTypeDef,
        maxResults: int = ...,
        nextToken: str = ...,
        statusList: Sequence[EphemerisStatusType] = ...,
    ) -> ListEphemeridesResponseTypeDef:
        """
        List existing ephemerides.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.list_ephemerides)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#list_ephemerides)
        """

    def list_ground_stations(
        self, *, maxResults: int = ..., nextToken: str = ..., satelliteId: str = ...
    ) -> ListGroundStationsResponseTypeDef:
        """
        Returns a list of ground stations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.list_ground_stations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#list_ground_stations)
        """

    def list_mission_profiles(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListMissionProfilesResponseTypeDef:
        """
        Returns a list of mission profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.list_mission_profiles)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#list_mission_profiles)
        """

    def list_satellites(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListSatellitesResponseTypeDef:
        """
        Returns a list of satellites.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.list_satellites)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#list_satellites)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#list_tags_for_resource)
        """

    def register_agent(
        self, *, agentDetails: AgentDetailsTypeDef, discoveryData: DiscoveryDataTypeDef
    ) -> RegisterAgentResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.register_agent)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#register_agent)
        """

    def reserve_contact(
        self,
        *,
        endTime: TimestampTypeDef,
        groundStation: str,
        missionProfileArn: str,
        satelliteArn: str,
        startTime: TimestampTypeDef,
        tags: Mapping[str, str] = ...,
    ) -> ContactIdResponseTypeDef:
        """
        Reserves a contact using specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.reserve_contact)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#reserve_contact)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Assigns a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deassigns a resource tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#untag_resource)
        """

    def update_agent_status(
        self,
        *,
        agentId: str,
        aggregateStatus: AggregateStatusTypeDef,
        componentStatuses: Sequence[ComponentStatusDataTypeDef],
        taskId: str,
    ) -> UpdateAgentStatusResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.update_agent_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#update_agent_status)
        """

    def update_config(
        self,
        *,
        configData: ConfigTypeDataTypeDef,
        configId: str,
        configType: ConfigCapabilityTypeType,
        name: str,
    ) -> ConfigIdResponseTypeDef:
        """
        Updates the `Config` used when scheduling contacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.update_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#update_config)
        """

    def update_ephemeris(
        self, *, enabled: bool, ephemerisId: str, name: str = ..., priority: int = ...
    ) -> EphemerisIdResponseTypeDef:
        """
        Updates an existing ephemeris See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/groundstation-2019-05-23/UpdateEphemeris).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.update_ephemeris)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#update_ephemeris)
        """

    def update_mission_profile(
        self,
        *,
        missionProfileId: str,
        contactPostPassDurationSeconds: int = ...,
        contactPrePassDurationSeconds: int = ...,
        dataflowEdges: Sequence[Sequence[str]] = ...,
        minimumViableContactDurationSeconds: int = ...,
        name: str = ...,
        streamsKmsKey: KmsKeyTypeDef = ...,
        streamsKmsRole: str = ...,
        trackingConfigArn: str = ...,
    ) -> MissionProfileIdResponseTypeDef:
        """
        Updates a mission profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.update_mission_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#update_mission_profile)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_configs"]) -> ListConfigsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_contacts"]) -> ListContactsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataflow_endpoint_groups"]
    ) -> ListDataflowEndpointGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ephemerides"]
    ) -> ListEphemeridesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ground_stations"]
    ) -> ListGroundStationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_mission_profiles"]
    ) -> ListMissionProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_satellites"]) -> ListSatellitesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_paginator)
        """

    def get_waiter(self, waiter_name: Literal["contact_scheduled"]) -> ContactScheduledWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/client/#get_waiter)
        """
