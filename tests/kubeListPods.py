import os
import urllib3
import yaml
from kubernetes import client, config


def main():
    # Define the barer token we are going to use to authenticate.
    # See here to create the token:
    # https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/
    #apiserver = os.system("kubectl config view --minify | grep server | cut -f 2- -d ':' | tr -d ' '")
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
    print("Name\tNamespace\tNode\tIp\tStatus\tLiveness Probe\tReadiness Probe")
    #ret = v1.list_pod_for_all_namespaces(watch=False)
    namespaces = {"default", "kube-system"}
    for namespace in namespaces:
        print("Namespace: %s"%namespace)
        ret = v1.list_namespaced_pod(namespace)
        #print("result %s"%ret)
        if not ret.items :
            print("Error: No pods running in %s namespace"%namespace)
        else:
            for i in ret.items:
                # i.metadata.name, i.metadata.namespace, i.spec.node_name, i.status.pod_ip, i.status.phase
                #print("pods: %s"%i)
                if "Running" not in i.status.phase:
                    print("Pod %s is not running"%i.metadata.name)
                if not i.spec.containers[0].liveness_probe:
                    lprobe = "None"
                    #print("No Liveness Probe defined: %s"%i.spec.containers[0].liveness_probe)
                else:
                    if not i.spec.containers[0].liveness_probe.http_get:
                        lprobe = "None"
                        #print("probe: %s"%i.spec.containers[0].liveness_probe)
                    else:
                        lprobe = i.spec.containers[0].liveness_probe.http_get.path + ":" + str(i.spec.containers[0].liveness_probe.http_get.port)
                        #print("Liveness Probe defined: %s"%lprobe)
                if not i.spec.containers[0].readiness_probe:
                    rprobe = "None"
                    #print("No Readiness Probe defined: %s"%i.spec.containers[0].readiness_probe)
                else:
                    if not i.spec.containers[0].readiness_probe.http_get:
                        rprobe = "None"
                        #print("probe: %s"%i.spec.containers[0].readiness_probe)
                    else:
                        rprobe = i.spec.containers[0].readiness_probe.http_get.path + ":" + str(i.spec.containers[0].readiness_probe.http_get.port)
                        #print("Readiness Probe defined: %s"%rprobe)
                print("%s\t%s\t%s\t%s\t%s\t%s\t%s" %
                    (i.metadata.name, i.metadata.namespace, i.spec.node_name, i.status.pod_ip, i.status.phase, lprobe, rprobe))


if __name__ == '__main__':
    main()
