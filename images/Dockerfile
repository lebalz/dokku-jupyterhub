FROM jupyter/minimal-notebook:lab-4.0.7

LABEL maintainer="scf"
LABEL version="latest"
LABEL description="Jupyter Notebook image"

USER root
# graphviz and graphviz-dev is needed for use with jupyterlab
RUN apt-get update -y && apt-get install -y graphviz graphviz-dev
USER jovyan

# all additional pip packages
RUN pip3 install --no-cache \
    jupyterhub==5.4.3 \
    jupyterlab==4.5.6 \
    notebook==7.5.5 \
    numpy==2.4.3 \
    Pillow==12.1.1 \
    XlsxWriter==3.2.9 \
    pandas==3.0.1 \
    xlrd==2.0.2 \
    openpyxl==3.1.5 \
    ipywidgets==8.1.8 \
    ipympl==0.10.0 \
    jupyterlab-spellchecker==0.8.4 \
    scipy==1.17.1 \
    'python-lsp-server[all]'==1.14.0 \
    ipycanvas==0.14.3\
    orjson==3.11.7\
    graphviz==0.21\
    termcolor==3.3.0\
    colour-science==0.4.7\
    jupyterlab-lsp==5.3.0

#   PGPLOT
# RUN pip3 install --no- \
#     traitlets==4.3.3 \
#     traittypes==0.2.1 \
#     bqplot==0.12.26
    


# check where to put the overrides file within a jupyterlab container: 
#       jupyter lab path
COPY --chmod=644 overrides.json /opt/conda/share/jupyter/lab/settings/
