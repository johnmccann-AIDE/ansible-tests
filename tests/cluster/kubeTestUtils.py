import unittest
import yaml
import os
import warnings
from kubernetes import utils, client, config
from kubernetes.client.rest import ApiException


yaml.warnings({'YAMLLoadWarning': False})
inventory = ['melmore.jnpr.belfast', 'mulroy.jnpr.belfast', 'swilly.jnpr.belfast']
s1 = set(inventory)

# check in correct folder
cwd = os.getcwd()
print("current folder %s"%cwd)
if not cwd.endswith("tests"):
    if "tests" in cwd:
        npath = cwd.split("tests")
        filepath = npath[0] + "tests/"
        print("filepath %s"%filepath)
else:
    filepath = cwd + "/"
    print("filepath %s"%filepath)

class TestUtils(unittest.TestCase):

    def test_create_apps_deployment_from_yaml(self):
        """
        Should be able to create an apps/v1 deployment.
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        utils.create_from_yaml(
            aApiClient, filepath + "cluster/files/" + "app-deployment.yaml")
        app_api = client.AppsV1Api(aApiClient)
        dep = app_api.read_namespaced_deployment(name="kubernetes-dashboard",
                                                 namespace="kube-system")
        self.assertIsNotNone(dep)
        while True:
            try:
                app_api.delete_namespaced_deployment(
                    name="kubernetes-dashboard", namespace="kube-system",
                    body={})
                break
            except ApiException:
                continue

    def test_create_pod_from_yaml(self):
        """
        Should be able to create a pod.
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        utils.create_from_yaml(
            aApiClient, filepath + "cluster/files/" + "core-pod.yaml")
        core_api = client.CoreV1Api(aApiClient)
        pod = core_api.read_namespaced_pod(name="myapp-pod",
                                           namespace="default")
        self.assertIsNotNone(pod)
        core_api.delete_namespaced_pod(
            name="myapp-pod", namespace="default",
            body={})

    def test_create_service_from_yaml(self):
        """
        Should be able to create a service.
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        utils.create_from_yaml(
            aApiClient, filepath + "cluster/files/"+ "core-service.yaml")
        core_api = client.CoreV1Api(aApiClient)
        svc = core_api.read_namespaced_service(name="my-service",
                                               namespace="default")
        self.assertIsNotNone(svc)
        core_api.delete_namespaced_service(
            name="my-service", namespace="default",
            body={})

    def test_create_rbac_role_from_yaml(self):
        """
        Should be able to create an rbac role.
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        utils.create_from_yaml(
            aApiClient, filepath + "cluster/files/" + "rbac-role.yaml")
        rbac_api = client.RbacAuthorizationV1Api(aApiClient)
        rbac_role = rbac_api.read_namespaced_role(name="pod-reader", 
                                                  namespace="default")
        self.assertIsNotNone(rbac_role)
        rbac_api.delete_namespaced_role(
            name="pod-reader", namespace="default", body={})

    def test_create_apiservice_from_yaml_conflict(self):
        """
        Should be able to create an API service.
        Should verify that creating the same API service should
        fail due to conflict.
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        utils.create_from_yaml(
            aApiClient, filepath + "cluster/files/" + "api-service.yaml")
        reg_api = client.ApiregistrationV1beta1Api(aApiClient)
        svc = reg_api.read_api_service(
            name="v1alpha1.wardle.k8s.io")
        self.assertIsNotNone(svc)

        with self.assertRaises(utils.FailToCreateError) as cm:
            utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/api-service.yaml")
        exp_error = ('Error from server (Conflict): '
                     '{"kind":"Status","apiVersion":"v1","metadata":{},'
                     '"status":"Failure",'
                     '"message":"apiservices.apiregistration.k8s.io '
                     '\\"v1alpha1.wardle.k8s.io\\" already exists",'
                     '"reason":"AlreadyExists",'
                     '"details":{"name":"v1alpha1.wardle.k8s.io",'
                     '"group":"apiregistration.k8s.io","kind":"apiservices"},'
                     '"code":409}\n'
                     )
        self.assertEqual(exp_error, str(cm.exception))
        reg_api.delete_api_service(
            name="v1alpha1.wardle.k8s.io", body={})

    def test_create_from_multi_resource_yaml(self):
        """
        Should be able to create a service and a replication controller
        from a multi-resource yaml file
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        utils.create_from_yaml(
            aApiClient, filepath + "cluster/files/" + "multi-resource.yaml")
        core_api = client.CoreV1Api(aApiClient)
        svc = core_api.read_namespaced_service(name="mock",
                                               namespace="default")
        self.assertIsNotNone(svc)
        ctr = core_api.read_namespaced_replication_controller(
            name="mock", namespace="default")
        self.assertIsNotNone(ctr)
        core_api.delete_namespaced_replication_controller(
            name="mock", namespace="default", body={})
        core_api.delete_namespaced_service(name="mock",
                                           namespace="default", body={})

    def test_create_from_list_in_multi_resource_yaml(self):
        """
        Should be able to create the items in the PodList and a deployment
        specified in the multi-resource file
        """
        result = []
        # Create a configuration object
        aConfiguration = config.load_kube_config()

        # Create a ApiClient with our config
        aApiClient = client.ApiClient(aConfiguration)
        core_v1 = client.CoreV1Api(aApiClient)

        utils.create_from_yaml(
            aApiClient, filepath + "cluster/files/" + "multi-resource-with-list.yaml")
        core_api = client.CoreV1Api(aApiClient)
        app_api = client.AppsV1Api(aApiClient)
        pod_0 = core_api.read_namespaced_pod(
            name="mock-pod-0", namespace="default")
        self.assertIsNotNone(pod_0)
        pod_1 = core_api.read_namespaced_pod(
            name="mock-pod-1", namespace="default")
        self.assertIsNotNone(pod_1)
        dep = app_api.read_namespaced_deployment(
            name="mock", namespace="default")
        self.assertIsNotNone(dep)
        core_api.delete_namespaced_pod(
            name="mock-pod-0", namespace="default", body={})
        core_api.delete_namespaced_pod(
            name="mock-pod-1", namespace="default", body={})
        app_api.delete_namespaced_deployment(
            name="mock", namespace="default", body={})

if __name__ == '__main__':
    unittest.main(warnings='ignore')