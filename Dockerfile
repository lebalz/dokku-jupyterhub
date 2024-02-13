# Do not forget to pin down the version
FROM jupyterhub/jupyterhub:4.0.2


# Install dependencies (for advanced authentication and spawning)
RUN pip3 install \
    dockerspawner==13.0.0 \
    oauthenticator==16.2.1 \
    jupyterhub-idle-culler==1.2.1 \
    psycopg2-binary==2.9.9

RUN pip3 install PyJWT==2.8.0

# Copy the custom authenticator

COPY my_azuread.py .

RUN mv my_azuread.py $(dirname "$(python3 -c "import oauthenticator as _; print(_.__file__)")")/my_azuread.py

# Copy the JupyterHub configuration into the container
COPY jupyterhub_config.py .

# Copy the POST_DEPLOY_SCRIPT into the container
COPY POST_DEPLOY_SCRIPT .

# Copy the notebook dockerfile into the container
COPY images ./images