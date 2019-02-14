# autodetectimagespawner

Jupyterhub spawner (based on DockerSpawner) to auto detect docker images with respect to a user pattern. Default pattern is suitable for jupyter/docker-stacks images :

    jupyter/(.+)-notebook:(.+)

Note that pattern should be a regular expression.

First, pull [jupyter/docker-stacks](https://github.com/jupyter/docker-stacks) images, for instance :

    docker pull jupyter/base-notebook
    docker pull jupyter/minimal-notebook
    docker pull jupyter/scipy-notebook
    docker pull jupyter/r-notebook

Second, install python package 'autodetectimagespawner' from root of project :

    pip install -e .

Then, the spawner class should be :

    c.JupyterHub.spawner_class = 'autodetectimagespawner.AutoDetectImageSpawner'

Working with docker containers implies security, so be sure to use ssl key/certificate. See the ssl directory and feel free to use these ones for testing :

    c.JupyterHub.ssl_key = 'ssl/jupyterhub.key'
    c.JupyterHub.ssl_cert = 'ssl/jupyterhub.crt'

Althought, please see [here](https://jupyter-notebook.readthedocs.io/en/latest/public_server.html#using-ssl-for-encrypted-communication) for more information.  

To run the hub on host, the hub configuration should be : 

    from jupyter_client.localinterfaces import public_ips
    c.JupyterHub.hub_ip = public_ips()[0]

To run the hub in docker, create a docker network, for instance :

    docker network create jupyterhub-network

Define the network in the spawner configuration :

    c.DockerSpawner.use_internal_ip = True
    c.DockerSpawner.network_name = 'jupyterhub-network'
    c.DockerSpawner.extra_host_config = { 'network_mode': 'jupyterhub-network' }
    
In that case, DNS can bind the name of the container, for instance 'jupyterhub' :

    c.JupyterHub.hub_ip = 'jupyterhub'

Build the docker :

    docker build -t autodetectimagespawner:0.1 .

Run the docker using mount volumes (PAM and socket), network and naming :
    
    docker run -p 8000:8000 \
    	       -v /etc/passwd:/etc/passwd \
	       -v /etc/shadow:/etc/shadow \
	       -v /var/run/docker.sock:/var/run/docker.sock \
	       --network jupyterhub-network \
	       --name jupyterhub \
	       autodetectimagespawner:0.1
