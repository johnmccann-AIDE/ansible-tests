import unittest
import yaml
from kubernetes import utils, client, config
from kubernetes.client.rest import ApiException
import warnings

yaml.warnings({'YAMLLoadWarning': False})
inventory = ['melmore.jnpr.belfast', 'mulroy.jnpr.belfast', 'swilly.jnpr.belfast']
s1 = set(inventory)

class TestServices(unittest.TestCase):

    def test_kibana_svc(self):
        """
        verify that all nodes are online
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_service("default")
        for i in response.items:
            if "kibana" in i.metadata.name:
                portRef = ""
                for p in i.spec.ports:
                    portRef = portRef + str(p.port) + "/" + p.protocol + ","
        self.assertIsNone(portRef)

    def test_kubernetes_svc(self):
        """
        verify that all nodes are online
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_service("default")
        for i in response.items:
            if "kubernetes" in i.metadata.name:
                portRef = ""
                for p in i.spec.ports:
                    portRef = portRef + str(p.port) + "/" + p.protocol + ","
        self.assertIsNone(portRef)

    def test_calico_svc(self):
        """
        verify that all nodes are online
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_service("kube-system")
        for i in response.items:
            if "calico" in i.metadata.name:
                portRef = ""
                for p in i.spec.ports:
                    portRef = portRef + str(p.port) + "/" + p.protocol + ","
        self.assertIsNone(portRef)

    def test_kube_dns_svc(self):
        """
        verify that all nodes are online
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_service("kube-system")
        for i in response.items:
            if "kube-dns" in i.metadata.name:
                portRef = ""
                for p in i.spec.ports:
                    portRef = portRef + str(p.port) + "/" + p.protocol + ","
        self.assertIsNone(portRef)

    def test_nginx-controller_svc(self):
        """
        verify that all nodes are online
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_service("kube-system")
        for i in response.items:
            if "nginx-ingress-controller" in i.metadata.name:
                portRef = ""
                for p in i.spec.ports:
                    portRef = portRef + str(p.port) + "/" + p.protocol + ","
        self.assertIsNone(portRef)

    def test_nginx-default_backend_svc(self):
        """
        verify that all nodes are online
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_service("kube-system")
        for i in response.items:
            if "nginx-ingress-default-backend" in i.metadata.name:
                portRef = ""
                for p in i.spec.ports:
                    portRef = portRef + str(p.port) + "/" + p.protocol + ","
        self.assertIsNone(portRef)

if __name__ == '__main__':
    unittest.main(warnings='ignore')