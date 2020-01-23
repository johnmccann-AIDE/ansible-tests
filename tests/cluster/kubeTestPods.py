import unittest
import yaml
from kubernetes import utils, client, config
from kubernetes.client.rest import ApiException
import warnings

yaml.warnings({'YAMLLoadWarning': False})
inventory = ['melmore.jnpr.belfast', 'mulroy.jnpr.belfast', 'swilly.jnpr.belfast']
s1 = set(inventory)

class TestPods(unittest.TestCase):

    def test_pod_running_default(self):
        """
        verify that all nodes are online
        """
        result = ""
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_pod("default")
        if not response.items :
            self.assertIsNotNone(response, msg="No pods are running for default namespace")
        else:
            for i in response.items:
                if "Running" not in i.status.phase:
                    result = "Not Running"
        self.assertIsNotNone(result)

    def test_pod_volume_running_on_all_nodes(self):
        """
        verify that all nodes are online
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_pod("default")
        for i in response.items:
            if i.metadata.name.startswith("local-volume"):
                result.append(i.spec.node_name)
        s2 = set(result)
        self.assertEqual(s1, s2, msg="Not all nodes are running local-volume-provisioner")

    def test_pod_kibana_running(self):
        """
        verify that all nodes are online
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_pod("default")
        for i in response.items:
            if i.metadata.name.startswith("kibana"):
                result.append(i.spec.node_name)
        #s2 = set(result)
        self.assertIsNotNone(result, msg="No pod instance running kibana")

    def test_pod_running_system(self):
        """
        verify that all nodes are online
        """
        result = ""
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_pod("kube-system")
        if not response.items :
            self.assertIsNotNone(response, msg="No pods are running for kube-system namespace")
        else:
            for i in response.items:
                if "Running" not in i.status.phase:
                    result = "Not Running"
        self.assertIsNotNone(result)

    def test_pod_etcd_running_on_all_nodes(self):
        """
        verify that all nodes are online
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_pod("kube-system")
        for i in response.items:
            if i.metadata.name.startswith("etcd"):
                result.append(i.spec.node_name)
        s2 = set(result)
        self.assertEqual(s1, s2, msg="Not all nodes are running etcd")

    def test_pod_nginx_running_on_all_nodes(self):
        """
        verify that all nodes are online
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_pod("kube-system")
        for i in response.items:
            if i.metadata.name.startswith("nginx-ingress-controller"):
                result.append(i.spec.node_name)
        s2 = set(result)
        self.assertEqual(s1, s2, msg="Not all nodes are running nginx %s"%result)

    def test_pod_fluentd_running_on_all_nodes(self):
        """
        verify that all nodes are online
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_pod("kube-system")
        for i in response.items:
            if i.metadata.name.startswith("fluentd-es"):
                result.append(i.spec.node_name)
        s2 = set(result)
        self.assertEqual(s1, s2, msg="Not all nodes are running fluentd %s"%result)

    def test_pod_calico_running_on_all_nodes(self):
        """
        verify that all nodes are online
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_namespaced_pod("kube-system")
        for i in response.items:
            if i.metadata.name.startswith("calico"):
                result.append(i.spec.node_name)
        s2 = set(result)
        self.assertEqual(s1, s2, msg="Not all nodes are running calico")

if __name__ == '__main__':
    unittest.main(warnings='ignore')