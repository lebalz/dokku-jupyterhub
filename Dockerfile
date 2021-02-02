# Do not forget to pin down the version
FROM jupyterhub/jupyterhub:1.3.0

# Copy the JupyterHub configuration in the container
COPY jupyterhub_config.py .

# Install dependencies (for advanced authentication and spawning)
RUN pip install \
    dockerspawner==0.11.1 \
    oauthenticator==0.12.3 \
    jupyterhub-idle-culler==1.0.0 \
    psycopg2-binary==2.8.6