'''
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
![npm](https://img.shields.io/npm/v/%40jttc%2Faws-codestarconnection)

[![View on Construct Hub](https://constructs.dev/badge?package=%40jttc%2Faws-codestarconnection)](https://constructs.dev/packages/@jttc/aws-codestarconnection)

# AWS CodeStar Connection Construct Library

This package contains constructs for working with Amazon CodeStar Connection.

## CodeStar Connection

Define a Codestar Connection by creating a new instance of CodeStarConnection. You can create a connection for different providers

```python
const codestartConnection = new CodeStarConnection(
  this,
  'CodeStarConnection',
    {
      connectionName: 'github-connection',
      providerType: CodeStarConnectionProviderType.GITHUB,
    }
  );
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@jttc/aws-codestarconnection.CodeStarConnectionPolicyActions")
class CodeStarConnectionPolicyActions(enum.Enum):
    '''Actions defined by AWS CodeStar Connections Service prefix: codestar-connections.

    The Resource Type indicates whether each action supports resource-level permissions.
    If there is no value, you must specify all resources ("*") to which the policy applies
    in the Resource element of your policy statement

    The Condition Keys includes keys that you can specify in a policy statement's Condition element
    '''

    CREATE_CONNECTION = "CREATE_CONNECTION"
    '''Grants permission to create a Connection resource.

    :accessLevel: Write
    :conditionKeys: codestar-connections:ProviderType
    '''
    CREATE_HOST = "CREATE_HOST"
    '''Grants permission to create a Host resource.

    :accessLevel: Write
    :conditionKeys: codestar-connections:ProviderType
    '''
    DELETE_CONNECTION = "DELETE_CONNECTION"
    '''Grants permission to delete a Connection resource.

    :accessLevel: Write
    :resourceTypes: arn:${Partition}:codestar-connections:${Region}:${Account}:connection/${ConnectionId} (Required)
    '''
    DELETE_HOST = "DELETE_HOST"
    '''Grants permission to delete a host resource.

    :accessLevel: Write
    :resourceTypes: arn:${Partition}:codestar-connections:${Region}:${Account}:host/${HostId} (Required)
    '''
    GET_CONNECTION = "GET_CONNECTION"
    '''Grants permission to get details about a Connection resource.

    :accessLevel: Read
    :resourceTypes: arn:${Partition}:codestar-connections:${Region}:${Account}:connection/${ConnectionId} (Required)
    '''
    GET_HOST = "GET_HOST"
    '''Grants permission to get details about a host resource.

    :accessLevel: Read
    :resourceTypes: arn:${Partition}:codestar-connections:${Region}:${Account}:host/${HostId} (Required)
    '''
    GET_INDIVIDUAL_ACCESS_TOKEN = "GET_INDIVIDUAL_ACCESS_TOKEN"
    '''Grants permission to associate a third party, such as a Bitbucket App installation, with a Connection.

    :accessLevel: Read
    :conditionKeys: codestar-connections:ProviderType
    :dependsOn: codestar-connections:StarOAuthHandshake
    '''
    GET_INSTALLATION_URL_FOR_APP = "GET_INSTALLATION_URL_FOR_APP"
    '''Grants permission to associate a third party, such as a Bitbucket App installation, with a Connection.

    :accessLevel: Read
    :conditionKeys: codestar-connections:ProviderType
    :dependsOn: codestar-connections:StarOAuthHandshake
    '''
    GET_INSTALLATION_URL_FOR_HOST = "GET_INSTALLATION_URL_FOR_HOST"
    '''Grants permission to get the URL to authorize an installation in a third party app.

    :accessLevel: Read
    :conditionKeys: codestar-connections:ProviderType
    :dependsOn: codestar-connections:StarOAuthHandshake
    '''
    GET_INSTALLATION_URL = "GET_INSTALLATION_URL"
    '''Grants permission to get the URL to authorize an installation in a third party app.

    :accessLevel: Read
    :conditionKeys: codestar-connections:ProviderType
    '''
    LIST_CONNECTIONS = "LIST_CONNECTIONS"
    '''Grants permission to list Connection resources.

    :accessLevel: List
    :conditionKeys: codestar-connections:ProviderTypeFilter
    '''
    LIST_HOSTS = "LIST_HOSTS"
    '''Grants permission to list host resources.

    :accessLevel: List
    :conditionKeys: codestar-connections:ProviderTypeFilter
    '''
    LIST_INDIVIDUAL_ACCESS_TOKENS = "LIST_INDIVIDUAL_ACCESS_TOKENS"
    '''Grants permission to list individual access token.

    :accessLevel: List
    '''
    LIST_INSTALLATIONS = "LIST_INSTALLATIONS"
    '''Grants permission to list installations.

    :accessLevel: List
    '''
    LIST_INSTALLATION_TARGETS = "LIST_INSTALLATION_TARGETS"
    '''Grants permission to associate a third party, such as a Bitbucket App installation, with a Connection.

    :accessLevel: List
    :dependsOn: codestar-connections:StarOAuthHandshake
    :dependson: codestar-connections:GetIndividualAccessToken
    '''
    LIST_PASS_CONNECTIONS = "LIST_PASS_CONNECTIONS"
    '''Grants permission to list pass connections.

    :accessLevel: List
    '''
    LIST_TAGS_FOR_RESOURCE = "LIST_TAGS_FOR_RESOURCE"
    '''Grants permission to the set of key-value pairs that are used to manage the resource.

    :accessList: List
    :resouceTypes: arn:${Partition}:codestar-connections:${Region}:${Account}:connection/${ConnectionId} (Required)
    '''
    PASS_CONNECTION = "PASS_CONNECTION"
    '''Grants permission to pass a Connection resource to an AWS service that accepts a Connection ARN as input, such as codepipeline:CreatePipeline.

    :accessLevel: Read
    :conditionKeys: codestar-connections:PassToService
    :resourceTypes: arn:${Partition}:codestar-connections:${Region}:${Account}:connection/${ConnectionId}
    '''
    REGISTER_APP_CODE = "REGISTER_APP_CODE"
    '''Grants permission to associate a third party server, such as a GitHub Enterprise Server instance, with a Host.

    :accessLevel: Read
    :conditionKeys: codestar-connections:HostArn
    '''
    START_APP_REGISTRATION_HANDSHAKE = "START_APP_REGISTRATION_HANDSHAKE"
    '''Grants permission to associate a third party server, such as a GitHub Enterprise Server instance, with a Host.

    :accessLevel: Read
    :conditionKeys: codestar-connections:HostArn
    '''
    START_OAUTH_HANDSHAKE = "START_OAUTH_HANDSHAKE"
    '''Grants permission to associate a third party, such as a Bitbucket App installation, with a Connection.

    :accessLevel: Read
    :conditionKeys: codestar-connections:ProviderType
    '''
    TAG_RESOURCE = "TAG_RESOURCE"
    '''Grants permission to add or modify the tags of the given resource.

    :accessLevel: Tagging
    :conditionKeys: aws:TagKeys
    :resourceTypes: arn:${Partition}:codestar-connections:${Region}:${Account}:connection/${ConnectionId} (Required)
    '''
    UNTAG_RESOURCE = "UNTAG_RESOURCE"
    '''Grants permission to remove tags from an AWS resource.

    :accessLevel: Tagging
    :conditionKeys: aws:TagKeys
    :resourceTypes: arn:${Partition}:codestar-connections:${Region}:${Account}:connection/${ConnectionId} (Required)
    '''
    UPDATE_CONNECTION_INSTALLATION = "UPDATE_CONNECTION_INSTALLATION"
    '''Grants permission to update a Connection resource with an installation of the CodeStar Connections App.

    :accessLevel: Write
    :conditionKeys: codestar-connections:InstallationId
    :dependsOn: codestar-connections:ListInstallationTargets
    :resourceTypes: arn:${Partition}:codestar-connections:${Region}:${Account}:connection/${ConnectionId} (Required)
    '''
    UPDATE_HOST = "UPDATE_HOST"
    '''Grants permission to update a host resource.

    :accessLevel: Write
    :resourceTypes: arn:${Partition}:codestar-connections:${Region}:${Account}:host/${HostId} (Required)
    '''
    USE_CONNECTION = "USE_CONNECTION"
    '''Grants permission to use a Connection resource to call provider actions.

    :accessLevel: Read
    :conditionKeys: codestar-connections:ProviderPermissionsRequired
    :resourceTypes: arn:${Partition}:codestar-connections:${Region}:${Account}:connection/${ConnectionId} (Required)
    '''


@jsii.data_type(
    jsii_type="@jttc/aws-codestarconnection.CodeStarConnectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_name": "connectionName",
        "provider_type": "providerType",
        "host_arn": "hostArn",
        "removal_policy": "removalPolicy",
        "tags": "tags",
    },
)
class CodeStarConnectionProps:
    def __init__(
        self,
        *,
        connection_name: builtins.str,
        provider_type: "CodeStarConnectionProviderType",
        host_arn: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
    ) -> None:
        '''
        :param connection_name: The name of the connection. Connection names must be in an AWS user account.
        :param provider_type: The type of the connection.
        :param host_arn: The Amazon Resource Name (ARN) of the host associated with the connection.
        :param removal_policy: Determine what happens to the code star connection when the resource/stack is deleted. Default: RemovalPolicy.Retain
        :param tags: The list of tags associated with the connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7847716ba0925c5dd74ebfe129fe9db61e6ebb7f70f980f24a8036d9411d1aa4)
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument host_arn", value=host_arn, expected_type=type_hints["host_arn"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_name": connection_name,
            "provider_type": provider_type,
        }
        if host_arn is not None:
            self._values["host_arn"] = host_arn
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connection_name(self) -> builtins.str:
        '''The name of the connection.

        Connection names must be in an AWS user account.
        '''
        result = self._values.get("connection_name")
        assert result is not None, "Required property 'connection_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_type(self) -> "CodeStarConnectionProviderType":
        '''The type of the connection.'''
        result = self._values.get("provider_type")
        assert result is not None, "Required property 'provider_type' is missing"
        return typing.cast("CodeStarConnectionProviderType", result)

    @builtins.property
    def host_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the host associated with the connection.'''
        result = self._values.get("host_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Determine what happens to the code star connection when the resource/stack is deleted.

        :default: RemovalPolicy.Retain
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]]:
        '''The list of tags associated with the connection.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeStarConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@jttc/aws-codestarconnection.CodeStarConnectionProviderType")
class CodeStarConnectionProviderType(enum.Enum):
    '''Connection Provider Type supported.'''

    GITHUB = "GITHUB"
    '''Github provider.'''
    GITHUB_ENTERPRISE = "GITHUB_ENTERPRISE"
    '''Github Entrprise provider.'''
    GITLAB = "GITLAB"
    '''Gitlab Provider.'''
    BITBUCKET = "BITBUCKET"
    '''Bitbucket Provider.'''


@jsii.data_type(
    jsii_type="@jttc/aws-codestarconnection.GithubCodeStarConnetionProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_name": "connectionName",
        "host_arn": "hostArn",
        "removal_policy": "removalPolicy",
        "tags": "tags",
    },
)
class GithubCodeStarConnetionProps:
    def __init__(
        self,
        *,
        connection_name: typing.Optional[builtins.str] = None,
        host_arn: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
    ) -> None:
        '''
        :param connection_name: The name of the connection. Connection names must be in an AWS user account.
        :param host_arn: The Amazon Resource Name (ARN) of the host associated with the connection.
        :param removal_policy: Determine what happens to the code star connection when the resource/stack is deleted. Default: RemovalPolicy.Retain
        :param tags: The list of tags associated with the connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dcc2624269370f2c124f4b5bfc5daafa6160fa033fdfa005c9d792136c79712)
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument host_arn", value=host_arn, expected_type=type_hints["host_arn"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if host_arn is not None:
            self._values["host_arn"] = host_arn
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''The name of the connection.

        Connection names must be in an AWS user account.
        '''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the host associated with the connection.'''
        result = self._values.get("host_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Determine what happens to the code star connection when the resource/stack is deleted.

        :default: RemovalPolicy.Retain
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]]:
        '''The list of tags associated with the connection.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubCodeStarConnetionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@jttc/aws-codestarconnection.ICodeStarConnection")
class ICodeStarConnection(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''The ARN of the connection.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        '''The name of the connection.

        Connection names must be in an AWS user account.
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given principal identity permissions to perform the actions on this code star connection.

        :param grantee: -
        :param actions: -
        '''
        ...

    @jsii.member(jsii_name="grantAdmin")
    def grant_admin(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given identity full access to AWS CodeStar Connections so that the user can add, update, and delete connections.

        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="grantConnectionFullAccess")
    def grant_connection_full_access(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given identity permission to connection full access to the code star connection.

        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''you want to grant an IAM user in your account read-only access to the connections in your AWS account.

        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="grantUse")
    def grant_use(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given identity permissions to use this code start connection.

        :param grantee: -
        '''
        ...


class _ICodeStarConnectionProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@jttc/aws-codestarconnection.ICodeStarConnection"

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''The ARN of the connection.'''
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        '''The name of the connection.

        Connection names must be in an AWS user account.
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given principal identity permissions to perform the actions on this code star connection.

        :param grantee: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0966f180b96f92b3e3bc9cd2b279772fee93a57fbbd4f8c5b986da05201cb451)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantAdmin")
    def grant_admin(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given identity full access to AWS CodeStar Connections so that the user can add, update, and delete connections.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f988591e453ae9144b7c658947c2be69c3cfb38a8168ab95900fa3255979f43)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantAdmin", [grantee]))

    @jsii.member(jsii_name="grantConnectionFullAccess")
    def grant_connection_full_access(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given identity permission to connection full access to the code star connection.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1873a9f22e7556f229d90a4271a0a931257273b53c090b1d7536201c329cf90f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantConnectionFullAccess", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''you want to grant an IAM user in your account read-only access to the connections in your AWS account.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__866f08231c79fee023c45df42f1f494396c07192f6f0bd2621c51db271afc003)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantUse")
    def grant_use(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given identity permissions to use this code start connection.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88ecbe4ab88f7e13a088b02d751d3af23a733e1173b37f4c07c06ce557dda85)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantUse", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICodeStarConnection).__jsii_proxy_class__ = lambda : _ICodeStarConnectionProxy


@jsii.implements(ICodeStarConnection)
class CodeStarConnectionBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@jttc/aws-codestarconnection.CodeStarConnectionBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9af88b8cd6808d14a5e6dc0350093ec328bc001696e8951a22ac3cff1d69738)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given principal identity permissions to perform the actions on this code star connection.

        :param grantee: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e980ce7942d1afe3410df1e215a2462f3247f06ea976f46b0c2f5853da4c0f29)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantAdmin")
    def grant_admin(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''you want to grant an IAM user in your AWS account full access to AWS CodeStar Connections, so that the user can add, update, and delete connections.

        :param grantee: -

        :see: https://docs.aws.amazon.com/dtconsole/latest/userguide/security_iam_id-based-policy-examples-connections.html#security_iam_id-based-policy-examples-connections-fullaccess
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8e763de58bc6cf224bb5deb75058bd014b81df8c062daf49b6c085a1296013)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantAdmin", [grantee]))

    @jsii.member(jsii_name="grantConnectionFullAccess")
    def grant_connection_full_access(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given identity permission to full access to the code star connection.

        :param grantee: -

        :see: https://docs.aws.amazon.com/dtconsole/latest/userguide/security_iam_id-based-policy-examples-connections.html#security_iam_id-based-policy-examples-connections-clisdk
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89374aed189b7f5d7d747b5ac9795d9ab34f374cfd88b389966e708b565515b3)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantConnectionFullAccess", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''you want to grant an IAM user in your account read-only access to the connections in your AWS account.

        :param grantee: -

        :see: https://docs.aws.amazon.com/dtconsole/latest/userguide/security_iam_id-based-policy-examples-connections.html#security_iam_id-based-policy-examples-connections-readonly
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea47c27438b3e701adf8c26c78d268527d207a662a0e5ba573d29883f2fa8109)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantUse")
    def grant_use(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given identity permissions to use this code star connetion.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d52a58d65d65cbc0639615f6400b68942f41fb78c71d0ef7e68b5bb00cbfefa)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantUse", [grantee]))

    @jsii.member(jsii_name="validateConnectionName")
    def validate_connection_name(self, name: builtins.str) -> None:
        '''Validate if the name of the code connection is longer thatn 32 characters.

        :param name: Name of the connection.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-connectionname
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc7de1f12d04734efd6c0a59f7e4a14b02437dc241e626be7189b92ca65f1e7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(None, jsii.invoke(self, "validateConnectionName", [name]))

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    @abc.abstractmethod
    def connection_arn(self) -> builtins.str:
        '''The ARN of the Code Star connection.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    @abc.abstractmethod
    def connection_name(self) -> builtins.str:
        '''The name of the Code Star connection.'''
        ...


class _CodeStarConnectionBaseProxy(
    CodeStarConnectionBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''The ARN of the Code Star connection.'''
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        '''The name of the Code Star connection.'''
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, CodeStarConnectionBase).__jsii_proxy_class__ = lambda : _CodeStarConnectionBaseProxy


class GithubCodeStarConnection(
    CodeStarConnectionBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@jttc/aws-codestarconnection.GithubCodeStarConnection",
):
    '''Define a Github CodeStar Connection resource.

    :resource: AWS::CodeStarConnections::Connection

    Example::

          new GithubCodeStarConnection(this, 'GithubConnection')
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        connection_name: typing.Optional[builtins.str] = None,
        host_arn: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param connection_name: The name of the connection. Connection names must be in an AWS user account.
        :param host_arn: The Amazon Resource Name (ARN) of the host associated with the connection.
        :param removal_policy: Determine what happens to the code star connection when the resource/stack is deleted. Default: RemovalPolicy.Retain
        :param tags: The list of tags associated with the connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171557b3993a6a6ff8ea2b09de3dce634d4d3693ccdf21a3853a9e56af9102b2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GithubCodeStarConnetionProps(
            connection_name=connection_name,
            host_arn=host_arn,
            removal_policy=removal_policy,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromCodeStarConnectionArn")
    @builtins.classmethod
    def from_code_star_connection_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        codestar_connection_arn: builtins.str,
    ) -> ICodeStarConnection:
        '''Import an externally defined Code Star Connection using its ARN.

        :param scope: the construct that will "own" the imported key.
        :param id: the id of the imported code star conection in the construct tree.
        :param codestar_connection_arn: the ARN of an existing Code Star Connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b336b2e4d3965c72fc4ce518ea84f32155ba3940b86c32a91b338589d9c0e1e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument codestar_connection_arn", value=codestar_connection_arn, expected_type=type_hints["codestar_connection_arn"])
        return typing.cast(ICodeStarConnection, jsii.sinvoke(cls, "fromCodeStarConnectionArn", [scope, id, codestar_connection_arn]))

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''The ARN of the Code Star connection.'''
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        '''The name of the CodeStar connection.'''
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))


class CodeStarConnection(
    CodeStarConnectionBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@jttc/aws-codestarconnection.CodeStarConnection",
):
    '''Define a CodeStar Connection resource.

    :resource: AWS::CodeStarConnections::Connection

    Example::

          new CodeStarConnection(this, 'MyConnection', {
            connectionName: 'MyConnection',
            providerType: 'GitHub',
            tags: [{
              key: 'key',
              value: 'value',
            }],
          }
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        connection_name: builtins.str,
        provider_type: CodeStarConnectionProviderType,
        host_arn: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param connection_name: The name of the connection. Connection names must be in an AWS user account.
        :param provider_type: The type of the connection.
        :param host_arn: The Amazon Resource Name (ARN) of the host associated with the connection.
        :param removal_policy: Determine what happens to the code star connection when the resource/stack is deleted. Default: RemovalPolicy.Retain
        :param tags: The list of tags associated with the connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb824a5a937ef06145234141dfd459b17d6f6a6443ad01a9561bc666d2948e6c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CodeStarConnectionProps(
            connection_name=connection_name,
            provider_type=provider_type,
            host_arn=host_arn,
            removal_policy=removal_policy,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromCodeStarConnectionArn")
    @builtins.classmethod
    def from_code_star_connection_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        codestar_connection_arn: builtins.str,
    ) -> ICodeStarConnection:
        '''Import an externally defined Code Star Connection using its ARN.

        :param scope: the construct that will "own" the imported key.
        :param id: the id of the imported code star conection in the construct tree.
        :param codestar_connection_arn: the ARN of an existing Code Star Connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d51f402c4edaf541736229b27d7176639f7b9fd67a19d6ef302d14831efdd5f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument codestar_connection_arn", value=codestar_connection_arn, expected_type=type_hints["codestar_connection_arn"])
        return typing.cast(ICodeStarConnection, jsii.sinvoke(cls, "fromCodeStarConnectionArn", [scope, id, codestar_connection_arn]))

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''The ARN of the Code Star connection.'''
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        '''The name of the Code Star connection.'''
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))


__all__ = [
    "CodeStarConnection",
    "CodeStarConnectionBase",
    "CodeStarConnectionPolicyActions",
    "CodeStarConnectionProps",
    "CodeStarConnectionProviderType",
    "GithubCodeStarConnection",
    "GithubCodeStarConnetionProps",
    "ICodeStarConnection",
]

publication.publish()

def _typecheckingstub__7847716ba0925c5dd74ebfe129fe9db61e6ebb7f70f980f24a8036d9411d1aa4(
    *,
    connection_name: builtins.str,
    provider_type: CodeStarConnectionProviderType,
    host_arn: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dcc2624269370f2c124f4b5bfc5daafa6160fa033fdfa005c9d792136c79712(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    host_arn: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0966f180b96f92b3e3bc9cd2b279772fee93a57fbbd4f8c5b986da05201cb451(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f988591e453ae9144b7c658947c2be69c3cfb38a8168ab95900fa3255979f43(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1873a9f22e7556f229d90a4271a0a931257273b53c090b1d7536201c329cf90f(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866f08231c79fee023c45df42f1f494396c07192f6f0bd2621c51db271afc003(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88ecbe4ab88f7e13a088b02d751d3af23a733e1173b37f4c07c06ce557dda85(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9af88b8cd6808d14a5e6dc0350093ec328bc001696e8951a22ac3cff1d69738(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e980ce7942d1afe3410df1e215a2462f3247f06ea976f46b0c2f5853da4c0f29(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8e763de58bc6cf224bb5deb75058bd014b81df8c062daf49b6c085a1296013(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89374aed189b7f5d7d747b5ac9795d9ab34f374cfd88b389966e708b565515b3(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea47c27438b3e701adf8c26c78d268527d207a662a0e5ba573d29883f2fa8109(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d52a58d65d65cbc0639615f6400b68942f41fb78c71d0ef7e68b5bb00cbfefa(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc7de1f12d04734efd6c0a59f7e4a14b02437dc241e626be7189b92ca65f1e7(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171557b3993a6a6ff8ea2b09de3dce634d4d3693ccdf21a3853a9e56af9102b2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    connection_name: typing.Optional[builtins.str] = None,
    host_arn: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b336b2e4d3965c72fc4ce518ea84f32155ba3940b86c32a91b338589d9c0e1e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    codestar_connection_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb824a5a937ef06145234141dfd459b17d6f6a6443ad01a9561bc666d2948e6c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    connection_name: builtins.str,
    provider_type: CodeStarConnectionProviderType,
    host_arn: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d51f402c4edaf541736229b27d7176639f7b9fd67a19d6ef302d14831efdd5f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    codestar_connection_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
