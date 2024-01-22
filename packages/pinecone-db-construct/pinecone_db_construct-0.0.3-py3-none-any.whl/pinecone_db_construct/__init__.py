'''
![Pinecone DB Icon](https://avatars.githubusercontent.com/u/54333248?s=200&v=4)

# Pinecone DB Construct for AWS CDK

[![CI](https://github.com/petterle-endeavors/pinecone-db-construct/workflows/build/badge.svg)](https://github.com/petterle-endeavors/pinecone-db-construct/actions?query=workflow%3Abuild+event%3Apush+branch%3Amain)
[![NPM version](https://img.shields.io/npm/v/pinecone-db-construct.svg)](https://www.npmjs.com/package/pinecone-db-construct)
[![PyPI version](https://img.shields.io/pypi/v/pinecone-db-construct.svg)](https://pypi.org/project/pinecone-db-construct/)
[![License](https://img.shields.io/github/license/petterle-endeavors/pinecone-db-construct.svg)](https://github.com/petterle-endeavors/pinecone-db-construct/blob/main/LICENSE)

The Pinecone DB Construct for AWS CDK is a JSII-constructed library that simplifies the creation and management of Pinecone indexes in your AWS infrastructure. It allows you to define, configure, and orchestrate your vector database resources alongside your AWS resources within your CDK application.

## Features

* Define Pinecone index configurations in code using familiar AWS CDK constructs.
* Automate the setup and configuration of Pinecone resources with AWS Lambda and AWS Secrets Manager.
* Seamlessly integrate Pinecone DB into your cloud-native applications.
* Supports ARM serverless for deployments

## Installation

Install this construct library using npm or pip, depending on your development language:

For TypeScript/JavaScript users:

```bash
npm install pinecone-db-construct
```

For Python users:

```bash
pip install pinecone-db-construct
```

## Usage

### TypeScript

Below is an example demonstrating how to use the Pinecone DB Construct in a TypeScript CDK application:

```python
import { App, RemovalPolicy, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { PineconeIndex, PineConeEnvironment } from '../index';

class MyStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    new PineconeIndex(
      this,
      'PineconeIndex',
      {
        indexSettings: [{
          apiKeySecretName: 'pinecone-test',
          environment: PineConeEnvironment.GCP_STARTER,
          dimension: 128,
          removalPolicy: RemovalPolicy.SNAPSHOT,
        }],
        customResourceSettings: {
          numAttemptsToRetryOperation: 2,
        },
      },
    );
  }
}

const APP = new App();

new MyStack(APP, 'MyStack');

APP.synth();
```

### Python

For CDK applications written in Python, you can use the construct as shown:

```python
from aws_cdk import (
    App,
    RemovalPolicy,
    Stack,
    StackProps
)
from constructs import Construct
from pinecone_db_construct import PineconeIndex, PineConeEnvironment  # Assuming these exist in the ../index file relative to this file

class MyStack(Stack):
    def __init__(self, scope: Construct, id: str, props: StackProps = None):
        super().__init__(scope, id, props)

        PineconeIndex(
            self,
            'PineconeIndex',
            index_settings=[{
                'api_key_secret_name': 'pinecone-test',
                'environment': PineConeEnvironment.GCP_STARTER,
                'dimension': 128,
                'removal_policy': RemovalPolicy.SNAPSHOT,
            }],
            custom_resource_settings={
                'num_attempts_to_retry_operation': 2,
            }
        )

APP = App()

MyStack(APP, 'MyStack')

APP.synth()
```

## Common Issues

If running the default ARM deployment architecture and deploying on an x86_64 machine, you may run into the dreaded `exec /bin/sh: exec format error`, if this happens you have two options:

1. Switch to x86 architecture (Lame 😒):

```
new PineconeIndex(
this,
'PineconeIndex',
{
  deploymentSettings: {
    deploymentArchitecture: lambda.Architecture.X86_64,
  },
  .
  .
  .
})
```

1. Allow docker to emulate ARM (Better 💪):

```
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

**Note:** first time bundling will be slower when running in emulation mode, so keep that in mind (adds about 40 sec for first time deployment). **Most most CICD environments will do this for you (github actions) with do this emulation out of the box for you.**

## Contributing

We welcome contributions, feedback, and bug reports. Before you contribute, please read our [contributing guidelines](CONTRIBUTING.md).

## Reporting Security Vulnerabilities

If you find a security issue, please contact us at [security@example.com](mailto:security@example.com). We take all security bugs seriously. Thank you for improving the security of our project.
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
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="pinecone-db-construct.DeploymentSettings",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_architecture": "deploymentArchitecture",
        "num_attempts_to_retry_operation": "numAttemptsToRetryOperation",
    },
)
class DeploymentSettings:
    def __init__(
        self,
        *,
        deployment_architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        num_attempts_to_retry_operation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param deployment_architecture: 
        :param num_attempts_to_retry_operation: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd75f29bfc60c3d9c029b70375017d9d216a4ced3184c1c2c69ccce79866f4d)
            check_type(argname="argument deployment_architecture", value=deployment_architecture, expected_type=type_hints["deployment_architecture"])
            check_type(argname="argument num_attempts_to_retry_operation", value=num_attempts_to_retry_operation, expected_type=type_hints["num_attempts_to_retry_operation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deployment_architecture is not None:
            self._values["deployment_architecture"] = deployment_architecture
        if num_attempts_to_retry_operation is not None:
            self._values["num_attempts_to_retry_operation"] = num_attempts_to_retry_operation

    @builtins.property
    def deployment_architecture(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture]:
        '''
        :stability: experimental
        '''
        result = self._values.get("deployment_architecture")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture], result)

    @builtins.property
    def num_attempts_to_retry_operation(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("num_attempts_to_retry_operation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="pinecone-db-construct.DistanceMetric")
class DistanceMetric(enum.Enum):
    '''
    :stability: experimental
    '''

    EUCLIDEAN = "EUCLIDEAN"
    '''
    :stability: experimental
    '''
    COSINE = "COSINE"
    '''
    :stability: experimental
    '''
    DOT_PRODUCT = "DOT_PRODUCT"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="pinecone-db-construct.MetaDataConfig",
    jsii_struct_bases=[],
    name_mapping={"indexed": "indexed"},
)
class MetaDataConfig:
    def __init__(self, *, indexed: typing.Sequence[builtins.str]) -> None:
        '''
        :param indexed: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703cdbf87e4a2a62babe7a970e79bb65b232417c4ba3db417e7ae1644840697c)
            check_type(argname="argument indexed", value=indexed, expected_type=type_hints["indexed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "indexed": indexed,
        }

    @builtins.property
    def indexed(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("indexed")
        assert result is not None, "Required property 'indexed' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetaDataConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="pinecone-db-construct.PineConeEnvironment")
class PineConeEnvironment(enum.Enum):
    '''
    :stability: experimental
    '''

    GCP_STARTER = "GCP_STARTER"
    '''
    :stability: experimental
    '''
    GCP_FREE_US_WEST_1 = "GCP_FREE_US_WEST_1"
    '''
    :stability: experimental
    '''
    GCP_FREE_ASIA_SOUTHEAST_1 = "GCP_FREE_ASIA_SOUTHEAST_1"
    '''
    :stability: experimental
    '''
    GCP_FREE_US_WEST_4 = "GCP_FREE_US_WEST_4"
    '''
    :stability: experimental
    '''
    GCP_STD_US_WEST_1 = "GCP_STD_US_WEST_1"
    '''
    :stability: experimental
    '''
    GCP_STD_US_CENTRAL_1 = "GCP_STD_US_CENTRAL_1"
    '''
    :stability: experimental
    '''
    GCP_STD_US_WEST_4 = "GCP_STD_US_WEST_4"
    '''
    :stability: experimental
    '''
    GCP_STD_US_EAST_4 = "GCP_STD_US_EAST_4"
    '''
    :stability: experimental
    '''
    GCP_STD_NORTH_AMERICA_NORTHEAST_1 = "GCP_STD_NORTH_AMERICA_NORTHEAST_1"
    '''
    :stability: experimental
    '''
    GCP_STD_ASIA_NORTHEAST_1 = "GCP_STD_ASIA_NORTHEAST_1"
    '''
    :stability: experimental
    '''
    GCP_STD_ASIA_SOUTHEAST_1 = "GCP_STD_ASIA_SOUTHEAST_1"
    '''
    :stability: experimental
    '''
    GCP_STD_US_EAST_1 = "GCP_STD_US_EAST_1"
    '''
    :stability: experimental
    '''
    GCP_STD_EU_WEST_1 = "GCP_STD_EU_WEST_1"
    '''
    :stability: experimental
    '''
    GCP_STD_EU_WEST_4 = "GCP_STD_EU_WEST_4"
    '''
    :stability: experimental
    '''
    AWS_STD_US_EAST_1 = "AWS_STD_US_EAST_1"
    '''
    :stability: experimental
    '''
    AZURE_STD_EAST_US = "AZURE_STD_EAST_US"
    '''
    :stability: experimental
    '''


class PineconeIndex(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="pinecone-db-construct.PineconeIndex",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        index_settings: typing.Sequence[typing.Union["PineconeIndexSettings", typing.Dict[builtins.str, typing.Any]]],
        deployment_settings: typing.Optional[typing.Union[DeploymentSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param index_settings: 
        :param deployment_settings: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849db0e4f72c5e817e872757142ee29b956f7175d719d0dad401a3b9866a37eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PineconeIndexProps(
            index_settings=index_settings, deployment_settings=deployment_settings
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="pinecone-db-construct.PineconeIndexProps",
    jsii_struct_bases=[],
    name_mapping={
        "index_settings": "indexSettings",
        "deployment_settings": "deploymentSettings",
    },
)
class PineconeIndexProps:
    def __init__(
        self,
        *,
        index_settings: typing.Sequence[typing.Union["PineconeIndexSettings", typing.Dict[builtins.str, typing.Any]]],
        deployment_settings: typing.Optional[typing.Union[DeploymentSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param index_settings: 
        :param deployment_settings: 

        :stability: experimental
        '''
        if isinstance(deployment_settings, dict):
            deployment_settings = DeploymentSettings(**deployment_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3724d39ea9b603c4e8e256ab08b7852c7519ec580ff3297b206263c6ca7303)
            check_type(argname="argument index_settings", value=index_settings, expected_type=type_hints["index_settings"])
            check_type(argname="argument deployment_settings", value=deployment_settings, expected_type=type_hints["deployment_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "index_settings": index_settings,
        }
        if deployment_settings is not None:
            self._values["deployment_settings"] = deployment_settings

    @builtins.property
    def index_settings(self) -> typing.List["PineconeIndexSettings"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("index_settings")
        assert result is not None, "Required property 'index_settings' is missing"
        return typing.cast(typing.List["PineconeIndexSettings"], result)

    @builtins.property
    def deployment_settings(self) -> typing.Optional[DeploymentSettings]:
        '''
        :stability: experimental
        '''
        result = self._values.get("deployment_settings")
        return typing.cast(typing.Optional[DeploymentSettings], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PineconeIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="pinecone-db-construct.PineconeIndexSettings",
    jsii_struct_bases=[],
    name_mapping={
        "api_key_secret_name": "apiKeySecretName",
        "dimension": "dimension",
        "environment": "environment",
        "metadata_config": "metadataConfig",
        "metric": "metric",
        "name": "name",
        "pod_instance_type": "podInstanceType",
        "pods": "pods",
        "pod_size": "podSize",
        "removal_policy": "removalPolicy",
        "replicas": "replicas",
        "source_collection": "sourceCollection",
    },
)
class PineconeIndexSettings:
    def __init__(
        self,
        *,
        api_key_secret_name: builtins.str,
        dimension: jsii.Number,
        environment: PineConeEnvironment,
        metadata_config: typing.Optional[typing.Union[MetaDataConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[DistanceMetric] = None,
        name: typing.Optional[builtins.str] = None,
        pod_instance_type: typing.Optional["PodType"] = None,
        pods: typing.Optional[jsii.Number] = None,
        pod_size: typing.Optional["PodSize"] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        replicas: typing.Optional[jsii.Number] = None,
        source_collection: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_key_secret_name: 
        :param dimension: 
        :param environment: 
        :param metadata_config: 
        :param metric: 
        :param name: 
        :param pod_instance_type: 
        :param pods: 
        :param pod_size: 
        :param removal_policy: 
        :param replicas: 
        :param source_collection: 

        :stability: experimental
        '''
        if isinstance(metadata_config, dict):
            metadata_config = MetaDataConfig(**metadata_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb05d74942d451e05ccc50a5ed24f87df6a80a4d8dc57304c7dd31860b6353a4)
            check_type(argname="argument api_key_secret_name", value=api_key_secret_name, expected_type=type_hints["api_key_secret_name"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument metadata_config", value=metadata_config, expected_type=type_hints["metadata_config"])
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pod_instance_type", value=pod_instance_type, expected_type=type_hints["pod_instance_type"])
            check_type(argname="argument pods", value=pods, expected_type=type_hints["pods"])
            check_type(argname="argument pod_size", value=pod_size, expected_type=type_hints["pod_size"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
            check_type(argname="argument source_collection", value=source_collection, expected_type=type_hints["source_collection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key_secret_name": api_key_secret_name,
            "dimension": dimension,
            "environment": environment,
        }
        if metadata_config is not None:
            self._values["metadata_config"] = metadata_config
        if metric is not None:
            self._values["metric"] = metric
        if name is not None:
            self._values["name"] = name
        if pod_instance_type is not None:
            self._values["pod_instance_type"] = pod_instance_type
        if pods is not None:
            self._values["pods"] = pods
        if pod_size is not None:
            self._values["pod_size"] = pod_size
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if replicas is not None:
            self._values["replicas"] = replicas
        if source_collection is not None:
            self._values["source_collection"] = source_collection

    @builtins.property
    def api_key_secret_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("api_key_secret_name")
        assert result is not None, "Required property 'api_key_secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("dimension")
        assert result is not None, "Required property 'dimension' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def environment(self) -> PineConeEnvironment:
        '''
        :stability: experimental
        '''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(PineConeEnvironment, result)

    @builtins.property
    def metadata_config(self) -> typing.Optional[MetaDataConfig]:
        '''
        :stability: experimental
        '''
        result = self._values.get("metadata_config")
        return typing.cast(typing.Optional[MetaDataConfig], result)

    @builtins.property
    def metric(self) -> typing.Optional[DistanceMetric]:
        '''
        :stability: experimental
        '''
        result = self._values.get("metric")
        return typing.cast(typing.Optional[DistanceMetric], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_instance_type(self) -> typing.Optional["PodType"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pod_instance_type")
        return typing.cast(typing.Optional["PodType"], result)

    @builtins.property
    def pods(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pod_size(self) -> typing.Optional["PodSize"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pod_size")
        return typing.cast(typing.Optional["PodSize"], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''
        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def source_collection(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("source_collection")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PineconeIndexSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="pinecone-db-construct.PodSize")
class PodSize(enum.Enum):
    '''
    :stability: experimental
    '''

    X1 = "X1"
    '''
    :stability: experimental
    '''
    X2 = "X2"
    '''
    :stability: experimental
    '''
    X4 = "X4"
    '''
    :stability: experimental
    '''
    X8 = "X8"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="pinecone-db-construct.PodType")
class PodType(enum.Enum):
    '''
    :stability: experimental
    '''

    S1 = "S1"
    '''
    :stability: experimental
    '''
    P1 = "P1"
    '''
    :stability: experimental
    '''
    P2 = "P2"
    '''
    :stability: experimental
    '''


__all__ = [
    "DeploymentSettings",
    "DistanceMetric",
    "MetaDataConfig",
    "PineConeEnvironment",
    "PineconeIndex",
    "PineconeIndexProps",
    "PineconeIndexSettings",
    "PodSize",
    "PodType",
]

publication.publish()

def _typecheckingstub__7fd75f29bfc60c3d9c029b70375017d9d216a4ced3184c1c2c69ccce79866f4d(
    *,
    deployment_architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    num_attempts_to_retry_operation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703cdbf87e4a2a62babe7a970e79bb65b232417c4ba3db417e7ae1644840697c(
    *,
    indexed: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849db0e4f72c5e817e872757142ee29b956f7175d719d0dad401a3b9866a37eb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    index_settings: typing.Sequence[typing.Union[PineconeIndexSettings, typing.Dict[builtins.str, typing.Any]]],
    deployment_settings: typing.Optional[typing.Union[DeploymentSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3724d39ea9b603c4e8e256ab08b7852c7519ec580ff3297b206263c6ca7303(
    *,
    index_settings: typing.Sequence[typing.Union[PineconeIndexSettings, typing.Dict[builtins.str, typing.Any]]],
    deployment_settings: typing.Optional[typing.Union[DeploymentSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb05d74942d451e05ccc50a5ed24f87df6a80a4d8dc57304c7dd31860b6353a4(
    *,
    api_key_secret_name: builtins.str,
    dimension: jsii.Number,
    environment: PineConeEnvironment,
    metadata_config: typing.Optional[typing.Union[MetaDataConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metric: typing.Optional[DistanceMetric] = None,
    name: typing.Optional[builtins.str] = None,
    pod_instance_type: typing.Optional[PodType] = None,
    pods: typing.Optional[jsii.Number] = None,
    pod_size: typing.Optional[PodSize] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    replicas: typing.Optional[jsii.Number] = None,
    source_collection: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
