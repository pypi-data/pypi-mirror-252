from contextlib import closing
import os
import shlex
import socket
import subprocess
from typing import List, Mapping, Tuple


def get_machine_hostname() -> str:
    return socket.getfqdn()


def get_machine_primary_ip() -> str:
    # from https://stackoverflow.com/a/28950776
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        with closing(s):
            s.settimeout(0)
            s.connect(('10.254.254.254', 1))
            return s.getsockname()[0]
    except Exception as e:
        raise OSError('failed to get the primary IP') from e


def dict_from_mappings(mappings: List[str]) -> Mapping[str, str]:
    result = {}

    for mapping in mappings:
        k, _, v = mapping.partition(':')
        if not (k and v):
            raise ValueError('invalid mapping, should have key and value')
        result[k] = v

    return result


def get_user_ids() -> Tuple[int, int]:
    return [os.getuid(), os.getgid()]


def get_compose_cmd() -> str:
    for cmd in ('docker compose', 'docker-compose'):
        try:
            subprocess.run(
                shlex.split(f'{cmd} version'),
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.SubprocessError:
            pass
        else:
            return cmd

    raise ValueError("Couldn't detect the docker-compose command")
