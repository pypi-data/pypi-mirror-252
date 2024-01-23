import dataclasses
from ipaddress import IPv4Network
from logging import getLogger
import os
import yaml

from jinja2 import Environment, PackageLoader, select_autoescape, StrictUndefined

from k3s_local_docker.config import load_from_config, GenerateConfig, version

logger = getLogger(__name__)
env = Environment(
    loader=PackageLoader('k3s_local_docker'),
    autoescape=select_autoescape(),
    undefined=StrictUndefined,
)

template_merge_keys = {
    'config/config.yaml': 'k3s_config',
    'config/registries.yaml': 'k3s_registries_config',
    'docker-compose.yml': None,
}


def merge_yaml(yaml1: str, yaml2: str) -> str:
    data1 = yaml.load(yaml1, Loader=yaml.SafeLoader)
    data2 = yaml.load(yaml2, Loader=yaml.SafeLoader)

    data1.update(data2)
    return yaml.dump(data1, default_flow_style=False)


def get_merge_content(config: GenerateConfig, template_name: str) -> str:
    merge_key = template_merge_keys.get(template_name) or ''
    merge_file = getattr(config, merge_key, None) or ''

    if merge_file:
        with open(merge_file):
            return merge_file.read()
    else:
        return ''


@dataclasses.dataclass()
class TemplateVars(GenerateConfig):
    pod_network_cidr: IPv4Network
    service_network_cidr: IPv4Network
    docker_io_mirror: str
    version: str

    @staticmethod
    def from_config(config: GenerateConfig) -> 'TemplateVars':
        pod_network_cidr, service_network_cidr = config.cluster_network_cidr.subnets()
        docker_io_mirror = config.registry_mirrors.get('docker.io') or 'docker.io'

        config_dict = dataclasses.asdict(config)
        kwargs = {
            f.name: config_dict.get(f.name)
            for f in dataclasses.fields(TemplateVars)
        }
        kwargs.update(
            pod_network_cidr=pod_network_cidr,
            service_network_cidr=service_network_cidr,
            docker_io_mirror=docker_io_mirror,
            version=version,
        )

        return TemplateVars(**kwargs)


def generate_template(template_vars: TemplateVars, template_name: str):
    template = env.get_template(template_name + '.j2')
    output_path = os.path.join(template_vars.data_dir, template_name)

    template_content = template.render(**dataclasses.asdict(template_vars))

    merge_content = get_merge_content(template_vars, template_name)
    if merge_content:
        template_content = merge_yaml(template_content, merge_content)

    with open(output_path, 'w') as fp:
        fp.write(template_content)
        if not template_content.endswith('\n'):
            fp.write('\n')

    logger.info('rendered template to %s', output_path)


def create_dirs(data_dir: str):
    os.makedirs(os.path.join(data_dir, 'config'), exist_ok=True)
    os.makedirs(os.path.join(data_dir, 'secret'), exist_ok=True)
    os.makedirs(os.path.join(data_dir, 'server', 'tls', 'etcd'), exist_ok=True)
    os.makedirs(os.path.join(data_dir, 'data'), exist_ok=True)
    os.makedirs(os.path.join(data_dir, 'data', 'registry-proxy-cache'), exist_ok=True)


def generate(config: GenerateConfig):
    template_vars = TemplateVars.from_config(config)

    create_dirs(config.data_dir)

    template_names = config.template or list(template_merge_keys)

    for template_name in template_names:
        generate_template(template_vars, template_name)


def main():
    config = load_from_config(GenerateConfig)
    generate(config)


if __name__ == '__main__':
    main()
