# Do not forget to pin down the version
FROM jupyterhub/jupyterhub:5.4.3


# Install dependencies (for advanced authentication and spawning)
RUN pip3 install \
    dockerspawner==14.0.0 \
    oauthenticator==17.3.0 \
    jupyterhub-idle-culler==1.4.0 \
    psycopg2-binary==2.9.11

RUN pip3 install PyJWT==2.12.1

# Copy the custom authenticator
COPY my_azuread.py .

RUN mv my_azuread.py $(dirname "$(python3 -c "import oauthenticator as _; print(_.__file__)")")/my_azuread.py

# Copy the JupyterHub configuration into the container
COPY jupyterhub_config.py .

# Copy the POST_DEPLOY_SCRIPT into the container
COPY POST_DEPLOY_SCRIPT .

# Copy the notebook dockerfile into the container
COPY images ./images

RUN cat > /entrypoint.sh <<'EOF'
#!/bin/bash
set -e
jupyterhub upgrade-db
exec jupyterhub "$@"
EOF
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]