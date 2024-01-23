import dataclasses
import importlib.metadata
from ipaddress import IPv4Address, IPv4Network
import logging
from typing import Annotated, List, Mapping, NamedTuple, Type, TypeVar

import configargparse

from k3s_local_docker.utils import (
    dict_from_mappings,
    get_machine_hostname,
    get_machine_primary_ip,
    get_user_ids,
)


class PortRange(NamedTuple):
    start: int
    end: int

    def __str__(self):
        return f'{self.start}-{self.end}'

    @staticmethod
    def from_config(config: str) -> 'PortRange':
        start_string, _, end_string = config.partition('-')
        try:
            start = int(start_string)
            end = int(end_string)
            return PortRange(start, end)
        except Exception as e:
            raise ValueError('invalid port range') from e

    def check(self, port: int):
        if not (self.start <= port <= self.end):
            raise ValueError(f'invalid port {port}: should be in range [{self.start}, {self.end}]')


class PortMapping(NamedTuple):
    host: int
    cluster: int

    def __str__(self):
        return f'{self.host}:{self.cluster}'

    @staticmethod
    def from_config(config: str) -> 'PortMapping':
        host_string, _, cluster_string = config.partition(':')
        cluster_string = cluster_string or '0'
        try:
            host = int(host_string)
            cluster = int(cluster_string)
        except Exception as e:
            raise ValueError('invalid port mapping') from e
        return PortMapping(host, cluster)

    def check(self, other: 'PortMapping'):
        if self.host == other.host or self.cluster == other.cluster:
            raise ValueError(f'invalid port mapping {other} conflicts with {self}')


T = TypeVar('T', bound=dataclasses.dataclass)


def load_from_config(cls: Type[T]) -> T:
    parser = configargparse.ArgParser(
        default_config_files=['pyproject.toml', '.k3s-local-docker.toml'],
        config_file_parser_class=configargparse.TomlConfigParser(['tool.k3s-local-docker']),
        formatter_class=configargparse.ArgumentDefaultsRawHelpFormatter,
        ignore_unknown_config_file_keys=True,
    )
    callable_defaults = {}

    for field in dataclasses.fields(cls):
        name = field.name
        try:
            arg_name, opts = field.type.__metadata__
            opts = {**opts}
        except Exception:
            continue

        if callable(opts.get('default')):
            callable_defaults[name] = opts.pop('default')
            opts['default'] = None
        parser.add(arg_name, **opts)

    kwargs = vars(parser.parse_args())
    for name, callable_default in callable_defaults.items():
        if not kwargs.get(name):
            kwargs[name] = callable_default()

    config = cls(**kwargs)
    config.configure()
    return config


@dataclasses.dataclass()
class BaseConfig:
    def configure(self):
        pass


@dataclasses.dataclass()
class GlobalConfig(BaseConfig):
    config_file: Annotated[str, '--config-file', dict(
        env_var='K3S_LOCAL_DOCKER_CONFIG',
        is_config_file=True,
        help="config file path",
    )]

    data_dir: Annotated[str, '--data-dir', dict(
        env_var='K3S_LOCAL_DOCKER_DATA_DIR',
        default='.cluster.local',
        help="local path to store the persistent cluster configs and data",
    )]

    log_level: Annotated[str, '--log-level', dict(
        default='INFO',
        choices=['INFO', 'WARNING', 'ERROR', 'DEBUG'],
        help='app log level',
    )]

    def configure(self):
        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            level=getattr(logging, self.log_level),
            datefmt='%Y-%m-%d %H:%M:%S',
        )


@dataclasses.dataclass()
class ClusterConfig(GlobalConfig):
    master_hostname: Annotated[str, '--master-hostname', dict(
        default=get_machine_hostname,
        help="master hostname, should be externally accessible. Defaults to this machine\'s hostname",
    )]

    master_ip: Annotated[IPv4Address, '--master-ip', dict(
        default=get_machine_primary_ip,
        help="master IP, should be externally accessible. Defaults to this machine's main IP",
    )]

    service_port_range: Annotated[PortRange, '--service-port-range', dict(
        default=PortRange(30000, 30020),
        type=PortRange.from_config,
        help="range of TCP ports to bind externally for NodePort and LoadBalancer services",
    )]

    http_port: Annotated[PortMapping, '--http-port', dict(
        default=PortMapping(80, 0),
        type=PortMapping.from_config,
        help=(
            "port to bind to the HTTP ingress port, in the format HOST_PORT:SERVICE_PORT. "
            "The service port must be within the range given in --service-port-range."
            "The host port defaults to 80 and the service port to the first one in the aforementioned service port range"
        ),
    )]

    https_port: Annotated[PortMapping, '--https-port', dict(
        default=PortMapping(443, 0),
        type=PortMapping.from_config,
        help=(
            "port to bind to the HTTPS ingress port, in the format HOST_PORT:SERVICE_PORT. "
            "The service port must be within the range given in --service-port-range."
            "The host port defaults to 443 and the service port to the second one in the aforementioned service port range"
        ),
    )]

    docker_network_cidr: Annotated[IPv4Network, '--docker-network-cidr', dict(
        default=IPv4Network('10.1.0.0/16'),
        type=IPv4Network,
        help=(
            "IP CIDR block to assign to the container subnet. "
            "It must not insersect with the CIDR in --cluster-network-cidr"
        ),
    )]

    docker_network_name: Annotated[str, '--docker-network-name', dict(
        default='docker.internal',
        help="Name of the container subnet."
    )]

    cluster_network_cidr: Annotated[IPv4Network, '--cluster-network-cidr', dict(
        default=IPv4Network('10.2.0.0/16'),
        type=IPv4Network,
        help=(
            "IP CIDR block to assign to the cluster. "
            "This block will be split: half to pods and half to services. "
            "It must not insersect with the CIDR in --docker-network-cidr"
        ),
    )]

    network_backend: Annotated[str, '--network-backend', dict(
        default='vxlan',
        choices=['vxlan', 'wireguard-native'],
        help=(
            "Backend for the flannel networking stack. "
            "You must have the wireguard modules installed in your Docker machine if you want to use wireguard "
            "(needed for multi-node clusters)"
        ),
    )]

    k3s_registries_config: Annotated[str, '--k3s-registries-config', dict(
        help="Path to a registries.yaml config to be merged with the generated one",
    )]

    k3s_config: Annotated[str, '--k3s-config', dict(
        help="Path to a k3s.yaml config to be merged with the generated one",
    )]
    k3s_role: Annotated[str, '--k3s-role', dict(
        default='server',
        choices=['server', 'agent'],
        help="Path to a k3s.yaml config to be merged with the generated one",
    )]

    registry_mirrors: Annotated[Mapping[str, str], '--registry-mirrors', dict(
        default={},
        nargs='*',
        type=dict_from_mappings,
        help='Mappings REGISTRY_HOSTNAME:MIRROR_HOSTNAME',
    )]

    containerd_proxy: Annotated[str, '--containerd-proxy', dict(
        nargs='?',
        const='http://proxy.docker.internal:3128',
        default=None,
        help='Proxy to pass to containerd',
    )]

    local_proxy_enable: Annotated[bool, '--local-proxy-enable', dict(
        action='store_true',
        default=False,
        dest='local_proxy_enable',
        help='Enable the local registry caching proxy',
    )]
    local_proxy_registries: Annotated[List[str], '--local-proxy-registries', dict(
        nargs='*',
        default=[],
        help='Proxy registry hostnames',
    )]

    shm_size: Annotated[str, '--shm-size', dict(
        default='2g',
        help='shared memory space',
    )]

    user_uid: Annotated[int, '--user-uid', dict(
        default=lambda: get_user_ids()[0],
        type=int,
        help='User UID to set in the generated external files',
    )]
    user_gid: Annotated[int, '--user-gid', dict(
        default=lambda: get_user_ids()[1],
        type=int,
        help='User GID to set in the generated external files',
    )]

    def configure(self):
        super().configure()

        if self.docker_network_cidr.overlaps(self.cluster_network_cidr):
            raise ValueError(
                f'invalid subnets: docker={self.docker_network_cidr} '
                f'overlaps with cluster={self.cluster_network_cidr}'
            )

        if not self.http_port.cluster:
            self.http_port = self.http_port._replace(cluster=self.service_port_range.start)

        if not self.https_port.cluster:
            self.https_port = self.https_port._replace(cluster=self.service_port_range.start + 1)

        self.service_port_range.check(self.http_port.cluster)
        self.service_port_range.check(self.https_port.cluster)
        self.http_port.check(self.https_port)


@dataclasses.dataclass()
class GenerateConfig(ClusterConfig):
    template: Annotated[List[str], 'template', dict(
        nargs='*',
        help='file template name',
    )]


version = importlib.metadata.version('k3s_local_docker')


if __name__ == '__main__':
    config = load_from_config(GenerateConfig)
    print(config)
