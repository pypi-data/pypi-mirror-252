# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['ClientCredentialsArgs', 'ClientCredentials']

@pulumi.input_type
class ClientCredentialsArgs:
    def __init__(__self__, *,
                 authentication_method: pulumi.Input[str],
                 client_id: pulumi.Input[str],
                 client_secret: Optional[pulumi.Input[str]] = None,
                 private_key_jwt: Optional[pulumi.Input['ClientCredentialsPrivateKeyJwtArgs']] = None):
        """
        The set of arguments for constructing a ClientCredentials resource.
        :param pulumi.Input[str] authentication_method: Configure the method to use when making requests to any endpoint that requires this client to authenticate. Options include `none` (public client without a client secret), `client_secret_post` (confidential client using HTTP POST parameters), `client_secret_basic` (confidential client using HTTP Basic), `private_key_jwt` (confidential client using a Private Key JWT).
        :param pulumi.Input[str] client_id: The ID of the client for which to configure the authentication method.
        :param pulumi.Input[str] client_secret: Secret for the client when using `client_secret_post` or `client_secret_basic` authentication method. Keep this private.
               To access this attribute you need to add the `read:client_keys` scope to the Terraform client. Otherwise, the attribute
               will contain an empty string. The attribute will also be an empty string in case `private_key_jwt` is selected as an
               authentication method.
        :param pulumi.Input['ClientCredentialsPrivateKeyJwtArgs'] private_key_jwt: Defines `private_key_jwt` client authentication method.
        """
        pulumi.set(__self__, "authentication_method", authentication_method)
        pulumi.set(__self__, "client_id", client_id)
        if client_secret is not None:
            pulumi.set(__self__, "client_secret", client_secret)
        if private_key_jwt is not None:
            pulumi.set(__self__, "private_key_jwt", private_key_jwt)

    @property
    @pulumi.getter(name="authenticationMethod")
    def authentication_method(self) -> pulumi.Input[str]:
        """
        Configure the method to use when making requests to any endpoint that requires this client to authenticate. Options include `none` (public client without a client secret), `client_secret_post` (confidential client using HTTP POST parameters), `client_secret_basic` (confidential client using HTTP Basic), `private_key_jwt` (confidential client using a Private Key JWT).
        """
        return pulumi.get(self, "authentication_method")

    @authentication_method.setter
    def authentication_method(self, value: pulumi.Input[str]):
        pulumi.set(self, "authentication_method", value)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Input[str]:
        """
        The ID of the client for which to configure the authentication method.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> Optional[pulumi.Input[str]]:
        """
        Secret for the client when using `client_secret_post` or `client_secret_basic` authentication method. Keep this private.
        To access this attribute you need to add the `read:client_keys` scope to the Terraform client. Otherwise, the attribute
        will contain an empty string. The attribute will also be an empty string in case `private_key_jwt` is selected as an
        authentication method.
        """
        return pulumi.get(self, "client_secret")

    @client_secret.setter
    def client_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_secret", value)

    @property
    @pulumi.getter(name="privateKeyJwt")
    def private_key_jwt(self) -> Optional[pulumi.Input['ClientCredentialsPrivateKeyJwtArgs']]:
        """
        Defines `private_key_jwt` client authentication method.
        """
        return pulumi.get(self, "private_key_jwt")

    @private_key_jwt.setter
    def private_key_jwt(self, value: Optional[pulumi.Input['ClientCredentialsPrivateKeyJwtArgs']]):
        pulumi.set(self, "private_key_jwt", value)


@pulumi.input_type
class _ClientCredentialsState:
    def __init__(__self__, *,
                 authentication_method: Optional[pulumi.Input[str]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 private_key_jwt: Optional[pulumi.Input['ClientCredentialsPrivateKeyJwtArgs']] = None):
        """
        Input properties used for looking up and filtering ClientCredentials resources.
        :param pulumi.Input[str] authentication_method: Configure the method to use when making requests to any endpoint that requires this client to authenticate. Options include `none` (public client without a client secret), `client_secret_post` (confidential client using HTTP POST parameters), `client_secret_basic` (confidential client using HTTP Basic), `private_key_jwt` (confidential client using a Private Key JWT).
        :param pulumi.Input[str] client_id: The ID of the client for which to configure the authentication method.
        :param pulumi.Input[str] client_secret: Secret for the client when using `client_secret_post` or `client_secret_basic` authentication method. Keep this private.
               To access this attribute you need to add the `read:client_keys` scope to the Terraform client. Otherwise, the attribute
               will contain an empty string. The attribute will also be an empty string in case `private_key_jwt` is selected as an
               authentication method.
        :param pulumi.Input['ClientCredentialsPrivateKeyJwtArgs'] private_key_jwt: Defines `private_key_jwt` client authentication method.
        """
        if authentication_method is not None:
            pulumi.set(__self__, "authentication_method", authentication_method)
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if client_secret is not None:
            pulumi.set(__self__, "client_secret", client_secret)
        if private_key_jwt is not None:
            pulumi.set(__self__, "private_key_jwt", private_key_jwt)

    @property
    @pulumi.getter(name="authenticationMethod")
    def authentication_method(self) -> Optional[pulumi.Input[str]]:
        """
        Configure the method to use when making requests to any endpoint that requires this client to authenticate. Options include `none` (public client without a client secret), `client_secret_post` (confidential client using HTTP POST parameters), `client_secret_basic` (confidential client using HTTP Basic), `private_key_jwt` (confidential client using a Private Key JWT).
        """
        return pulumi.get(self, "authentication_method")

    @authentication_method.setter
    def authentication_method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authentication_method", value)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the client for which to configure the authentication method.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> Optional[pulumi.Input[str]]:
        """
        Secret for the client when using `client_secret_post` or `client_secret_basic` authentication method. Keep this private.
        To access this attribute you need to add the `read:client_keys` scope to the Terraform client. Otherwise, the attribute
        will contain an empty string. The attribute will also be an empty string in case `private_key_jwt` is selected as an
        authentication method.
        """
        return pulumi.get(self, "client_secret")

    @client_secret.setter
    def client_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_secret", value)

    @property
    @pulumi.getter(name="privateKeyJwt")
    def private_key_jwt(self) -> Optional[pulumi.Input['ClientCredentialsPrivateKeyJwtArgs']]:
        """
        Defines `private_key_jwt` client authentication method.
        """
        return pulumi.get(self, "private_key_jwt")

    @private_key_jwt.setter
    def private_key_jwt(self, value: Optional[pulumi.Input['ClientCredentialsPrivateKeyJwtArgs']]):
        pulumi.set(self, "private_key_jwt", value)


class ClientCredentials(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication_method: Optional[pulumi.Input[str]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 private_key_jwt: Optional[pulumi.Input[pulumi.InputType['ClientCredentialsPrivateKeyJwtArgs']]] = None,
                 __props__=None):
        """
        With this resource, you can configure the method to use when making requests to any endpoint that requires this client to authenticate.

        > Refer to the client secret rotation guide
        for instructions on how to rotate client secrets with zero downtime.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_auth0 as auth0

        my_client = auth0.Client("myClient",
            app_type="non_interactive",
            jwt_configuration=auth0.ClientJwtConfigurationArgs(
                alg="RS256",
            ))
        # Configuring client_secret_post as an authentication method.
        test_client_credentials = auth0.ClientCredentials("testClientCredentials",
            client_id=my_client.id,
            authentication_method="client_secret_post")
        # Configuring client_secret_basic as an authentication method.
        test_index_client_credentials_client_credentials = auth0.ClientCredentials("testIndex/clientCredentialsClientCredentials",
            client_id=my_client.id,
            authentication_method="client_secret_basic")
        # Configuring none as an authentication method.
        test_auth0_index_client_credentials_client_credentials = auth0.ClientCredentials("testAuth0Index/clientCredentialsClientCredentials",
            client_id=my_client.id,
            authentication_method="none")
        # Configuring private_key_jwt as an authentication method.
        test_auth0_index_client_credentials_client_credentials1 = auth0.ClientCredentials("testAuth0Index/clientCredentialsClientCredentials1",
            client_id=my_client.id,
            authentication_method="private_key_jwt",
            private_key_jwt=auth0.ClientCredentialsPrivateKeyJwtArgs(
                credentials=[auth0.ClientCredentialsPrivateKeyJwtCredentialArgs(
                    name="Testing Credentials 1",
                    credential_type="public_key",
                    algorithm="RS256",
                    parse_expiry_from_cert=True,
                    pem=\"\"\"-----BEGIN CERTIFICATE-----
        MIIFWDCCA0ACCQDXqpBo3R...G9w0BAQsFADBuMQswCQYDVQQGEwJl
        -----END CERTIFICATE-----
        \"\"\",
                )],
            ))
        # Configuring the client_secret.
        test_auth0_index_client_credentials_client_credentials2 = auth0.ClientCredentials("testAuth0Index/clientCredentialsClientCredentials2",
            client_id=my_client.id,
            authentication_method="client_secret_basic",
            client_secret="LUFqPx+sRLjbL7peYRPFmFu-bbvE7u7og4YUNe_C345=683341")
        ```

        ## Import

        This resource can be imported by specifying the client ID. # Example

        ```sh
         $ pulumi import auth0:index/clientCredentials:ClientCredentials my_creds "AaiyAPdpYdesoKnqjj8HJqRn4T5titww"
        ```

         ~> Importing this resource when the `authentication_method` is set to `private_key_jwt` will force the resource to be recreated. This is to be expected, because the pem file can't be checked for differences.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication_method: Configure the method to use when making requests to any endpoint that requires this client to authenticate. Options include `none` (public client without a client secret), `client_secret_post` (confidential client using HTTP POST parameters), `client_secret_basic` (confidential client using HTTP Basic), `private_key_jwt` (confidential client using a Private Key JWT).
        :param pulumi.Input[str] client_id: The ID of the client for which to configure the authentication method.
        :param pulumi.Input[str] client_secret: Secret for the client when using `client_secret_post` or `client_secret_basic` authentication method. Keep this private.
               To access this attribute you need to add the `read:client_keys` scope to the Terraform client. Otherwise, the attribute
               will contain an empty string. The attribute will also be an empty string in case `private_key_jwt` is selected as an
               authentication method.
        :param pulumi.Input[pulumi.InputType['ClientCredentialsPrivateKeyJwtArgs']] private_key_jwt: Defines `private_key_jwt` client authentication method.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClientCredentialsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        With this resource, you can configure the method to use when making requests to any endpoint that requires this client to authenticate.

        > Refer to the client secret rotation guide
        for instructions on how to rotate client secrets with zero downtime.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_auth0 as auth0

        my_client = auth0.Client("myClient",
            app_type="non_interactive",
            jwt_configuration=auth0.ClientJwtConfigurationArgs(
                alg="RS256",
            ))
        # Configuring client_secret_post as an authentication method.
        test_client_credentials = auth0.ClientCredentials("testClientCredentials",
            client_id=my_client.id,
            authentication_method="client_secret_post")
        # Configuring client_secret_basic as an authentication method.
        test_index_client_credentials_client_credentials = auth0.ClientCredentials("testIndex/clientCredentialsClientCredentials",
            client_id=my_client.id,
            authentication_method="client_secret_basic")
        # Configuring none as an authentication method.
        test_auth0_index_client_credentials_client_credentials = auth0.ClientCredentials("testAuth0Index/clientCredentialsClientCredentials",
            client_id=my_client.id,
            authentication_method="none")
        # Configuring private_key_jwt as an authentication method.
        test_auth0_index_client_credentials_client_credentials1 = auth0.ClientCredentials("testAuth0Index/clientCredentialsClientCredentials1",
            client_id=my_client.id,
            authentication_method="private_key_jwt",
            private_key_jwt=auth0.ClientCredentialsPrivateKeyJwtArgs(
                credentials=[auth0.ClientCredentialsPrivateKeyJwtCredentialArgs(
                    name="Testing Credentials 1",
                    credential_type="public_key",
                    algorithm="RS256",
                    parse_expiry_from_cert=True,
                    pem=\"\"\"-----BEGIN CERTIFICATE-----
        MIIFWDCCA0ACCQDXqpBo3R...G9w0BAQsFADBuMQswCQYDVQQGEwJl
        -----END CERTIFICATE-----
        \"\"\",
                )],
            ))
        # Configuring the client_secret.
        test_auth0_index_client_credentials_client_credentials2 = auth0.ClientCredentials("testAuth0Index/clientCredentialsClientCredentials2",
            client_id=my_client.id,
            authentication_method="client_secret_basic",
            client_secret="LUFqPx+sRLjbL7peYRPFmFu-bbvE7u7og4YUNe_C345=683341")
        ```

        ## Import

        This resource can be imported by specifying the client ID. # Example

        ```sh
         $ pulumi import auth0:index/clientCredentials:ClientCredentials my_creds "AaiyAPdpYdesoKnqjj8HJqRn4T5titww"
        ```

         ~> Importing this resource when the `authentication_method` is set to `private_key_jwt` will force the resource to be recreated. This is to be expected, because the pem file can't be checked for differences.

        :param str resource_name: The name of the resource.
        :param ClientCredentialsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClientCredentialsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication_method: Optional[pulumi.Input[str]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 private_key_jwt: Optional[pulumi.Input[pulumi.InputType['ClientCredentialsPrivateKeyJwtArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClientCredentialsArgs.__new__(ClientCredentialsArgs)

            if authentication_method is None and not opts.urn:
                raise TypeError("Missing required property 'authentication_method'")
            __props__.__dict__["authentication_method"] = authentication_method
            if client_id is None and not opts.urn:
                raise TypeError("Missing required property 'client_id'")
            __props__.__dict__["client_id"] = client_id
            __props__.__dict__["client_secret"] = None if client_secret is None else pulumi.Output.secret(client_secret)
            __props__.__dict__["private_key_jwt"] = private_key_jwt
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["clientSecret"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(ClientCredentials, __self__).__init__(
            'auth0:index/clientCredentials:ClientCredentials',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            authentication_method: Optional[pulumi.Input[str]] = None,
            client_id: Optional[pulumi.Input[str]] = None,
            client_secret: Optional[pulumi.Input[str]] = None,
            private_key_jwt: Optional[pulumi.Input[pulumi.InputType['ClientCredentialsPrivateKeyJwtArgs']]] = None) -> 'ClientCredentials':
        """
        Get an existing ClientCredentials resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication_method: Configure the method to use when making requests to any endpoint that requires this client to authenticate. Options include `none` (public client without a client secret), `client_secret_post` (confidential client using HTTP POST parameters), `client_secret_basic` (confidential client using HTTP Basic), `private_key_jwt` (confidential client using a Private Key JWT).
        :param pulumi.Input[str] client_id: The ID of the client for which to configure the authentication method.
        :param pulumi.Input[str] client_secret: Secret for the client when using `client_secret_post` or `client_secret_basic` authentication method. Keep this private.
               To access this attribute you need to add the `read:client_keys` scope to the Terraform client. Otherwise, the attribute
               will contain an empty string. The attribute will also be an empty string in case `private_key_jwt` is selected as an
               authentication method.
        :param pulumi.Input[pulumi.InputType['ClientCredentialsPrivateKeyJwtArgs']] private_key_jwt: Defines `private_key_jwt` client authentication method.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ClientCredentialsState.__new__(_ClientCredentialsState)

        __props__.__dict__["authentication_method"] = authentication_method
        __props__.__dict__["client_id"] = client_id
        __props__.__dict__["client_secret"] = client_secret
        __props__.__dict__["private_key_jwt"] = private_key_jwt
        return ClientCredentials(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="authenticationMethod")
    def authentication_method(self) -> pulumi.Output[str]:
        """
        Configure the method to use when making requests to any endpoint that requires this client to authenticate. Options include `none` (public client without a client secret), `client_secret_post` (confidential client using HTTP POST parameters), `client_secret_basic` (confidential client using HTTP Basic), `private_key_jwt` (confidential client using a Private Key JWT).
        """
        return pulumi.get(self, "authentication_method")

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Output[str]:
        """
        The ID of the client for which to configure the authentication method.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> pulumi.Output[str]:
        """
        Secret for the client when using `client_secret_post` or `client_secret_basic` authentication method. Keep this private.
        To access this attribute you need to add the `read:client_keys` scope to the Terraform client. Otherwise, the attribute
        will contain an empty string. The attribute will also be an empty string in case `private_key_jwt` is selected as an
        authentication method.
        """
        return pulumi.get(self, "client_secret")

    @property
    @pulumi.getter(name="privateKeyJwt")
    def private_key_jwt(self) -> pulumi.Output[Optional['outputs.ClientCredentialsPrivateKeyJwt']]:
        """
        Defines `private_key_jwt` client authentication method.
        """
        return pulumi.get(self, "private_key_jwt")

