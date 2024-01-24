'''
# CDK fck-nat

A CDK construct for deploying NAT Instances using [fck-nat](https://github.com/AndrewGuenther/fck-nat). The (f)easible (c)ost (k)onfigurable NAT!

* Overpaying for AWS Managed NAT Gateways? fck-nat.
* Want to use NAT instances and stay up-to-date with the latest security patches? fck-nat.
* Want to reuse your Bastion hosts as a NAT? fck-nat.

fck-nat offers a ready-to-use ARM and x86 based AMIs built on Amazon Linux 2 which can support up to 5Gbps NAT traffic
on a t4g.nano instance. How does that compare to a Managed NAT Gateway?

Hourly rates:

* Managed NAT Gateway hourly: $0.045
* t4g.nano hourly: $0.0042

Per GB rates:

* Managed NAT Gateway per GB: $0.045
* fck-nat per GB: $0.00

Sitting idle, fck-nat costs 10% of a Managed NAT Gateway. In practice, the savings are even greater.

*"But what about AWS' NAT Instance AMI?"*

The official AWS supported NAT Instance AMI hasn't been updates since 2018, is still running Amazon Linux 1 which is
now EOL, and has no ARM support, meaning it can't be deployed on EC2's most cost effective instance types. fck-nat.

*"When would I want to use a Managed NAT Gateway instead of fck-nat?"*

AWS limits outgoing internet bandwidth on EC2 instances to 5Gbps. This means that the highest bandwidth that fck-nat
can support is 5Gbps. This is enough to cover a very broad set of use cases, but if you need additional bandwidth,
you should use Managed NAT Gateway. If AWS were to lift the limit on internet egress bandwidth from EC2, you could
cost-effectively operate fck-nat at speeds up to 25Gbps, but you wouldn't need Managed NAT Gateway then would you?
fck-nat.

Read more about EC2 bandwidth limits here: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-network-bandwidth.html
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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d


@jsii.data_type(
    jsii_type="cdk-fck-nat.FckNatInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "key_name": "keyName",
        "machine_image": "machineImage",
        "security_group": "securityGroup",
    },
)
class FckNatInstanceProps:
    def __init__(
        self,
        *,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        key_name: typing.Optional[builtins.str] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    ) -> None:
        '''Properties for a fck-nat instance.

        :param instance_type: Instance type of the fck-nat instance.
        :param key_name: Name of SSH keypair to grant access to instance. Default: - No SSH access will be possible.
        :param machine_image: The machine image (AMI) to use. By default, will do an AMI lookup for the latest fck-nat instance image. If you have a specific AMI ID you want to use, pass a ``GenericLinuxImage``. For example:: FckNatInstanceProvider({ instanceType: new ec2.InstanceType('t3.micro'), machineImage: new LookupMachineImage({ name: 'fck-nat-amzn2-*-arm64-ebs', owners: ['568608671756'], }) }) Default: - Latest fck-nat instance image
        :param security_group: Security Group for fck-nat instances. Default: - A new security group will be created
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4557b0164d909dd1470d454a4f5d57f3ed9a34033b627565f2c5265d5d68c85)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument machine_image", value=machine_image, expected_type=type_hints["machine_image"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
        }
        if key_name is not None:
            self._values["key_name"] = key_name
        if machine_image is not None:
            self._values["machine_image"] = machine_image
        if security_group is not None:
            self._values["security_group"] = security_group

    @builtins.property
    def instance_type(self) -> _aws_cdk_aws_ec2_ceddda9d.InstanceType:
        '''Instance type of the fck-nat instance.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.InstanceType, result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''Name of SSH keypair to grant access to instance.

        :default: - No SSH access will be possible.
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_image(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage]:
        '''The machine image (AMI) to use.

        By default, will do an AMI lookup for the latest fck-nat instance image.

        If you have a specific AMI ID you want to use, pass a ``GenericLinuxImage``. For example::

           FckNatInstanceProvider({
             instanceType: new ec2.InstanceType('t3.micro'),
             machineImage: new LookupMachineImage({
               name: 'fck-nat-amzn2-*-arm64-ebs',
               owners: ['568608671756'],
             })
           })

        :default: - Latest fck-nat instance image
        '''
        result = self._values.get("machine_image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Security Group for fck-nat instances.

        :default: - A new security group will be created
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FckNatInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_ec2_ceddda9d.IConnectable)
class FckNatInstanceProvider(
    _aws_cdk_aws_ec2_ceddda9d.NatProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-fck-nat.FckNatInstanceProvider",
):
    def __init__(
        self,
        *,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        key_name: typing.Optional[builtins.str] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    ) -> None:
        '''
        :param instance_type: Instance type of the fck-nat instance.
        :param key_name: Name of SSH keypair to grant access to instance. Default: - No SSH access will be possible.
        :param machine_image: The machine image (AMI) to use. By default, will do an AMI lookup for the latest fck-nat instance image. If you have a specific AMI ID you want to use, pass a ``GenericLinuxImage``. For example:: FckNatInstanceProvider({ instanceType: new ec2.InstanceType('t3.micro'), machineImage: new LookupMachineImage({ name: 'fck-nat-amzn2-*-arm64-ebs', owners: ['568608671756'], }) }) Default: - Latest fck-nat instance image
        :param security_group: Security Group for fck-nat instances. Default: - A new security group will be created
        '''
        props = FckNatInstanceProps(
            instance_type=instance_type,
            key_name=key_name,
            machine_image=machine_image,
            security_group=security_group,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="configureNat")
    def configure_nat(
        self,
        *,
        nat_subnets: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
        private_subnets: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet],
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    ) -> None:
        '''Called by the VPC to configure NAT.

        Don't call this directly, the VPC will call it automatically.

        :param nat_subnets: The public subnets where the NAT providers need to be placed.
        :param private_subnets: The private subnets that need to route through the NAT providers. There may be more private subnets than public subnets with NAT providers.
        :param vpc: The VPC we're configuring NAT for.
        '''
        options = _aws_cdk_aws_ec2_ceddda9d.ConfigureNatOptions(
            nat_subnets=nat_subnets, private_subnets=private_subnets, vpc=vpc
        )

        return typing.cast(None, jsii.invoke(self, "configureNat", [options]))

    @jsii.member(jsii_name="configureSubnet")
    def configure_subnet(self, subnet: _aws_cdk_aws_ec2_ceddda9d.PrivateSubnet) -> None:
        '''Configures subnet with the gateway.

        Don't call this directly, the VPC will call it automatically.

        :param subnet: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2530e48e0fe57e3382c88c654d9132a4425b047a1cbece5fb1b57592d62710ba)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        return typing.cast(None, jsii.invoke(self, "configureSubnet", [subnet]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMI_NAME")
    def AMI_NAME(cls) -> builtins.str:
        '''The AMI name used internally when calling ``LookupMachineImage``.

        Can be referenced if you wish to do AMI lookups
        externally.
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "AMI_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMI_OWNER")
    def AMI_OWNER(cls) -> builtins.str:
        '''The AMI owner used internally when calling ``LookupMachineImage``.

        Can be referenced if you wish to do AMI lookups
        externally.
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "AMI_OWNER"))

    @builtins.property
    @jsii.member(jsii_name="configuredGateways")
    def configured_gateways(
        self,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.GatewayConfig]:
        '''Return list of gateways spawned by the provider.'''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.GatewayConfig], jsii.get(self, "configuredGateways"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''Manage the Security Groups associated with the NAT instances.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''The Security Group associated with the NAT instances.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "securityGroup"))


__all__ = [
    "FckNatInstanceProps",
    "FckNatInstanceProvider",
]

publication.publish()

def _typecheckingstub__c4557b0164d909dd1470d454a4f5d57f3ed9a34033b627565f2c5265d5d68c85(
    *,
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    key_name: typing.Optional[builtins.str] = None,
    machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2530e48e0fe57e3382c88c654d9132a4425b047a1cbece5fb1b57592d62710ba(
    subnet: _aws_cdk_aws_ec2_ceddda9d.PrivateSubnet,
) -> None:
    """Type checking stubs"""
    pass
