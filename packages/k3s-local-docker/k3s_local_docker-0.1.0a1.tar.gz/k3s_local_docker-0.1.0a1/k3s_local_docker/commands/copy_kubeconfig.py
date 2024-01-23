#!/usr/bin/env python3

from dataclasses import dataclass
from logging import getLogger
import os
from pathlib import Path
import shlex
import subprocess
import time
from typing import Annotated, Optional
from urllib.parse import urlparse, urlunparse

import yaml

from k3s_local_docker.config import load_from_config, ClusterConfig
from k3s_local_docker.utils import get_compose_cmd

logger = getLogger(__name__)


@dataclass()
class KubeConfig(ClusterConfig):
    retry_pause: Annotated[float, '--retry-pause', dict(
        default=5.0,
        env_var='RETRY_PAUSE',
        help='pause before retrying',
    )]
    kubeconfig: Annotated[str, '--kubeconfig', dict(
        env_var='KUBECONFIG',
        help=(
            'Output path for the kubeconfig file. '
            'Defaults to secret/kubeconfig.yaml in the data dir. '
            "If set to '-' (a dash), the contents will be printed to the stdout."
        ),
    )]

    def configure(self):
        super().configure()
        self.kubeconfig = self.kubeconfig or os.path.join(self.data_dir, 'secret', 'kubeconfig.yaml')
        os.environ['KUBECONFIG'] = self.kubeconfig


@dataclass()
class CopyConfig(KubeConfig):
    compose_cmd: Annotated[str, '--compose-cmd', dict(
        env_var='DOCKER_COMPOSE',
        help='Command to run docker-compose. Defaults to autodetection',
    )]
    proxy: Annotated[Optional[str], '--proxy', dict(
        help='Add a proxy to the kubeconfig file',
    )]


def get_kubeconfig(basedir: str, retry_pause: float = 5.0, compose_cmd: Optional[str] = None) -> str:
    '''
    Uses docker-compose to copy the contents of the kubeconfig file, retrying until it succeeds
    '''
    # old versions of docker-compose don't have the cp subcommand
    compose_cmd_args = shlex.split(compose_cmd or get_compose_cmd()) + [
        'exec',
        '-T',
        'k3s',
        '/bin/sh',
        '-c',
        'cat $KUBECONFIG',
    ]

    while True:
        logger.info('trying to copy the kubeconfig locally')
        try:
            process = subprocess.run(
                compose_cmd_args,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                cwd=basedir,
            )
        except subprocess.SubprocessError:
            logger.warning('failed to copy the kubeconfig file, trying again in %.2f seconds', retry_pause)
            time.sleep(retry_pause)
            continue
        else:
            content: str = process.stdout
            # make sure we've copied a valid YAML
            yaml.load(content, Loader=yaml.SafeLoader)
            return content


def adjust_kubeconfig(content: str, hostname: str, proxy: Optional[str]) -> str:
    '''
    Adjusts the kubeconfig server and optionally the hostname
    '''
    data = yaml.load(content, Loader=yaml.SafeLoader)

    for cluster_item in data['clusters']:
        cluster = cluster_item['cluster']

        server_url = urlparse(cluster['server'])
        server_url = server_url._replace(netloc=f'{hostname}:{server_url.port}')
        cluster['server'] = urlunparse(server_url)

        if proxy:
            cluster['proxy-url'] = proxy

    return yaml.dump(data, default_flow_style=False)


def write_kubeconfig(content: str, dest: str):
    '''
    Writes the content to a file, adjusting its permissions appropriately.
    If dest is '-', the contents are just printed to stdout
    '''
    if dest == '-':
        logger.info('writing the kubeconfig to stdout')
        print(content)
    else:
        logger.info('copying the kubeconfig to %s', dest)
        path = Path(dest)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(0o600)
        path.chmod(0o600)

        with path.open('w') as fp:
            fp.write(content)
            if not content.endswith('\n'):
                fp.write('\n')


def copy_kubeconfig(config: CopyConfig):
    content = get_kubeconfig(config.data_dir, config.retry_pause, config.compose_cmd)
    content = adjust_kubeconfig(content, config.master_hostname, config.proxy)

    write_kubeconfig(content, config.kubeconfig)


def main():
    config = load_from_config(CopyConfig)
    copy_kubeconfig(config)


if __name__ == '__main__':
    main()
