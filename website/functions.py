#importing libraries
from kubernetes import client
import subprocess

#function to create a username string from the login manager user
def get_username(user):
    username = str(user).replace("<","")
    username = username.replace(">","")
    username = username.replace(" ","")
    return username

#function to create the studentnumber string from the login manager user
def get_studentnumber(user):
    studentnumber = str(user).replace("<student ","")
    studentnumber = studentnumber.replace(">","")
    return studentnumber

#function to delete a namespace from the kubernetes cluster with the help of the command line
def delete_namespace(name):
    subprocess.run(['kubectl', 'delete', 'namespace', name])

#function to label a kubernetes pod in the kubernetes cluster with the help of the command line
def label_pod(name):
    subprocess.run(['kubectl', 'label', 'pod', name,'-n', name ,'app=capture-the-flag-1'])

#function to expose a kubernetes pod in the kubernetes cluster with the help of the command line
def expose_pod(name):
    subprocess.run(['kubectl', 'expose', 'pod', name, '-n', name, '--type=NodePort', '--port', '31139', '--target-port=22'])

#function to create a kubernetes namespace and pod in the kubernetes cluster with the help of the command line
def create_pod(name,id):
    #create an api instance from the library
    api_instance = client.CoreV1Api()

    #create a kubernetes container template
    container     = client.V1Container(
        name      = str("ctf-challenge" + id),
        image     = str("ghcr.io/forwardit332/ctf-challenge" + id + ":latest"),
        ports     = [client.V1ContainerPort(container_port=22)]
    )
    #initialize container accordint to the library with the template
    pod_spec = client.V1PodSpec(containers=[container])
    #give the container a name
    metadata = client.V1ObjectMeta(name=name)
    #create the pod template with information from above
    pod = client.V1Pod(
        api_version="v1",
        kind="Pod",
        metadata=metadata,
        spec=pod_spec
    )
    #create a namespace for the user
    api_instance.create_namespace(body=client.V1Namespace(metadata=client.V1ObjectMeta(name=name)))
    #create the the pod on the kubernetes service
    api_instance.create_namespaced_pod(body=pod, namespace=name)

#function to create an access url string of the kubernetes pod with the help of the command line
def get_ip_address(name):
    #create an api instance from the library
    v1 = client.CoreV1Api()
    #variable to store the pod ip in
    pod_ip = ""
    #use the api instance to list all the pods with the given namespace
    pod_list = v1.list_namespaced_pod(namespace=name)
    #iterate through the list to get the ip of the host which is in this case only 1.
    for pod in pod_list.items:
        pod_ip = str(pod.status.host_ip)
    return str(pod_ip)

def get_port_address(name):
    #create an api instance from the library
    v1 = client.CoreV1Api()
    #variable to store the pod port in
    pod_port = ""
    #use the api instance to list all the services with the given namespace
    service = v1.read_namespaced_service(name=name,namespace=name)
    #iterate through the list to get the port of the host which is in this case only 1
    for port in service.spec.ports:
        pod_port = str(port.node_port)
    return str(pod_port)

def connect_to_shellinabox(port):
    #start the shellinabox web terminal and port into an http access string
    subprocess.run(['shellinaboxd', '-t', '-b', '-p', port])
    #formating the shellinabox web terminal and port into an http access string
    return str( "http://192.168.2.40:" + port)

