"""
Type annotations for outposts service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_outposts.client import OutpostsClient

    session = Session()
    client: OutpostsClient = session.client("outposts")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AddressTypeType,
    AssetStateType,
    CapacityTaskStatusType,
    CatalogItemClassType,
    FiberOpticCableTypeType,
    MaximumSupportedWeightLbsType,
    OpticalStandardType,
    PaymentOptionType,
    PaymentTermType,
    PowerConnectorType,
    PowerDrawKvaType,
    PowerFeedDropType,
    PowerPhaseType,
    SupportedHardwareTypeType,
    SupportedStorageEnumType,
    UplinkCountType,
    UplinkGbpsType,
)
from .paginator import (
    GetOutpostInstanceTypesPaginator,
    GetOutpostSupportedInstanceTypesPaginator,
    ListAssetsPaginator,
    ListCapacityTasksPaginator,
    ListCatalogItemsPaginator,
    ListOrdersPaginator,
    ListOutpostsPaginator,
    ListSitesPaginator,
)
from .type_defs import (
    AddressTypeDef,
    CreateOrderOutputTypeDef,
    CreateOutpostOutputTypeDef,
    CreateSiteOutputTypeDef,
    GetCapacityTaskOutputTypeDef,
    GetCatalogItemOutputTypeDef,
    GetConnectionResponseTypeDef,
    GetOrderOutputTypeDef,
    GetOutpostInstanceTypesOutputTypeDef,
    GetOutpostOutputTypeDef,
    GetOutpostSupportedInstanceTypesOutputTypeDef,
    GetSiteAddressOutputTypeDef,
    GetSiteOutputTypeDef,
    InstanceTypeCapacityTypeDef,
    LineItemRequestTypeDef,
    ListAssetsOutputTypeDef,
    ListCapacityTasksOutputTypeDef,
    ListCatalogItemsOutputTypeDef,
    ListOrdersOutputTypeDef,
    ListOutpostsOutputTypeDef,
    ListSitesOutputTypeDef,
    ListTagsForResourceResponseTypeDef,
    RackPhysicalPropertiesTypeDef,
    StartCapacityTaskOutputTypeDef,
    StartConnectionResponseTypeDef,
    UpdateOutpostOutputTypeDef,
    UpdateSiteAddressOutputTypeDef,
    UpdateSiteOutputTypeDef,
    UpdateSiteRackPhysicalPropertiesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("OutpostsClient",)

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
    NotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class OutpostsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OutpostsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#can_paginate)
        """

    def cancel_capacity_task(
        self, *, CapacityTaskId: str, OutpostIdentifier: str
    ) -> Dict[str, Any]:
        """
        Cancels the capacity task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.cancel_capacity_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#cancel_capacity_task)
        """

    def cancel_order(self, *, OrderId: str) -> Dict[str, Any]:
        """
        Cancels the specified order for an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.cancel_order)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#cancel_order)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#close)
        """

    def create_order(
        self,
        *,
        OutpostIdentifier: str,
        LineItems: Sequence[LineItemRequestTypeDef],
        PaymentOption: PaymentOptionType,
        PaymentTerm: PaymentTermType = ...,
    ) -> CreateOrderOutputTypeDef:
        """
        Creates an order for an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.create_order)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#create_order)
        """

    def create_outpost(
        self,
        *,
        Name: str,
        SiteId: str,
        Description: str = ...,
        AvailabilityZone: str = ...,
        AvailabilityZoneId: str = ...,
        Tags: Mapping[str, str] = ...,
        SupportedHardwareType: SupportedHardwareTypeType = ...,
    ) -> CreateOutpostOutputTypeDef:
        """
        Creates an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.create_outpost)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#create_outpost)
        """

    def create_site(
        self,
        *,
        Name: str,
        Description: str = ...,
        Notes: str = ...,
        Tags: Mapping[str, str] = ...,
        OperatingAddress: AddressTypeDef = ...,
        ShippingAddress: AddressTypeDef = ...,
        RackPhysicalProperties: RackPhysicalPropertiesTypeDef = ...,
    ) -> CreateSiteOutputTypeDef:
        """
        Creates a site for an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.create_site)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#create_site)
        """

    def delete_outpost(self, *, OutpostId: str) -> Dict[str, Any]:
        """
        Deletes the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.delete_outpost)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#delete_outpost)
        """

    def delete_site(self, *, SiteId: str) -> Dict[str, Any]:
        """
        Deletes the specified site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.delete_site)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#delete_site)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#generate_presigned_url)
        """

    def get_capacity_task(
        self, *, CapacityTaskId: str, OutpostIdentifier: str
    ) -> GetCapacityTaskOutputTypeDef:
        """
        Gets details of the specified capacity task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_capacity_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_capacity_task)
        """

    def get_catalog_item(self, *, CatalogItemId: str) -> GetCatalogItemOutputTypeDef:
        """
        Gets information about the specified catalog item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_catalog_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_catalog_item)
        """

    def get_connection(self, *, ConnectionId: str) -> GetConnectionResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_connection)
        """

    def get_order(self, *, OrderId: str) -> GetOrderOutputTypeDef:
        """
        Gets information about the specified order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_order)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_order)
        """

    def get_outpost(self, *, OutpostId: str) -> GetOutpostOutputTypeDef:
        """
        Gets information about the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_outpost)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_outpost)
        """

    def get_outpost_instance_types(
        self, *, OutpostId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> GetOutpostInstanceTypesOutputTypeDef:
        """
        Gets the instance types for the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_outpost_instance_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_outpost_instance_types)
        """

    def get_outpost_supported_instance_types(
        self, *, OutpostIdentifier: str, OrderId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetOutpostSupportedInstanceTypesOutputTypeDef:
        """
        Gets the instance types that an Outpost can support in `InstanceTypeCapacity`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_outpost_supported_instance_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_outpost_supported_instance_types)
        """

    def get_site(self, *, SiteId: str) -> GetSiteOutputTypeDef:
        """
        Gets information about the specified Outpost site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_site)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_site)
        """

    def get_site_address(
        self, *, SiteId: str, AddressType: AddressTypeType
    ) -> GetSiteAddressOutputTypeDef:
        """
        Gets the site address of the specified site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_site_address)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_site_address)
        """

    def list_assets(
        self,
        *,
        OutpostIdentifier: str,
        HostIdFilter: Sequence[str] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        StatusFilter: Sequence[AssetStateType] = ...,
    ) -> ListAssetsOutputTypeDef:
        """
        Lists the hardware assets for the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_assets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_assets)
        """

    def list_capacity_tasks(
        self,
        *,
        OutpostIdentifierFilter: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        CapacityTaskStatusFilter: Sequence[CapacityTaskStatusType] = ...,
    ) -> ListCapacityTasksOutputTypeDef:
        """
        Lists the capacity tasks for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_capacity_tasks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_capacity_tasks)
        """

    def list_catalog_items(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        ItemClassFilter: Sequence[CatalogItemClassType] = ...,
        SupportedStorageFilter: Sequence[SupportedStorageEnumType] = ...,
        EC2FamilyFilter: Sequence[str] = ...,
    ) -> ListCatalogItemsOutputTypeDef:
        """
        Lists the items in the catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_catalog_items)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_catalog_items)
        """

    def list_orders(
        self, *, OutpostIdentifierFilter: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListOrdersOutputTypeDef:
        """
        Lists the Outpost orders for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_orders)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_orders)
        """

    def list_outposts(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        LifeCycleStatusFilter: Sequence[str] = ...,
        AvailabilityZoneFilter: Sequence[str] = ...,
        AvailabilityZoneIdFilter: Sequence[str] = ...,
    ) -> ListOutpostsOutputTypeDef:
        """
        Lists the Outposts for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_outposts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_outposts)
        """

    def list_sites(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        OperatingAddressCountryCodeFilter: Sequence[str] = ...,
        OperatingAddressStateOrRegionFilter: Sequence[str] = ...,
        OperatingAddressCityFilter: Sequence[str] = ...,
    ) -> ListSitesOutputTypeDef:
        """
        Lists the Outpost sites for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_sites)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_sites)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#list_tags_for_resource)
        """

    def start_capacity_task(
        self,
        *,
        OutpostIdentifier: str,
        OrderId: str,
        InstancePools: Sequence[InstanceTypeCapacityTypeDef],
        DryRun: bool = ...,
    ) -> StartCapacityTaskOutputTypeDef:
        """
        Starts the specified capacity task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.start_capacity_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#start_capacity_task)
        """

    def start_connection(
        self,
        *,
        AssetId: str,
        ClientPublicKey: str,
        NetworkInterfaceDeviceIndex: int,
        DeviceSerialNumber: str = ...,
    ) -> StartConnectionResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.start_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#start_connection)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#untag_resource)
        """

    def update_outpost(
        self,
        *,
        OutpostId: str,
        Name: str = ...,
        Description: str = ...,
        SupportedHardwareType: SupportedHardwareTypeType = ...,
    ) -> UpdateOutpostOutputTypeDef:
        """
        Updates an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.update_outpost)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#update_outpost)
        """

    def update_site(
        self, *, SiteId: str, Name: str = ..., Description: str = ..., Notes: str = ...
    ) -> UpdateSiteOutputTypeDef:
        """
        Updates the specified site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.update_site)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#update_site)
        """

    def update_site_address(
        self, *, SiteId: str, AddressType: AddressTypeType, Address: AddressTypeDef
    ) -> UpdateSiteAddressOutputTypeDef:
        """
        Updates the address of the specified site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.update_site_address)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#update_site_address)
        """

    def update_site_rack_physical_properties(
        self,
        *,
        SiteId: str,
        PowerDrawKva: PowerDrawKvaType = ...,
        PowerPhase: PowerPhaseType = ...,
        PowerConnector: PowerConnectorType = ...,
        PowerFeedDrop: PowerFeedDropType = ...,
        UplinkGbps: UplinkGbpsType = ...,
        UplinkCount: UplinkCountType = ...,
        FiberOpticCableType: FiberOpticCableTypeType = ...,
        OpticalStandard: OpticalStandardType = ...,
        MaximumSupportedWeightLbs: MaximumSupportedWeightLbsType = ...,
    ) -> UpdateSiteRackPhysicalPropertiesOutputTypeDef:
        """
        Update the physical and logistical details for a rack at a site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.update_site_rack_physical_properties)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#update_site_rack_physical_properties)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_outpost_instance_types"]
    ) -> GetOutpostInstanceTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_outpost_supported_instance_types"]
    ) -> GetOutpostSupportedInstanceTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_assets"]) -> ListAssetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_capacity_tasks"]
    ) -> ListCapacityTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_catalog_items"]
    ) -> ListCatalogItemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_orders"]) -> ListOrdersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_outposts"]) -> ListOutpostsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_sites"]) -> ListSitesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/client/#get_paginator)
        """
