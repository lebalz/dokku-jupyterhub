import os
import sys
from pathlib import Path
import shutil
from oauthenticator.my_azuread import MyAzureAdOAuthenticator
from dockerspawner import DockerSpawner

PREFIX = 'scf'
ADMINS = set(['lukas-schaffner--gbsl-ch', 'christian-schneeberger--gbsl-ch'])
HOME_PATH = '/home/jovyan/work'
APP_NAME = f'{PREFIX}-jupyter'
APP_ROOT_HOST = f'/var/lib/dokku/data/storage/{APP_NAME}'

VOLUME_GROUPS = {
    'data-science': [
        f'{APP_ROOT_HOST}/groups/data-science'
    ]
}

MEMBERSHIPS = {
    'lukas-schaffner--gbsl-ch': set(['data-science']),
    'christian-schneeberger--gbsl-ch': set(['data-science']),
}

PERFORMANCE_LIMITS = {
    'lukas-schaffner--gbsl-ch': '8G',
    'christian-schneeberger--gbsl-ch': '8G',
}


class MyDockerSpawner(DockerSpawner):

    def start(self):
        username = self.user.name
        if self.user.name in ADMINS:
            shared_mode = 'rw'
        else:
            shared_mode = 'ro'
        root = Path(notebook_dir)
        # basic volumes
        self.volumes = {
            f'{APP_ROOT_HOST}/data/users/{username}': {'bind': notebook_dir, 'mode': 'rw'},
            f'{APP_ROOT_HOST}/data/user-settings/{username}': {'bind': '/home/jovyan/.jupyter/lab', 'mode': 'rw'},
            f'{APP_ROOT_HOST}/data/shared': {'bind': str(root.joinpath('shared')), 'mode': shared_mode},
            f'{APP_ROOT_HOST}/data/colab': {'bind': str(root.joinpath('colab')), 'mode': 'rw'}
        }

        # additional volumes for assigned students only
        if self.user.name in MEMBERSHIPS:
            for group in MEMBERSHIPS[self.user.name]:
                for group_dir in VOLUME_GROUPS[group]:
                    # make a relative path to mount, e.g.
                    #   /var/lib/dokku/data/storage/jupyterhub/groups/data-science/
                    # will be mounted to
                    #   /groups/data-science/
                    parts = Path(group_dir).relative_to(APP_ROOT_HOST).parts

                    self.volumes[group_dir] = {
                        'bind': str(root.joinpath(*parts)),
                        'mode': shared_mode
                    }

        if self.user.name in ADMINS:
            self.volumes[f'{APP_ROOT_HOST}/data/users'] = {
                'bind': str(root.joinpath('users')),
                'mode': 'rw'
            }

        if self.user.name in PERFORMANCE_LIMITS:
            self.extra_host_config = {
                'mem_limit': PERFORMANCE_LIMITS[self.user.name],
                'memswap_limit': '-1'
            }
        return super().start()


c.JupyterHub.spawner_class = MyDockerSpawner
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
        dir_path.mkdir(exist_ok=True)
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


notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or HOME_PATH
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container

c.DockerSpawner.extra_host_config = {
    'mem_limit': '350m',
    'memswap_limit': '-1'
}
#    'mem_swappiness': 0


# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
c.DockerSpawner.name_template = f'{PREFIX}{"-{prefix}-{username}"}'
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
c.Authenticator.admin_users = ADMINS

# admin can access all other users
c.JupyterHub.admin_access = True

c.Spawner.default_url = '/lab'
