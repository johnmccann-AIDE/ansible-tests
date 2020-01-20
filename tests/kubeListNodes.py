import os
import urllib3
import yaml
from jnpr.junos.factory.factory_loader import FactoryLoader
from os.path import expanduser
from kubernetes import client, config

def main():
    # Define the barer token we are going to use to authenticate.
    # See here to create the token:
    # https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/
    aToken = ""
    home = expanduser("~")
    yaml.warnings({'YAMLLoadWarning': False})
    pretty = 'pretty_example'

    # Create a configuration object
    aConfiguration = config.load_kube_config()
    # path = home + "/.kube/config"
    # with open(path) as f:
    #    data = yaml.load(f, Loader=yaml.KubeConfigLoader)
    #    print(data)
    # globals().update(FactoryLoader().load(data))
    # aConfiguration = config.load_kube_config(config_file=path)
    # aConfiguration = FactoryLoader().load(data)

    # Create a ApiClient with our config
    aApiClient = client.ApiClient(aConfiguration)
    
    # Do calls
    v1 = client.CoreV1Api(aApiClient)
    ret = v1.list_node(watch=False)
    print("Node\tStatus\tRole\tInternalIP\tOS-Image")
    for i in ret.items:
        noderole = "None"
        for label in i.metadata.labels:
            if "node-role" in label:
                nodelabel = label.split("/")
                noderole = nodelabel[1].strip()
        for cond in i.status.conditions:
            if "KubeletReady" in cond.reason:
                stat = str(cond.type)
        for addr in i.status.addresses:
            if "InternalIP" in addr.type:
                #print("IP: %s"%addr)
                ipAddr = str(addr.address)
        print("%s\t%s\t%s\t%s\t%s" %
              (i.metadata.name, stat, noderole, ipAddr, i.status.node_info.os_image))
    #print("Listing node status:")
    #ret2 = v1.read_node_status("melmore.jnpr.belfast", pretty=pretty)
    #print("results %s"%ret2)
    

if __name__ == '__main__':
    main()
