
'''
Waits for the kubectl deployments to be ready
'''

import k3s_local_docker.monkeypatch as _

from dataclasses import dataclass
from logging import getLogger
from multiprocessing.pool import ThreadPool
import time
from typing import Annotated, Any, Callable

from kubernetes import client as kubeclient, config as kubeconfig

from k3s_local_docker.config import load_from_config
from k3s_local_docker.commands.copy_kubeconfig import KubeConfig

logger = getLogger(__name__)


@dataclass()
class WaitForResourcesConfig(KubeConfig):
    resource: Annotated[list[str], 'resource', dict(
        nargs='*',
        help='resource spec TYPE:NAMESPACE:NAME or TYPE:NAME'
    )]


def check_deployment_status(namespace: str, name: str, num_pods: int = 1) -> bool:
    logger.info('checking status of deployment %s/%s', namespace, name)

    try:
        api_instance = kubeclient.AppsV1Api()
        deployment = api_instance.read_namespaced_deployment_status(name=name, namespace=namespace)
        status: dict[str, Any] = deployment.status.to_dict()
    except Exception:
        logger.exception('failed to get the status of deployment %s/%s', namespace, name)
        return False

    status.pop('conditions', None)
    logger.info('got status for deployment %s/%s: %s', namespace, name, status)

    if status.get('ready_replicas') == status.get('replicas') == num_pods:
        logger.info('deployment %s/%s is ready', namespace, name)
        return True
    else:
        logger.info("deployment %s/%s still isn't ready", namespace, name)
        return False


def check_crd_status(name: str) -> bool:
    logger.info('checking existence of crd %s', name)

    try:
        api_instance = kubeclient.ApiextensionsV1Api()
        defs = kubeclient.V1CustomResourceDefinitionList = api_instance.list_custom_resource_definition(
            field_selector=f'metadata.name={name}'
        )
        if defs.items:
            logger.info('CRD %s exists', name)
            return True
        else:
            logger.warning("CRD %s doesn't exist", name)
            return False
    except Exception:
        logger.exception('failed to get the status of the CRD %s', name)
        return False


def check_node_status(name: str) -> bool:
    logger.info('checking status of node %s', name)

    try:
        api_instance = kubeclient.CoreV1Api()
        node: kubeclient.V1Node = api_instance.read_node_status(name)
        conditions: list[kubeclient.V1NodeCondition] = node.status.conditions
        for condition in conditions:
            if condition.type == "Ready" and condition.status == "True":
                logger.info('node %s is ready', name)
                return True

        logger.warning("node %s isn't ready", name)
        return False
    except Exception:
        logger.exception('failed to get the status of node %s', name)
        return False


def get_condition(resource: str) -> Callable[[], bool]:
    typename, _, spec = resource.partition(':')
    if typename == 'deployment':
        namespace, _, name = spec.partition('/')
        name, _, num_pods = name.partition('?')
        return lambda: check_deployment_status(namespace, name, int(num_pods or '1'))
    elif typename == 'crd':
        return lambda: check_crd_status(spec)
    elif typename == 'node':
        return lambda: check_node_status(spec)
    else:
        raise ValueError(f"Unrecognized resource type '{typename}'")


def wait_for_condition(condition: Callable[[], bool], retry_pause: float):
    while not condition():
        time.sleep(retry_pause)


def wait_for_resources(resources: list[str], retry_pause: float):
    kubeconfig.load_kube_config()
    conditions = [get_condition(resource) for resource in resources]
    with ThreadPool() as pool:
        pool.map(lambda condition: wait_for_condition(condition, retry_pause), conditions)


def main():
    config = load_from_config(WaitForResourcesConfig)

    wait_for_resources(config.resource, config.retry_pause)


if __name__ == '__main__':
    main()
