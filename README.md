# Dokku Jupyterhub

Expecting dokku service name is set via 'APP', e.g. `APP='jupyterhub'`

```sh
APP="jupyterhub"
DOMAIN="your.domain.com"
# create app
dokku apps:create $APP
# ensure docker networks can be used
dokku config:set $APP DOCKER_SCHEDULER=docker-local

# configure port map for accessing hub
dokku config:set $APP DOKKU_PROXY_PORT_MAP="http:80:8000"

# mount docker socket to spawn new containers
dokku storage:mount $APP /var/run/docker.sock:/var/run/docker.sock

# add a domain to it
dokku domains:add $APP $DOMAIN

# create network
dokku network:create $APP
dokku network:set $APP bind-all-interfaces true

# attach the network to the app
dokku network:set $APP attach-post-create $APP

# configure env variables for the network
dokku config:set $APP DOCKER_NETWORK_NAME=$APP
dokku config:set $APP HUB_IP=$APP.web

# create postgres service
dokku postgres:create $APP
dokku postgres:link $APP $APP

# DATA PERSISTENCE

mkdir -p /var/lib/dokku/data/storage/$APP/data
dokku storage:mount $APP /var/lib/dokku/data/storage/$APP/data:/data

## create shared directories
mkdir -p /var/lib/dokku/data/storage/$APP/data/shared
mkdir -p /var/lib/dokku/data/storage/$APP/data/colab

## grant user jovian:users access to colab
chown -R 1000:100 /var/lib/dokku/data/storage/$APP/data/colab

# increase max body upload size
dokku nginx:set $APP client-max-body-size 30m


# OAUTH
### edit your credentials: `nano /home/dokku/$APP/ENV`

## github oauth config
# dokku config:set $APP OAUTH_CALLBACK_URL="https://$DOMAIN/hub/oauth_callback"
# dokku config:set $APP GITHUB_CLIENT_ID="XXXXXXXXXXXXXX"
# dokku config:set $APP GITHUB_CLIENT_SECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

## azure active directory
dokku config:set $APP AAD_TENANT_ID="xxxxxx-xxxxxx-xxxxxxx"
dokku config:set $APP AAD_OAUTH_CALLBACK_URL="https://$DOMAIN/hub/oauth_callback"
dokku config:set $APP AAD_CLIENT_ID="xxxxxx-xxxxxx-xxxxxxx"
dokku config:set $APP AAD_CLIENT_SECRET="xxxxxx-xxxxxx-xxxxxxx"

```

## Images

Make sure all used images are available on the system. Either pull them yourself or setup your own image (e.g. with a postdeploy script).

```sh
docker pull jupyter/scipy-notebook:latest

# and set the network as default
dokku config:set $APP DOCKER_JUPYTER_IMAGE="jupyter/scipy-notebook:latest"
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
MAIL="your@email.address"
dokku config:set --no-restart $APP DOKKU_LETSENCRYPT_EMAIL=$MAIL
dokku letsencrypt $APP
```
