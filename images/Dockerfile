FROM jupyter/minimal-notebook:lab-4.0.7

LABEL maintainer="hfr"
LABEL version="0.1.7"
LABEL description="Jupyter Notebook image"

USER root
# graphviz and graphviz-dev is needed for use with jupyterlab
RUN apt-get update -y && apt-get install -y graphviz graphviz-dev
USER jovyan

# all additional pip packages
RUN pip3 install --no-cache \
    jupyterhub==4.0.2 \
    jupyterlab==4.1.1 \
    smartphone-connector==0.0.115 \
    notebook==7.1.0rc1 \
    playsound==1.2.2 \
    numpy==1.26.4 \
    gTTs==2.2.2 \
    Pillow==10.2.0 \
    XlsxWriter==3.1.2 \
    pandas==2.2.0 \
    xlrd==2.0.1 \
    openpyxl==3.1.2 \
    ipywidgets==8.1.2 \
    ipympl==0.9.3 \
    jupyterlab-spellchecker==0.8.4 \
    scipy==1.12.0 \
    # lckr-jupyterlab-variableinspector==3.0.9 \
    # jupyterlab-lsp==4.2.0 \
    'python-lsp-server[all]'==1.10.0 \
    ipycanvas==0.13.1\
    orjson==3.9.13\
    graphviz==0.20\
    termcolor==2.4.0

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
