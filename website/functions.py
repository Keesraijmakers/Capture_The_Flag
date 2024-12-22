#importing libraries
from kubernetes import client
from kubernetes.client.rest import ApiException
import subprocess


#function to create a string username from the login manager username tag
def get_username(user):
    username = str(user).replace("<","")
    username = username.replace(">","")
    username = username.replace(" ","")
    return username


#function to get the kubernetes nodes with the help of the command line
def get_nodes():
    subprocess.run(['kubectl', 'get', 'nodes'])


#function to get the kubernetes pods with the help of the command line
def get_pods(name):
    subprocess.run(['kubectl', 'get', 'pods', '-n', name])


#function to delete a kubernetes node with the help of the command line
def delete_pods(name):
    subprocess.run(['kubectl', 'delete', 'pod' ,name, '-n', name])


#function to delete a kubernetes service with the help of the command line
def delete_service(name):
    subprocess.run(['kubectl', 'delete', 'service', '-n', name, name])


#function to create a kubernetes pod with the help of the command line
def create_pod(name):
    #create an api instance from the library
    api_instance = client.CoreV1Api()
    #create a kubernetes container template
    container     = client.V1Container(
        name      = "ctf-challenge1",
        image     = "ghcr.io/forwardit332/ctf-challenge1:1.0",
        ports     = [client.V1ContainerPort(container_port=80)]
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
    #create the the pod on the kubernetes service
    api_instance.create_namespaced_pod(body=pod, namespace=name)

#function to label a kubernetes pod with the help of the command line
def label_pod(name):
    subprocess.run(['kubectl', 'label', 'pod', '-n', name, name ,'app=capture-the-flag-1'])

#function to expose a kubernetes pod with the help of the command line
def expose_pod(name):
    subprocess.run(['kubectl', 'expose', 'pod', '-n', name, name, '--type=NodePort', '--port', '31139', '--target-port=80'])

#function to create an access url string of the kubernetes pod with the help of the command line
def get_address(name):
    #create an api instance from the library
    v1 = client.CoreV1Api()
    #variable to store the pod ip in
    pod_ip = ""
    #use the api instance to list all the pods with the given namespace
    pod_list = v1.list_namespaced_pod(namespace=name)
    #iterate through the list to get the ip of the host which is in this case only 1.
    for pod in pod_list.items:
        pod_ip = str(pod.status.host_ip)

    #variable to store the pod port in
    pod_port = ""
    #use the api instance to list all the services with the given namespace
    service = v1.read_namespaced_service(name=name,namespace=name)
    #iterate through the list to get the port of the host which is in this case only 1
    for port in service.spec.ports:
        pod_port = str(port.node_port)

    #formating the ip and port into an access string
    return str( "http://" + pod_ip + ":" + pod_port + "/")

