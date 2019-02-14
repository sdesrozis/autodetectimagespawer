c = get_config()

c.JupyterHub.spawner_class = 'autodetectimagespawner.AutoDetectImageSpawner'

# Remove containers when shutdown
c.DockerSpawner.remove_containers = True

# Avoid errors from multiple session...
c.PAMAuthenticator.open_sessions = False

# On host
#from jupyter_client.localinterfaces import public_ips
#c.JupyterHub.hub_ip = public_ips()[0]

# On docker
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = 'jupyterhub-network'
c.DockerSpawner.extra_host_config = { 'network_mode': 'jupyterhub-network' }
c.JupyterHub.hub_ip = 'jupyterhub'

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000

c.JupyterHub.ssl_key = 'ssl/jupyterhub.key'
c.JupyterHub.ssl_cert = 'ssl/jupyterhub.crt'
