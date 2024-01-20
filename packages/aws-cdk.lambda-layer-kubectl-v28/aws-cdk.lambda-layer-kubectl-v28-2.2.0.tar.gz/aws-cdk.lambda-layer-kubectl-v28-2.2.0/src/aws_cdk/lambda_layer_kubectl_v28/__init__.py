'''
# Lambda Layer with KubeCtl v1.28

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module exports a single class called `KubectlV28Layer` which is a `lambda.LayerVersion` that
bundles the [`kubectl`](https://kubernetes.io/docs/reference/kubectl/kubectl/) and the
[`helm`](https://helm.sh/) command line.

> * Helm Version: 3.14.0
> * Kubectl Version: 1.28.3

Usage:

```python
// KubectlLayer bundles the 'kubectl' and 'helm' command lines
import { KubectlV28Layer } from '@aws-cdk/lambda-layer-kubectl-v28';
import * as lambda from 'aws-cdk-lib/aws-lambda';

declare const fn: lambda.Function;
const kubectl = new KubectlV28Layer(this, 'KubectlLayer');
fn.addLayers(kubectl);
```

`kubectl` will be installed under `/opt/kubectl/kubectl`, and `helm` will be installed under `/opt/helm/helm`.
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

import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


class KubectlV28Layer(
    _aws_cdk_aws_lambda_ceddda9d.LayerVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/lambda-layer-kubectl-v28.KubectlV28Layer",
):
    '''A CDK Asset construct that contains ``kubectl`` and ``helm``.'''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999799084c8c97cfeb26f03bead103bcf1d1fa49b25a7cc380b4b249168c7739)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])


__all__ = [
    "KubectlV28Layer",
]

publication.publish()

def _typecheckingstub__999799084c8c97cfeb26f03bead103bcf1d1fa49b25a7cc380b4b249168c7739(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
