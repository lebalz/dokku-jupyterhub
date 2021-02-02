# Dokku Jupyterhub

Expecting dokku service name `jupyterhub`

```sh
# create app
dokku apps:create jupyterhub
# ensure docker networks can be used
dokku config:set jupyterhub DOCKER_SCHEDULER=docker-local

# configure port map for accessing hub
dokku config:set jupyterhub DOKKU_PROXY_PORT_MAP="http:80:8000"

# mount docker socket to spawn new containers
dokku storage:mount jupyterhub /var/run/docker.sock:/var/run/docker.sock

# add a domain to it
dokku domains:add jupyterhub "your.domain.com"

# create network
dokku network:create jupyterhub
dokku network:set jupyterhub bind-all-interfaces true

# attach the network to the app
dokku network:set jupyterhub attach-post-create jupyterhub

# configure env variables for the network
dokku config:set jupyterhub DOCKER_NETWORK_NAME=jupyterhub
dokku config:set jupyterhub HUB_IP=jupyterhub.web

# create postgres service
dokku postgres:create jupyterhub
dokku postgres:link jupyterhub jupyterhub

# data persistence
mkdir -p /var/lib/dokku/data/storage/jupyterhub/data
dokku storage:mount jupyterhub /var/lib/dokku/data/storage/jupyterhub/data:/data

# add cookie secret
openssl rand -hex 32 > /var/lib/dokku/data/storage/jupyterhub/data/jupyterhub_cookie_secret
```

## Images

Make sure all used images are available on the system

```sh
docker pull jupyterlab/scipy-notebook:latest

# and set the network as default
dokku config:set jupyterhub DOCKER_JUPYTER_IMAGE="jupyter/scipy-notebook:latest"
```

### initial local setup

```sh
git remote add dokku dokku@<your-ip>:jupyterhub
```

## Letsencrypt

Make sure:

- you have set a domain and your page is reachable
- no pagerules with permanent redirects e.g. from Cloudflare exists

```sh
dokku config:set --no-restart jupyterhub DOKKU_LETSENCRYPT_EMAIL=your@email.address
dokku letsencrypt jupyterhub
```
