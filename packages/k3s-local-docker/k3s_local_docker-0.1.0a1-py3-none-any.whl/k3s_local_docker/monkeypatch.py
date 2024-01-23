#!/usr/bin/env python3

'''
The Kubernetes Python API doesn't handle proxies very well.

Import this module as soon as possible in the entrypoints to fix it
'''

import kubernetes.config.kube_config


class KubeConfigLoader(kubernetes.config.kube_config.KubeConfigLoader):
    def _set_config(self, client_configuration):
        super()._set_config(client_configuration)
        # copy these keys directly from self to configuration object
        keys = ['host', 'ssl_ca_cert', 'cert_file', 'key_file', 'verify_ssl', 'proxy']
        for key in keys:
            if key in self.__dict__:
                setattr(client_configuration, key, getattr(self, key))

    def _load_cluster_info(self):
        super()._load_cluster_info()
        if 'proxy-url' in self._cluster:
            self.proxy = self._cluster['proxy-url']


kubernetes.config.kube_config.KubeConfigLoader = KubeConfigLoader
