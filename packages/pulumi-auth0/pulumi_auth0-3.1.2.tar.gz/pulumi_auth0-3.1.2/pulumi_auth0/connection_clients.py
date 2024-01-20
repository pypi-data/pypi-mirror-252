# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ConnectionClientsArgs', 'ConnectionClients']

@pulumi.input_type
class ConnectionClientsArgs:
    def __init__(__self__, *,
                 connection_id: pulumi.Input[str],
                 enabled_clients: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        The set of arguments for constructing a ConnectionClients resource.
        :param pulumi.Input[str] connection_id: ID of the connection on which to enable the client.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] enabled_clients: IDs of the clients for which the connection is enabled.
        """
        pulumi.set(__self__, "connection_id", connection_id)
        pulumi.set(__self__, "enabled_clients", enabled_clients)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> pulumi.Input[str]:
        """
        ID of the connection on which to enable the client.
        """
        return pulumi.get(self, "connection_id")

    @connection_id.setter
    def connection_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "connection_id", value)

    @property
    @pulumi.getter(name="enabledClients")
    def enabled_clients(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        IDs of the clients for which the connection is enabled.
        """
        return pulumi.get(self, "enabled_clients")

    @enabled_clients.setter
    def enabled_clients(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "enabled_clients", value)


@pulumi.input_type
class _ConnectionClientsState:
    def __init__(__self__, *,
                 connection_id: Optional[pulumi.Input[str]] = None,
                 enabled_clients: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 strategy: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ConnectionClients resources.
        :param pulumi.Input[str] connection_id: ID of the connection on which to enable the client.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] enabled_clients: IDs of the clients for which the connection is enabled.
        :param pulumi.Input[str] name: The name of the connection on which to enable the client.
        :param pulumi.Input[str] strategy: The strategy of the connection on which to enable the client.
        """
        if connection_id is not None:
            pulumi.set(__self__, "connection_id", connection_id)
        if enabled_clients is not None:
            pulumi.set(__self__, "enabled_clients", enabled_clients)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if strategy is not None:
            pulumi.set(__self__, "strategy", strategy)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the connection on which to enable the client.
        """
        return pulumi.get(self, "connection_id")

    @connection_id.setter
    def connection_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_id", value)

    @property
    @pulumi.getter(name="enabledClients")
    def enabled_clients(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        IDs of the clients for which the connection is enabled.
        """
        return pulumi.get(self, "enabled_clients")

    @enabled_clients.setter
    def enabled_clients(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "enabled_clients", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the connection on which to enable the client.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def strategy(self) -> Optional[pulumi.Input[str]]:
        """
        The strategy of the connection on which to enable the client.
        """
        return pulumi.get(self, "strategy")

    @strategy.setter
    def strategy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "strategy", value)


class ConnectionClients(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_id: Optional[pulumi.Input[str]] = None,
                 enabled_clients: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        With this resource, you can manage all of the enabled clients on a connection.

        !> This resource manages all the enabled clients for a connection. In contrast, the `ConnectionClient` resource
        appends an enabled client to a connection. To avoid potential issues, it is recommended not to use this
        resource in conjunction with the `ConnectionClient` resource when managing enabled clients for the same
        connection id.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_auth0 as auth0

        my_conn = auth0.Connection("myConn", strategy="auth0")
        my_first_client = auth0.Client("myFirstClient")
        my_second_client = auth0.Client("mySecondClient")
        # One connection to many clients association.
        # To prevent issues, avoid using this resource together with the `auth0_connection_client` resource.
        my_conn_clients_assoc = auth0.ConnectionClients("myConnClientsAssoc",
            connection_id=my_conn.id,
            enabled_clients=[
                my_first_client.id,
                my_second_client.id,
            ])
        ```

        ## Import

        This resource can be imported by specifying the Connection ID. # Example

        ```sh
         $ pulumi import auth0:index/connectionClients:ConnectionClients my_conn_clients_assoc "con_XXXXX"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_id: ID of the connection on which to enable the client.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] enabled_clients: IDs of the clients for which the connection is enabled.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConnectionClientsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        With this resource, you can manage all of the enabled clients on a connection.

        !> This resource manages all the enabled clients for a connection. In contrast, the `ConnectionClient` resource
        appends an enabled client to a connection. To avoid potential issues, it is recommended not to use this
        resource in conjunction with the `ConnectionClient` resource when managing enabled clients for the same
        connection id.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_auth0 as auth0

        my_conn = auth0.Connection("myConn", strategy="auth0")
        my_first_client = auth0.Client("myFirstClient")
        my_second_client = auth0.Client("mySecondClient")
        # One connection to many clients association.
        # To prevent issues, avoid using this resource together with the `auth0_connection_client` resource.
        my_conn_clients_assoc = auth0.ConnectionClients("myConnClientsAssoc",
            connection_id=my_conn.id,
            enabled_clients=[
                my_first_client.id,
                my_second_client.id,
            ])
        ```

        ## Import

        This resource can be imported by specifying the Connection ID. # Example

        ```sh
         $ pulumi import auth0:index/connectionClients:ConnectionClients my_conn_clients_assoc "con_XXXXX"
        ```

        :param str resource_name: The name of the resource.
        :param ConnectionClientsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConnectionClientsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_id: Optional[pulumi.Input[str]] = None,
                 enabled_clients: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConnectionClientsArgs.__new__(ConnectionClientsArgs)

            if connection_id is None and not opts.urn:
                raise TypeError("Missing required property 'connection_id'")
            __props__.__dict__["connection_id"] = connection_id
            if enabled_clients is None and not opts.urn:
                raise TypeError("Missing required property 'enabled_clients'")
            __props__.__dict__["enabled_clients"] = enabled_clients
            __props__.__dict__["name"] = None
            __props__.__dict__["strategy"] = None
        super(ConnectionClients, __self__).__init__(
            'auth0:index/connectionClients:ConnectionClients',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            connection_id: Optional[pulumi.Input[str]] = None,
            enabled_clients: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            strategy: Optional[pulumi.Input[str]] = None) -> 'ConnectionClients':
        """
        Get an existing ConnectionClients resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_id: ID of the connection on which to enable the client.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] enabled_clients: IDs of the clients for which the connection is enabled.
        :param pulumi.Input[str] name: The name of the connection on which to enable the client.
        :param pulumi.Input[str] strategy: The strategy of the connection on which to enable the client.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ConnectionClientsState.__new__(_ConnectionClientsState)

        __props__.__dict__["connection_id"] = connection_id
        __props__.__dict__["enabled_clients"] = enabled_clients
        __props__.__dict__["name"] = name
        __props__.__dict__["strategy"] = strategy
        return ConnectionClients(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> pulumi.Output[str]:
        """
        ID of the connection on which to enable the client.
        """
        return pulumi.get(self, "connection_id")

    @property
    @pulumi.getter(name="enabledClients")
    def enabled_clients(self) -> pulumi.Output[Sequence[str]]:
        """
        IDs of the clients for which the connection is enabled.
        """
        return pulumi.get(self, "enabled_clients")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the connection on which to enable the client.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def strategy(self) -> pulumi.Output[str]:
        """
        The strategy of the connection on which to enable the client.
        """
        return pulumi.get(self, "strategy")

