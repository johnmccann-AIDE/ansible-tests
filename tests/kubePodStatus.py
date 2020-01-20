import os
import urllib3
import yaml
from kubernetes import client, config


def main():
    # Define the barer token we are going to use to authenticate.
    # See here to create the token:
    # https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/
    aToken = ""
   
    # disable warnings
    #urllib3.disable_warnings()
    yaml.warnings({'YAMLLoadWarning': False})

    # Create a configuration object
    # aConfiguration = client.Configuration()
    aConfiguration = config.load_kube_config()

    # Specify the endpoint of your Kube cluster
    # aConfiguration.host = "https://172.26.138.146:6443"
    # aConfiguration.host = str(apiserver)
    # aConfiguration.api_key = {"Authorization": "Bearer " + str(aToken)}

    # Create a ApiClient with our config
    aApiClient = client.ApiClient(aConfiguration)
    
    # Do calls
    v1 = client.CoreV1Api(aApiClient)
    print("Listing services:")
    ret = v1.list_namespaced_service("kube-system")
    for i in ret.items:
        #print("pods: %s"%i)
        print("%s\t%s\t%s\t%s" %
              (i.metadata.name, i.spec.type, i.spec.cluster_ip, i.spec.external_i_ps))
        #ret2 = v1.list_namespaced_service(name=i.metadata.name, namespace=i.metadata.namespace)
        #print("status - %s"%ret2)

if __name__ == '__main__':
    main()
