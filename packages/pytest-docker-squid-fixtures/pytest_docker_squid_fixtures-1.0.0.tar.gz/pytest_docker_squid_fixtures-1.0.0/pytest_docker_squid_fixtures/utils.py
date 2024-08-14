#!/usr/bin/env python

"""Utility classes."""

import logging

from importlib.resources import read_text
from pathlib import Path
from random import randrange
from shutil import copyfile
from socket import getfqdn
from ssl import SSLContext
from time import time
from types import MethodType
from typing import Dict, Generator, List, NamedTuple
from urllib3 import ProxyManager, Retry

import bcrypt

from certifi import where
from OpenSSL import crypto
from _pytest.tmpdir import TempPathFactory
from lovely.pytest.docker.compose import execute as docker_compose_execute, Services

LOGGER = logging.getLogger(__name__)

SQUID_PORT_INSECURE = 3128
SQUID_PORT_SECURE = 3129
SQUID_SERVICE = "pytest-squid"
SQUID_SERVICE_PATTERN = f"{SQUID_SERVICE}-{{0}}-{{1}}"


class CertificateKeypair(NamedTuple):
    # pylint: disable=missing-class-docstring
    ca_certificate: bytes
    ca_private_key: bytes
    certificate: bytes
    private_key: bytes


def check_proxy(
    docker_ip: str,
    public_port: int,
    *,
    auth_header: Dict[str, str] = None,
    endpoint="www.google.com",
    protocol: str,
    ssl_context: SSLContext = None,
):
    """
    Secure form of lovey/pytest/docker/compose.py::check_url() that checks when the secure squid service is
    operational.

    Args:
        docker_ip: IP address on which the service is exposed.
        public_port: Port on which the service is exposed.
        auth_header: HTTP basic authentication header to using when connecting to the service.
        endpoint: Public endpoint used to verify the proxy.
        protocol: The protocol to use when verifying readiness.
        ssl_context:
            SSL context referencing the trusted root CA certificated to used when negotiating the TLS connection.

    Returns:
        (bool) True when the service is operational, False otherwise.
    """
    try:
        # Note: This cannot be imported above, as it causes a circular import!
        from . import __version__  # pylint: disable=import-outside-toplevel

        headers = {"User-Agent": f"pytest-docker-squid-fixtures/{__version__}"}
        proxy_headers = headers.copy()
        if auth_header:
            proxy_headers.update(auth_header)

        if ssl_context:
            ssl_context.check_hostname = False

        proxy_manager = ProxyManager(
            headers=headers,
            proxy_headers=proxy_headers,
            proxy_ssl_context=ssl_context,
            proxy_url=f"{protocol}://{docker_ip}:{public_port}/",
        )
        response = proxy_manager.request(
            method="HEAD", retries=Retry(total=0), url=f"{protocol}://{endpoint}/"
        )
        return response.status == 200
    except Exception as exception:  # pylint: disable=broad-except
        LOGGER.debug("Error checking proxy: %s", exception)
        return False


def generate_cacerts(
    tmp_path_factory: TempPathFactory,
    *,
    certificate: Path,
    delete_after: bool = True,
) -> Generator[Path, None, None]:
    """
    Generates a temporary CA certificate trust store containing a given certificate.

    Args:
        tmp_path_factory: Factory to use when generating temporary paths.
        certificate: Path to the certificate to be included in the trust store.
        delete_after: If True, the temporary file will be removed after the iteration is complete.

    Yields:
        The path to the temporary file.
    """
    # Note: where() path cannot be trusted to be temporary, don't pollute persistent files ...
    name = SQUID_SERVICE_PATTERN.format("cacerts", "x")
    tmp_path = tmp_path_factory.mktemp(__name__).joinpath(name)
    copyfile(where(), tmp_path)

    with certificate.open("r") as file_in:
        with tmp_path.open("w") as file_out:
            file_out.write(file_in.read())
    yield tmp_path
    if delete_after:
        tmp_path.unlink(missing_ok=True)


def generate_htpasswd(
    tmp_path_factory: TempPathFactory,
    *,
    delete_after: bool = True,
    password: str,
    username: str,
) -> Generator[Path, None, None]:
    """
    Generates a temporary htpasswd containing a given set of credentials.

    Args:
        tmp_path_factory: Factory to use when generating temporary paths.
        delete_after: If True, the temporary file will be removed after the iteration is complete.
        password: The password corresponding to the provided user name.
        username: The name of the user to include in the htpasswd file.

    Yields:
        The path to the temporary file.
    """
    hashpw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10)).decode()
    tmp_path = tmp_path_factory.mktemp(__name__).joinpath("htpasswd")
    with tmp_path.open("w") as file:
        file.write(f"{username}:{hashpw}")
    yield tmp_path
    if delete_after:
        tmp_path.unlink(missing_ok=True)


def generate_keypair(
    *, keysize: int = 4096, life_cycle: int = 7 * 24 * 60 * 60, service_name: str = None
) -> CertificateKeypair:
    """
    Generates a keypair and certificate for the secure squid service.

    Args:
        keysize: size of the private key.
        life_cycle: Lifespan of the generated certificates, in seconds.
        service_name: Name of the service to be added as a SAN.

    Returns:
        tuple:
            certificate: The public certificate.
            private_key: The private key.
    """

    # Generate a self-signed certificate authority ...
    pkey_ca = crypto.PKey()
    pkey_ca.generate_key(crypto.TYPE_RSA, keysize)

    x509_ca = crypto.X509()
    x509_ca.get_subject().commonName = f"pytest-docker-squid-fixtures-ca-{time()}"
    x509_ca.gmtime_adj_notBefore(0)
    x509_ca.gmtime_adj_notAfter(life_cycle)
    x509_ca.set_issuer(x509_ca.get_subject())
    x509_ca.set_pubkey(pkey_ca)
    x509_ca.set_serial_number(randrange(100000))
    x509_ca.set_version(2)

    x509_ca.add_extensions(
        [crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=x509_ca)]
    )
    x509_ca.add_extensions(
        [
            crypto.X509Extension(b"basicConstraints", True, b"CA:TRUE"),
            crypto.X509Extension(
                b"authorityKeyIdentifier", False, b"keyid:always", issuer=x509_ca
            ),
            crypto.X509Extension(
                b"keyUsage", True, b"digitalSignature, keyCertSign, cRLSign"
            ),
        ]
    )

    x509_ca.sign(pkey_ca, "sha256")

    # Generate a certificate ...
    pkey_cert = crypto.PKey()
    pkey_cert.generate_key(crypto.TYPE_RSA, keysize)

    x509_cert = crypto.X509()
    x509_cert.get_subject().commonName = getfqdn()
    x509_cert.gmtime_adj_notBefore(0)
    x509_cert.gmtime_adj_notAfter(life_cycle)
    x509_cert.set_issuer(x509_ca.get_subject())
    x509_cert.set_pubkey(pkey_cert)
    x509_cert.set_serial_number(randrange(100000))
    x509_cert.set_version(2)

    service_name = [f"DNS:{service_name}"] if service_name else []
    x509_cert.add_extensions(
        [
            crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
            crypto.X509Extension(b"extendedKeyUsage", False, b"serverAuth, clientAuth"),
            crypto.X509Extension(
                b"subjectAltName",
                False,
                ",".join(
                    [
                        f"DNS:{getfqdn()}",
                        f"DNS:*.{getfqdn()}",
                        "DNS:localhost",
                        "DNS:*.localhost",
                        *service_name,
                        "IP:127.0.0.1",
                    ]
                ).encode("utf-8"),
            ),
        ]
    )

    x509_cert.sign(pkey_ca, "sha256")

    return CertificateKeypair(
        ca_certificate=crypto.dump_certificate(crypto.FILETYPE_PEM, x509_ca),
        ca_private_key=crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey_ca),
        certificate=crypto.dump_certificate(crypto.FILETYPE_PEM, x509_cert),
        private_key=crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey_cert),
    )


def get_docker_compose_user_defined(
    docker_compose_files: List[str], service_name: str
) -> Generator[Path, None, None]:
    """
    Tests to see if a user-defined configuration exists, and contains the squid service name.

    Args:
        docker_compose_files: List of docker-compose.yml locations.
        service_name: Name of the squid service.

    Yields:
        The path to a user-defined docker-compose.yml file that contains the service.
    """
    for docker_compose_file in [Path(x) for x in docker_compose_files]:
        try:
            if f"{service_name}:" in docker_compose_file.read_text():
                yield docker_compose_file
        except (FileNotFoundError, IOError):
            ...


def get_embedded_file(
    tmp_path_factory: TempPathFactory, *, delete_after: bool = True, name: str
) -> Generator[Path, None, None]:
    """
    Replicates a file embedded within this package to a temporary file.

    Args:
        tmp_path_factory: Factory to use when generating temporary paths.
        delete_after: If True, the temporary file will be removed after the iteration is complete.
        name: The name of the embedded file to be replicated.

    Yields:
        The path to the temporary file.
    """
    tmp_path = tmp_path_factory.mktemp(__name__).joinpath(name)
    with tmp_path.open("w") as file:
        file.write(read_text(__package__, name))
    yield tmp_path
    if delete_after:
        tmp_path.unlink(missing_ok=True)


def get_user_defined_file(pytestconfig: "_pytest.config.Config", name: str):
    """
    Tests to see if a user-defined file exists.

    Args:
        pytestconfig: pytest configuration file to use when locating the user-defined file.
        name: Name of the user-defined file.

    Yields:
        The path to the user-defined file.
    """
    user_defined = Path(str(pytestconfig.rootdir), "tests", name)
    if user_defined.exists():
        yield user_defined


def duck_punch_execute(self, *subcommand):
    command = ["docker", "compose", "--project-directory", self.project_directory]
    for compose_file in self._compose_files:
        command.append("-f")
        command.append(compose_file)
    command.append("-p")
    command.append(self._project_name)
    command += subcommand
    return docker_compose_execute(command)


def start_service(
    docker_services: Services,
    *,
    docker_compose: Path,
    private_port: int,
    service_name: str,
    **kwargs,
):
    # pylint: disable=protected-access
    """
    Instantiates a given service using docker-compose.

    Args:
        docker_services: lovely service to use to start the service.
        docker_compose: Path to the docker-compose configuration file (to be injected).
        private_port: The private port to which the service is bound.
        service_name: Name of the service, within the docker-compose configuration, to be instantiated.
    """
    # DUCK PUNCH #1: The "docker-compose" package does work with cpython >= v3; swap it out for "docker compose"
    docker_services._docker_compose._original_execute = getattr(
        docker_services._docker_compose, "execute", None
    )
    docker_services._docker_compose.execute = MethodType(
        duck_punch_execute, docker_services._docker_compose
    )

    # DUCK PUNCH #2: Don't get in the way of user-defined lovely/pytest/docker/compose.py::docker_compose_files()
    #             overrides ...

    # Copy the original list appending our service(s). It should be assumed that all files in the list before we got
    # here should already exist. If they don't, docker-compose doesn't handle "-f <dne>" very well ...
    compose_files = [
        *docker_services._docker_compose._compose_files,
        str(docker_compose),
    ]
    compose_files = [file for file in compose_files if Path(file).exists()]

    # Stomp the list so that only our service(s) are started ...
    docker_services._docker_compose._compose_files = [str(docker_compose)]
    docker_services.start(service_name)

    # Assign the augmented list so that docker compose does not complain about orphans when stopping services during
    # teardown.
    docker_services._docker_compose._compose_files = compose_files

    public_port = docker_services.wait_for_service(
        pause=3,
        private_port=private_port,
        service=service_name,
        **kwargs,
    )
    return f"{docker_services.docker_ip}:{public_port}"
