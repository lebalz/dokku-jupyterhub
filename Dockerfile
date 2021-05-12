# Do not forget to pin down the version
FROM jupyterhub/jupyterhub:1.3.0

# Install dependencies (for advanced authentication and spawning)
RUN pip3 install \
    dockerspawner==0.11.1 \
    oauthenticator==0.12.3 \
    jupyterhub-idle-culler==1.0.0 \
    psycopg2-binary==2.8.6

RUN pip3 install oauthenticator==14.0.0 PyJWT==1.7.1

# Copy the custom authenticator

COPY my_azuread.py .

RUN mv my_azuread.py $(dirname "$(python3 -c "import oauthenticator as _; print(_.__file__)")")/my_azuread.py

# Copy the JupyterHub configuration in the container
COPY jupyterhub_config.py .

# Copy the POST_DEPLOY_SCRIPT in the container
COPY POST_DEPLOY_SCRIPT .

# Copy the notebook dockerfile in the container
COPY images ./images
