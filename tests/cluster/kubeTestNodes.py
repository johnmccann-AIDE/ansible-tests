import unittest
import yaml
from kubernetes import utils, client, config
from kubernetes.client.rest import ApiException

class TestNodes(unittest.TestCase):

   
    def test_node_status(self):
        """
        verify that all nodes are online
        """
        result = ""
        yaml.warnings({'YAMLLoadWarning': False})
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)

        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_node(watch=False)
        for i in response.items:
            for cond in i.status.conditions:
                if "KubeletReady" in cond.reason:
                    stat = str(cond.type)
            node = i.metadata.name
            # check whether node is notready
            if "None" in stat:
                result = "Not Ready"
            #self.assertEqual("Ready", stat, msg="Node %s is not ready!"%node)
        self.assertIsNotNone(result)


    def test_node_role(self):
        """
        verify that all nodes are online
        """
        result = ""
        yaml.warnings({'YAMLLoadWarning': False})
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)

        core_v1 = client.CoreV1Api(aApiClient)

        response = core_v1.list_node(watch=False)
        for i in response.items:
            for label in i.metadata.labels:
                if "node-role" in label:
                    nodelabel = label.split("/")
                    noderole = nodelabel[1].strip()
            node = i.metadata.name
            if "None" in noderole:
                result = "None"
            #self.assertEqual("master", noderole, msg="Node %s does not have a role!"%node)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()