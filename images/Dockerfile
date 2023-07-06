FROM jupyter/minimal-notebook:hub-4.0.2


LABEL maintainer="hfr"
LABEL version="0.1.4"
LABEL description="Jupyter Notebook image"

USER root
# graphviz and graphviz-dev is needed for use with jupyterlab
RUN apt-get update -y && apt-get install -y graphviz graphviz-dev
USER jovyan

# all additional pip packages
RUN pip3 install --no-cache \
    jupyterhub==4.0.1 \
    smartphone-connector==0.0.115 \
    notebook==6.5.4 \
    playsound==1.2.2 \
    numpy==1.22.3 \
    gTTs==2.2.2 \
    jupyterlab-drawio==0.9.0 \
    Pillow==9.0.1 \
    XlsxWriter==3.0.3 \
    pandas==1.4.1 \
    xlrd==2.0.1 \
    openpyxl==3.0.9 \
    ipywidgets==7.7.0 \
    ipympl==0.8.8 \
    jupyterlab-spellchecker==0.8.3 \
    scipy==1.8.0 \
    lckr-jupyterlab-variableinspector==3.0.9 \
    jupyterlab-lsp==4.2.0 \
    'python-lsp-server[all]'==1.7.4 \
    ipycanvas==0.13.1\
    orjson==3.6.7\
    graphviz==0.20\
    termcolor==1.1.0

#   PGPLOT
# RUN pip3 install --no- \
#     traitlets==4.3.3 \
#     traittypes==0.2.1 \
#     bqplot==0.12.26
    


# modify the playsound and gtts package to work on jupyter
COPY playsound_extension.py .
COPY gtts_extension.py .
# check where to put the overrides file within a jupyterlab container: 
#       jupyter lab path
COPY overrides.json /opt/conda/share/jupyter/lab/settings/

# the following command returns the install location of the given pip package
#       `python3 -c "import playsound as _; print(_.__file__)"`
# `tee -a` appends the piped output of the `cat` command to the specified file
RUN cat playsound_extension.py | tee -a $(dirname "$(python3 -c "import playsound as _; print(_.__file__)")")/playsound.py
RUN cat gtts_extension.py | tee -a $(dirname "$(python3 -c "import gtts as _; print(_.__file__)")")/tts.py
