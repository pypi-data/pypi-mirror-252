#!/usr/bin/env python3

from dataclasses import dataclass
from logging import getLogger
import shlex
import subprocess
from typing import Annotated, Literal

from k3s_local_docker.config import load_from_config
from k3s_local_docker.generate import (
    generate, GenerateConfig
)
from k3s_local_docker.utils import get_compose_cmd
from k3s_local_docker.commands.copy_kubeconfig import (
    copy_kubeconfig, CopyConfig,
)
from k3s_local_docker.commands.wait_for_resources import (
    wait_for_resources
)

logger = getLogger(__name__)

Cmd = Literal['start', 'stop', 'rm']


@dataclass()
class ComposeConfig(CopyConfig, GenerateConfig):
    compose_cmd: Annotated[str, '--compose-cmd', dict(
        default=get_compose_cmd,
        env_var='DOCKER_COMPOSE',
        help='Command to run docker-compose. Defaults to autodetection',
    )]
    cmd: Annotated[Cmd, 'cmd', dict(
        choices=Cmd.__args__,
        help='compose command',
    )]

    def configure(self):
        super(CopyConfig, self).configure()
        super(GenerateConfig, self).configure()


def compose_start(config: ComposeConfig):
    generate(config)

    cmd = shlex.split(config.compose_cmd) + ['up', '-d']
    subprocess.run(cmd, check=True, cwd=config.data_dir)

    copy_kubeconfig(config)
    wait_for_resources(
        retry_pause=config.retry_pause,
        resources=[
            'deployment:kube-system/coredns',
            'deployment:kube-system/local-path-provisioner',
            'deployment:kube-system/metrics-server',
        ],
    )
    logger.info('Cluster is alive!')


def compose_stop(config: ComposeConfig):
    cmd = shlex.split(config.compose_cmd) + ['rm', '--force', '--stop']
    subprocess.run(cmd, check=True, cwd=config.data_dir)
    logger.info('Cluster is stopped!')


def compose_rm(config: ComposeConfig):
    compose_stop(config)

    cmd = shlex.split(config.compose_cmd) + ['down', '--remove-orphans', '--volumes']
    subprocess.run(cmd, check=True, cwd=config.data_dir)
    logger.info('Cluster is removed!')


def compose_run(cmd: Cmd, config: ComposeConfig):
    if cmd == 'start':
        compose_start(config)
    elif cmd == 'stop':
        compose_stop(config)
    elif cmd == 'rm':
        compose_rm(config)


def main():
    config = load_from_config(ComposeConfig)
    compose_run(config.cmd, config)


if __name__ == '__main__':
    main()
