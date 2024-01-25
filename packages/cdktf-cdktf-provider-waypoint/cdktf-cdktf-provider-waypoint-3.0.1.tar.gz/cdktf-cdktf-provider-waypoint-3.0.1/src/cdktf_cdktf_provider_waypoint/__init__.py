'''
# CDKTF prebuilt bindings for hashicorp/waypoint provider version 0.1.0

HashiCorp made the decision to stop publishing new versions of prebuilt [Terraform waypoint provider](https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0) bindings for [CDK for Terraform](https://cdk.tf) on January 24, 2024. As such, this repository has been archived and is no longer supported in any way by HashiCorp. Previously-published versions of this prebuilt provider will still continue to be available on their respective package managers (e.g. npm, PyPi, Maven, NuGet), but these will not be compatible with new releases of `cdktf` past `0.20.0` and are no longer eligible for commercial support.

As a reminder, you can continue to use the `hashicorp/waypoint` provider in your CDK for Terraform (CDKTF) projects, even with newer versions of CDKTF, but you will need to generate the bindings locally. The easiest way to do so is to use the [`provider add` command](https://developer.hashicorp.com/terraform/cdktf/cli-reference/commands#provider-add), optionally with the `--force-local` flag enabled:

`cdktf provider add hashicorp/waypoint --force-local`

For more information and additional examples, check out our documentation on [generating provider bindings manually](https://cdk.tf/imports).

## Deprecated Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-waypoint](https://www.npmjs.com/package/@cdktf/provider-waypoint).

`npm install @cdktf/provider-waypoint`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-waypoint](https://pypi.org/project/cdktf-cdktf-provider-waypoint).

`pipenv install cdktf-cdktf-provider-waypoint`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Waypoint](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Waypoint).

`dotnet add package HashiCorp.Cdktf.Providers.Waypoint`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-waypoint](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-waypoint).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-waypoint</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-waypoint-go`](https://github.com/cdktf/cdktf-provider-waypoint-go) package.

`go get github.com/cdktf/cdktf-provider-waypoint-go/waypoint/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-waypoint-go/blob/main/waypoint/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-waypoint).
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

__all__ = [
    "auth_method",
    "config_source",
    "data_waypoint_app",
    "data_waypoint_auth_method",
    "data_waypoint_project",
    "data_waypoint_runner_profile",
    "project",
    "provider",
    "runner_profile",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import auth_method
from . import config_source
from . import data_waypoint_app
from . import data_waypoint_auth_method
from . import data_waypoint_project
from . import data_waypoint_runner_profile
from . import project
from . import provider
from . import runner_profile
