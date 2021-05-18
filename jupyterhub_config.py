import os
import sys
from pathlib import Path
import shutil
from oauthenticator.my_azuread import MyAzureAdOAuthenticator

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.JupyterHub.last_activity_interval = 150
c.JupyterHub.shutdown_on_logout = True

# Spawn containers from this image
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_IMAGE']

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


def ensure_dir(dir_path):
    if not dir_path.exists():
        dir_path.mkdir_p(exist_ok=True)
    if dir_path.group() != 'users':
        shutil.chown(str(dir_path), user=1000, group=100)


def set_user_permission(spawner):
    '''ensures the correct access rights for the jupyterhub user group'''
    username = spawner.user.name
    container_data = os.environ.get('DATA_VOLUME_CONTAINER', '/data')
    data_root = Path(container_data, 'users')
    ensure_dir(data_root)
    ensure_dir(data_root.joinpath(username))
    settings_root = Path(container_data, 'user-settings')
    ensure_dir(settings_root)
    ensure_dir(settings_root.joinpath(username))


c.Spawner.pre_spawn_hook = set_user_permission

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.


notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {
    '/var/lib/dokku/data/storage/hfr-jupyterhub/data/users/{username}': {'bind': notebook_dir, 'mode': 'rw'},
    '/var/lib/dokku/data/storage/hfr-jupyterhub/data/user-settings/{username}': {'bind': '/home/jovyan/.jupyter/lab/user-settings', 'mode': 'rw'},
    '/var/lib/dokku/data/storage/hfr-jupyterhub/data/shared': {'bind': '/home/jovyan/work/shared', 'mode': 'ro'},
    '/var/lib/dokku/data/storage/hfr-jupyterhub/data/colab': {'bind': '/home/jovyan/work/colab', 'mode': 'rw'}
}

c.DockerSpawner.extra_host_config = {
    'mem_limit': '350m',
    'memswap_limit': '-1'
}
#    'mem_swappiness': 0

# # shutdown the server after no activity for an hour
# c.NotebookApp.shutdown_no_activity_timeout = 60 * 60
# # shutdown kernels after no activity for 20 minutes
# c.MappingKernelManager.cull_idle_timeout = 20 * 60
# # check for idle kernels every two minutes
# c.MappingKernelManager.cull_interval = 2 * 60


# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
c.DockerSpawner.name_template = 'hfr-{prefix}-{username}'
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = False

# c.JupyterHub.bind_url = 'http://127.0.0.1:8000'

c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = os.environ['HUB_IP']
c.JupyterHub.services = [
    {
        'name': 'idle-culler',
        'admin': True,
        'command': [
            sys.executable,
            '-m',
            'jupyterhub_idle_culler',
            '--timeout=300'
        ],
    }
]


# Authenticate users with GitHub OAuth
# c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
# c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
c.JupyterHub.authenticator_class = MyAzureAdOAuthenticator
c.MyAzureAdOAuthenticator.tenant_id = os.environ.get('AAD_TENANT_ID')
c.MyAzureAdOAuthenticator.oauth_callback_url = os.environ.get('AAD_OAUTH_CALLBACK_URL')
c.MyAzureAdOAuthenticator.client_id = os.environ.get('AAD_CLIENT_ID')
c.MyAzureAdOAuthenticator.client_secret = os.environ.get('AAD_CLIENT_SECRET')

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')
c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
                                               'jupyterhub_cookie_secret')

c.JupyterHub.db_url = os.environ['DATABASE_URL']


# Whitlelist users and admins
# c.Authenticator.allowed_users = whitelist = set(['lebalz', 'test-user-reto'])

c.Authenticator.admin_users = admin = set(['lebalz', 'balthasar-hofer--gbsl-ch'])
# c.Authenticator.username_map = {
#     "balthasar-hofer--gbsl-ch": "lebalz",
# }
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
