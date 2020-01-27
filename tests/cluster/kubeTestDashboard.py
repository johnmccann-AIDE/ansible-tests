import unittest
import os
import urllib3
import yaml
import warnings
from kubernetes import utils, client, config
from kubernetes.client.rest import ApiException

# check in correct folder   
cwd = os.getcwd()
print("current folder %s"%cwd)
if not cwd.endswith("/tests"):
    if "/tests" in cwd:
        npath = cwd.split("/tests")
        filepath = npath[0] + "/tests/"
        print("filepath %s"%filepath)
    else:
        filepath = cwd + "/tests/"
else:
    filepath = cwd + "/"
    print("filepath %s"%filepath)

stream = os.popen("kubectl config view --minify | grep server | cut -f 2- -d ':' | tr -d ' '")
apiserver = stream.read()
#print("using server %s"%apiserver)
#secretName = os.system("kubectl get secrets | grep ^default | cut -f1 -d ' '")
stream = os.popen("kubectl get secrets | grep ^default | cut -f1 -d ' '")
secretName = stream.read()
#print("using secret %s"%secretName)
#aToken=os.system("kubectl describe secret " + str(secretName) + " | grep -E '^token' | cut -f2 -d':' | tr -d ' '")
command="kubectl describe secret " + str(secretName) #+ " | grep -E '^token' | cut -f2 -d':' | tr -d ' '"
# print("command to extract token %s"%command)
stream = os.popen(command)
kToken = stream.read()
nToken = kToken.split("token:")
aToken = nToken[1].strip()
#print("Using token '%s'"%aToken)

# disable warnings
yaml.warnings({'YAMLLoadWarning': False})

# Create a configuration object
aConfiguration = config.load_kube_config()
# Create a ApiClient with our config
aApiClient = client.ApiClient(aConfiguration)


class TestDashboard(unittest.TestCase):

    def test_a_create_user_cluster_role(self):
        # create service account and cluster role bindings
        try:
            utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/" + "dashboard-adminuser.yaml")
            core_api = client.CoreV1Api(aApiClient)
            user_resp = core_api.read_namespaced_service_account(name="admin-user", namespace="kube-system")
            #print("user response %s " %user_resp)

            self.assertIsNotNone(user_resp)

            rbac_body = utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/" + "dashboard-adminrolebind.yaml")
            rbac_api = client.RbacAuthorizationV1Api(aApiClient)
            cluster_resp = rbac_api.read_cluster_role_binding(name="admin-user")
            #print("cluster response %s " %cluster_resp)
            self.assertIsNotNone(user_resp)
        except ApiException as e:
            print("Exception creating user role: %s\n"%e)

        # tidy up created settings
        """ try:
            core_api = client.CoreV1Api(aApiClient)
            resp = core_api.delete_namespaced_service_account(name="admin-user", namespace='kube-system')
            rbac_api = client.RbacAuthorizationV1Api(aApiClient)
            resp = rbac_api.delete_cluster_role_binding(name="admin-user")
        except ApiException as e:
            print("Exception deleting user role: %s\n"%e) """

    def test_b_create_user_duplicate(self):
        # create a dupluicate user
        #self.maxDiff = None
        try:    
            with self.assertRaises(utils.FailToCreateError) as cm:
                utils.create_from_yaml(
                    aApiClient, filepath + "cluster/files/" + "dashboard-adminuser.yaml")
            exp_error = ('Error from server (Conflict): '
                        '{"kind":"Status","apiVersion":"v1","metadata":{},'
                        '"status":"Failure",'
                        '"message":"serviceaccounts \\"admin-user\\" already exists",'
                        '"reason":"AlreadyExists",'
                        '"details":{"name":"admin-user","kind":"serviceaccounts"},'
                        '"code":409}\n'
                        )
            self.assertEqual(exp_error, str(cm.exception))
        except ApiException as e:
            print("Exception creating duplicate user role: %s\n"%e)

    def test_c_create_secret_certs(self):
        # create certificates
        try:
            utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/" + "dashboard-certs.yaml")
            core_api = client.CoreV1Api(aApiClient)
            certs_resp = core_api.read_namespaced_secret(name="kubernetes-dashboard-certs", namespace="kube-system")
            #print("certs response %s " %certs_resp)
            self.assertIsNotNone(certs_resp)

            utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/" + "dashboard-csrf.yaml")
            core_api = client.CoreV1Api(aApiClient)
            csrf_resp = core_api.read_namespaced_secret(name="kubernetes-dashboard-csrf", namespace="kube-system")
            #print("certs response %s " %csrf_resp)
            self.assertIsNotNone(csrf_resp)

            utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/" + "dashboard-keyh.yaml")
            core_api = client.CoreV1Api(aApiClient)
            keyh_resp = core_api.read_namespaced_secret(name="kubernetes-dashboard-key-holder", namespace="kube-system")
            #print("certs response %s " %keyh_resp)
            self.assertIsNotNone(keyh_resp)

        except ApiException as e:
            print("Exception creating certs: %s\n"%e)

        # tidy up created settings
        """ try:
            certs_resp = core_api.delete_namespaced_secret(name="kubernetes-dashboard-certs", namespace="kube-system")
            print("certs response %s " %certs_resp)
            csrf_resp = core_api.delete_namespaced_secret(name="kubernetes-dashboard-csrf", namespace="kube-system")
            print("certs response %s " %csrf_resp)
            keyh_resp = core_api.delete_namespaced_secret(name="kubernetes-dashboard-key-holder", namespace="kube-system")
            print("certs response %s " %keyh_resp)
        except ApiException as e:
            print("Exception deleting certs: %s\n"%e) """

    def test_d_create_config_map(self):
        # create config map
        try:
            utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/" + "dashboard-configmap.yaml")
            core_api = client.CoreV1Api(aApiClient)
            conf_resp = core_api.read_namespaced_config_map(name="kubernetes-dashboard-settings", namespace="kube-system")
            #print("config map response %s " %conf_resp)

            self.assertIsNotNone(conf_resp)

        except ApiException as e:
            print("Exception creating config map: %s\n"%e)

        # tidy up created settings
        """ try:
            core_api = client.CoreV1Api(aApiClient)
            resp = core_api.delete_namespaced_config_map(name="kubernetes-dashboard-settings", namespace='kube-system')
        except ApiException as e:
            print("Exception deleting config map: %s\n"%e) """

    def test_e_create_cluster_role(self):
        # create cluster role
        try:
            utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/" + "dashboard-clusterrole.yaml")
            core_api = client.RbacAuthorizationV1Api(aApiClient)
            cluster_resp = core_api.read_cluster_role(name="kubernetes-dashboard")
            #print("cluster role response %s " %cluster_resp)

            self.assertIsNotNone(cluster_resp)

        except ApiException as e:
            print("Exception creating cluster role: %s\n"%e)

        # tidy up created settings
        """ try:
            core_api = client.RbacAuthorizationV1Api(aApiClient)
            resp = core_api.delete_namespaced_cluster_role(name="kubernetes-dashboard", namespace='kube-system')
        except ApiException as e:
            print("Exception deleting cluster role: %s\n"%e) """

    def test_f_create_role_bindings(self):
        # create cluster role
        try:
            utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/" + "dashboard-rolebinding.yaml")
            core_api = client.RbacAuthorizationV1Api(aApiClient)
            role_resp = core_api.read_namespaced_role(name="kubernetes-dashboard", namespace="kube-system")
            #print("role response %s " %role_resp)

            self.assertIsNotNone(cluster_resp)

        except ApiException as e:
            print("Exception creating role: %s\n"%e)

        # tidy up created settings
        """ try:
            core_api = client.RbacAuthorizationV1Api(aApiClient)
            resp = core_api.delete_namespaced_role(name="kubernetes-dashboard", namespace='kube-system')
        except ApiException as e:
            print("Exception deleting role: %s\n"%e) """

    def test_g_create_cluster_role_bindings(self):
        # create cluster role
        try:
            utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/" + "dashboard-clusterrolebinding.yaml")
            core_api = client.RbacAuthorizationV1Api(aApiClient)
            role_resp = core_api.read_cluster_role_binding(name="kubernetes-dashboard")
            #print("role response %s " %role_resp)

            self.assertIsNotNone(cluster_resp)

        except ApiException as e:
            print("Exception creating role: %s\n"%e)

        # tidy up created settings
        """ try:
            core_api = client.RbacAuthorizationV1Api(aApiClient)
            resp = core_api.delete_cluster_role_binding(name="kubernetes-dashboard", namespace='kube-system')
        except ApiException as e:
            print("Exception deleting role: %s\n"%e) """

    def test_h_create_deployment(self):
        # create deployment
        try:
            utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/" + "dashboard-deployment.yaml")
            apps_api = client.AppsV1Api(aApiClient)
            deploy_resp = apps_api.read_namespaced_deployment(name="kubernetes-dashboard", namespace="kube-system")
            #print("deploy response %s " %deploy_resp)

            self.assertIsNotNone(deploy_resp)

        except ApiException as e:
            print("Exception creating app: %s\n"%e)

        # tidy up created settings
        """ try:
            apps_api = client.AppsV1Api(aApiClient)
            resp = apps_api.delete_namespaced_deployment(name="kubernetes-dashboard", namespace='kube-system')
        except ApiException as e:
            print("Exception deleting app: %s\n"%e) """


    def test_i_create_metrics_service(self):
        # create service
        try:
            utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/" + "dashboard-metrics-service.yaml")
            core_api = client.CoreV1Api(aApiClient)
            deploy_resp = core_api.read_namespaced_service(name="dashboard-metrics-scraper", namespace="kube-system")
            #print("deploy response %s " %deploy_resp)

            self.assertIsNotNone(deploy_resp)

        except ApiException as e:
            print("Exception creating service: %s\n"%e)

        # tidy up created settings
        """ try:
            core_api = client.CoreV1Api(aApiClient)
            resp = core_api.delete_namespaced_service(name="dashboard-metrics-scraper", namespace='kube-system')
        except ApiException as e:
            print("Exception deleting service: %s\n"%e) """


    def test_j_create_metrics_deployment(self):
        # create deployment
        try:
            utils.create_from_yaml(
                aApiClient, filepath + "cluster/files/" + "dashboard-metrics-deploy.yaml")
            apps_api = client.AppsV1Api(aApiClient)
            deploy_resp = apps_api.read_namespaced_deployment(name="dashboard-metrics-scraper", namespace="kube-system")
            #print("deploy response %s " %deploy_resp)

            self.assertIsNotNone(deploy_resp)

        except ApiException as e:
            print("Exception creating app: %s\n"%e)

        # tidy up created settings
        """ try:
            apps_api = client.AppsV1Api(aApiClient)
            resp = apps_api.delete_namespaced_deployment(name="dashboard-metrics-scraper", namespace='kube-system')
        except ApiException as e:
            print("Exception deleting app: %s\n"%e) """


if __name__ == '__main__':
    unittest.main(warnings='ignore')