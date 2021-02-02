import os
import sys

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Spawn containers from this image
c.DockerSpawner.container_image = os.environ['DOCKER_JUPYTER_IMAGE']

# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
# spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
# c.DockerSpawner.extra_create_kwargs.update({'command': spawn_cmd})

c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True

# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = {'network_mode': os.environ['DOCKER_NETWORK_NAME']}

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.

notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {'jupyterhub-user-{username}': notebook_dir}

# c.DockerSpawner.volumes = {
#     '/srv/jupyterhub/{username}': notebook_dir,
#     '/srv/jupyterhub/shared': '/home/jovyan/shared'
# }
c.Spawner.mem_limit = '128M'
# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = os.environ['HUB_IP']
c.JupyterHub.services = [
    {
        'name': 'idle-culler',
        'admin': True,
        'command': [
            sys.executable,
            '-m', 'jupyterhub_idle_culler',
            '--timeout=3600'
        ],
    }
]


# Authenticate users with GitHub OAuth
c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']


# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')
c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
                                               'jupyterhub_cookie_secret')

c.JupyterHub.db_url = os.environ['DATABASE_URL']


# Whitlelist users and admins
c.Authenticator.allowed_users = whitelist = set(['lebalz'])
c.Authenticator.admin_users = admin = set(['lebalz'])
c.JupyterHub.admin_access = True
# pwd = os.path.dirname(__file__)
# with open(os.path.join(pwd, 'userlist')) as f:
#     for line in f:
#         if not line:
#             continue
#         parts = line.split()
#         # in case of newline at the end of userlist file
#         if len(parts) >= 1:
#             name = parts[0]
#             whitelist.add(name)
#             if len(parts) > 1 and parts[1] == 'admin':
#                 admin.add(name)

c.Spawner.default_url = '/lab'
