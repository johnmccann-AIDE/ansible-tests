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

    # Create a ApiClient with our config
    aApiClient = client.ApiClient(aConfiguration)
    
    # Do calls
    v1 = client.CoreV1Api(aApiClient)
    print ("Waiting for Nodes to be ready.....")
    while True:
        c = 0
        ret = v1.list_node(watch=False)
        #print("Node\tStatus\tRole\tInternalIP\tOS-Image")
        itemc = len(ret.items)
        for i in ret.items:
            noderole = "None"
            stat = "None"
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
            #print("%s\t%s" %
            #      (i.metadata.name, stat))
                  #, noderole, ipAddr, i.status.node_info.os_image))
            if "Ready" in stat:
                c = c + 1
        if c == itemc:
            break

if __name__ == '__main__':
    main()
