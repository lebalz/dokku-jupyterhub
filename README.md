# Dokku Jupyterhub

Expecting dokku service name `jupyterhub`

```sh
dokku apps:create jupyterhub
dokku config:unset --no-restart jupyterhub
dokku network:create jupyterhub
dokku network:set jupyterhub attach-post-create jupyterhub
docker pull jupyterlab/scipy-notebook:latest
```

## ENV's

run `nano /home/dokku/jupyterhub/ENV` and edit as follows

```sh
DOCKER_JUPYTER_IMAGE="jupyterlab/scipy-notebook:latest"
DOCKER_NETWORK_NAME="jupyerhub"
HUB_IP="jupyerhub.web"
```
