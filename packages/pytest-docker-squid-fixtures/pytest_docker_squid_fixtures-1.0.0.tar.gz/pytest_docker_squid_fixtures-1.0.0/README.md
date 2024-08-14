# pytest-docker-squid-fixtures

[![pypi version](https://img.shields.io/pypi/v/pytest-docker-squid-fixtures.svg)](https://pypi.org/project/pytest-docker-squid-fixtures)
[![build status](https://github.com/crashvb/pytest-docker-squid-fixtures/actions/workflows/main.yml/badge.svg)](https://github.com/crashvb/pytest-docker-squid-fixtures/actions)
[![coverage status](https://coveralls.io/repos/github/crashvb/pytest-docker-squid-fixtures/badge.svg)](https://coveralls.io/github/crashvb/pytest-docker-squid-fixtures)
[![python versions](https://img.shields.io/pypi/pyversions/pytest-docker-squid-fixtures.svg?logo=python&logoColor=FBE072)](https://pypi.org/project/pytest-docker-squid-fixtures)
[![linting](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![license](https://img.shields.io/github/license/crashvb/pytest-docker-squid-fixtures.svg)](https://github.com/crashvb/pytest-docker-squid-fixtures/blob/master/LICENSE.md)

## Overview

Pytest fixtures to instantiate and utilize local squid docker containers, using [lovely-pytest-docker](https://pypi.org/project/lovely-pytest-docker) and [docker-py](https://pypi.org/project/docker-py), for testing.

## Getting Started

Update <tt>setup.py</tt> to include:

```python
from distutils.core import setup

setup(
	tests_require=["pytest-docker-squid-fixtures"]
)
```

All fixtures should be automatically included via the <tt>pytest11</tt> entry point.
```python
import requests
import pytest
from pytest_docker_squid_fixtures import SquidInsecure, SquidSecure  # Optional, for typing

def test_squid_secure(squid_secure: SquidSecure):
    response = requests.head(f"https://{squid_secure.endpoint}/",
        headers=squid_secure.auth_header,
        verify=str(squid_secure.cacerts),
    )
    assert response.status_code == 200

def test_squid_insecure(squid_insecure: SquidInsecure):
    response = requests.head(f"http://{squid_insecure.endpoint}/")
    assert response.status_code == 200
```

The `push_image` mark can optionally be added to stage images in the squid prior to testing. See [Markers](#markers) for details.

## Installation
### From [pypi.org](https://pypi.org/project/pytest-docker-squid-fixtures/)

```
$ pip install pytest_docker_squid_fixtures
```

### From source code

```bash
$ git clone https://github.com/crashvb/pytest-docker-squid-fixtures
$ cd pytest-docker-squid-fixtures
$ virtualenv env
$ source env/bin/activate
$ python -m pip install --editable .[dev]
```

## <a name="fixtures"></a>Fixtures

### <a name="squid_auth_header"></a> squid_auth_header

Retrieves an HTTP basic authentication header that is populated with credentials that can access the secure squid service. The credentials are retrieved from the [squid_password](#squid_password) and [squid_username](#squid_username) fixtures. This fixture is used to replicate docker images into the secure squid service.

### <a name="squid_cacerts"></a> squid_cacerts

Locates a user-defined CA trust store (<tt>tests/cacerts</tt>) to use to verify connections to the secure squid service. If one cannot be located, a temporary trust store is created containing certificates from <tt>certifi</tt> and the [squid_certs](#squid_certs) fixture. This fixture is used to instantiate the secure squid service.

### <a name="squid_certs"></a> squid_certs

Returns the paths of the self-signed certificate authority certificate, certificate, and private key that are used by the secure squid service. This fixture is used to instantiate the secure squid service.

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **ca_certificate** - Path to the self-signed certificate authority certificate.
* **ca_private_key** - Path to the self-signed certificate authority private key.
* **certificate** - Path to the certificate.
* **private_key** - Path to the private key.

Typing is provided by `pytest_docker_squid_fixtures.SquidCerts`.

### <a name="squid_hwpasswd"></a> squid_htpasswd

Provides the path to a htpasswd file that is used by the secure squid service. If a user-defined htpasswd file (<tt>tests/htpasswd</tt>) can be located, it is used. Otherwise, a temporary htpasswd file is created using credentials from the [squid_password](#squid_password) and [squid_username](#squid_username) fixtures. This fixture is used to instantiate the secure squid ervice.

### <a name="squid_squidcfg_insecure"></a> squid_squidcfg_insecure

Provides the path to an insecure squid.cfg file that is used by the insecure squid service. If a user-defined squid.cfg file (<tt>tests/squid.insecure.cfg</tt>) can be located, it is used. Otherwise, an embedded configuration is copied to a temporary location and returned. This fixture is used to instantiate the insecure squid service.

### <a name="squid_squidcfg_secure"></a> squid_squidcfg_secure

Provides the path to a secure squid.cfg file that is used by the secure squid service. If a user-defined squid.cfg file (<tt>tests/squid.secure.cfg</tt>) can be located, it is used. Otherwise, an embedded configuration is copied to a temporary location and returned. This fixture is used to instantiate the secure squid service.

### <a name="squid_insecure"></a> squid_insecure

Configures and instantiates a squid service without TLS or authentication.

```python
import requests
from pytest_docker_squid_fixtures import SquidInsecure  # Optional, for typing

def test_squid_insecure(squid_insecure: SquidInsecure):
    response = requests.head(f"http://{squid_insecure.endpoint}/")
    assert response.status_code == 200
```

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **docker_compose** - Path to the fully instantiated docker-compose configuration.
* **endpoint** - Endpoint of the insecure squid service.
* **endpoint_name** - Endpoint of the insecure squid service, by service name.
* **service_name** - Name of the service within the docker-compose configuration.

Typing is provided by `pytest_docker_squid_fixtures.SquidInsecure`.

### <a name="squid_password"></a> squid_password

Provides a generated password to use for authentication to the secure squid service. This fixture is used to replicate docker images into the secure squid service.

### <a name="squid_secure"></a> squid_secure

Configures and instantiates a TLS enabled squid service with HTTP basic authorization.

```python
import requests
from pytest_docker_squid_fixtures import SquidSecure  # Optional, for typing

def test_squid_secure(squid_secure: SquidSecure):
    response = requests.head(
        f"https://{squid_secure.endpoint}/",
        headers=squid_secure.auth_header,
        verify=str(squid_secure.cacerts),
    )
    assert response.status_code == 200
```

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **auth_header** - from [squid_auth_header](#squid_auth_header).
* **cacerts** - from [squid_cacerts](#squid_cacerts).
* **certs** - from [squid_certs](#squid_certs).
* **docker_compose** - Path to the fully instantiated docker-compose configuration.
* **endpoint** - Endpoint of the secure squid service.
* **endpoint_name** - Endpoint of the secure squid service, by service name.
* **htpasswd** - from [squid_htpasswd](#squid_htpasswd)
* **password** - from [squid_password](#squid_password).
* **service_name** - Name of the service within the docker-compose configuration.
* **ssl_context** - from [squid_ssl_context](#squid_ssl_context).
* **username** - from [squid_username](#squid_username).

Typing is provided by `pytest_docker_squid_fixtures.SquidSecure`.

### <a name="squid_ssl_context"></a> squid_ssl_context

Provides an SSL context containing the CA trust store from the  [squid_cacerts](#squid_cacerts) fixture. This fixture is used to instantiate the secure squid service.

### <a name="squid_username"></a> squid_username

Provides a generated username to use for authentication to the secure squid service. This fixture is used to replicate docker images into the secure squid service.

### <a name="pdsf_docker_compose_insecure"></a> pdsf_docker_compose_insecure

This fixture uses the `docker_compose_files` fixture to locate a user-defined docker-compose configuration file (typically <tt>tests/docker-compose.yml</tt>) that contains the <tt>pytest-docker-squid-insecure</tt> service. If one cannot be located, an embedded configuration is copied to a temporary location and returned. This fixture is used to instantiate the insecure squid service. The configuration will be treated as a template; the <tt>$PATH_SQUIDCFG</tt> token will be populated with the absolute path provided by the [squid_squidcfg](#squid_squidcfg) fixture.

### <a name="pdsf_docker_compose_secure"></a> pdsf_docker_compose_secure

This fixture uses the `docker_compose_files` fixture to locate a user-defined docker-compose configuration file (typically <tt>tests/docker-compose.yml</tt>) that contains the <tt>pytest-docker-squid-secure</tt> service. If one cannot be located, an embedded configuration is copied to a temporary location and returned. This fixture is used to instantiate the secure squid service. The configuration will be treated as a template; the <tt>$PATH_CERTIFICATE</tt>, <tt>$PATH_HTPASSWD</tt>, <tt>$PATH_KEY</tt>, and <tt>$PATH_SQUIDCFG</tt> tokens will be populated with the absolute paths provided by the [squid_certs](#squid_certs), [squid_htpasswd](#squid_htpasswd), and [squid_squidcfg](#squid_squidcfg) fixtures, as appropriate.

## <a name="enumerated_fixtures"></a>Enumerated Fixtures

It is possible to instantiate multiple squid instances using the corresponding enumerated fixtures. All [fixtures](#fixtures) listed above have _*_list_ (e.g. `squid_secure` -> `squid_secure_list`) versions that will return enumerated lists of corresponding data type.

For example:

```python
import requests
from typing import List  # Optional, for typing
from pytest_docker_squid_fixtures import SquidSecure  # Optional, for typing

def test_squid_secure_list(squid_secure_list: List[SquidSecure]):
    for squid_secure in squid_secure_list:
        response = requests.head(
            f"https://{squid_secure.endpoint}/",
            headers=squid_secure.auth_header,
            verify=str(squid_secure.cacerts),
        )
        assert response.status_code == 200
```

It is possible to use both singular and enumerated fixtures within the same test context; however, the same values will be returned for the singular fixture as the first enumerated list value (i.e. squid_secure == squid_secure_list[0]). To avoid complications with lower layers, mainly docker-compose, and to allow for this interchangeability, caching is used internally.

By default, the scale factor of the enumerated instances is set to one (n=1). This value can be changed by overriding the `pdsf_scale_factor` fixture, as follows:

```python
import pytest

@pytest.fixture(scope="session")
def pdsf_scale_factor() -> int:
    return 4
```

This fixture will be used to scale both the insecure and secure docker registries.

## <a name="limitations"></a>Limitations

1. All the fixtures provided by this package are <tt>session</tt> scoped; and will only be executed once per test execution.
2. At most 10 insecure and 10 secure squid instances are supported using the embedded docker compose.

## External Debugging
While all the metadata needed to interact with the proxy is available for consumption via fixtures, sometimes it is desirable to interact with the instantiated service outside of the test context.

If pytest is executed with <tt>--keepalive</tt>, it is possible to connect to the proxy using external tooling both during and after testing has completed:

```bash
$ https_proxy=https://127.0.0.1:$(docker inspect --format='{{ (index (index .NetworkSettings.Ports "3129/tcp") 0).HostPort }}' pytest-squid-secure-0) \
curl --head --proxy-insecure --proxy-user "pytest.username...:pytest.password..." https://www.google.com/
HTTP/1.1 200 Connection established

HTTP/2 200
content-type: text/html; charset=ISO-8859-1
...
```

You can also retrieve additional, transient, configuration files, such as the CA certificate or proxy configuration, from <tt>/tmp/pytest-of-${USER}/pytest-current/...</tt> or by inspecting the running container.

## Development

[Source Control](https://github.com/crashvb/pytest-docker-squid-fixtures)
