FROM jupyter/minimal-notebook:latest


LABEL maintainer="hfr"
LABEL version="0.1.2"
LABEL description="Jupyter Notebook image"

# all additional pip packages
RUN pip3 install --no-cache \
    jupyterhub==1.4.2 \
    smartphone-connector==0.0.115 \
    notebook==6.4.2 \
    playsound==1.2.2 \
    numpy==1.20.3 \
    gTTs==2.2.2 \
    jupyterlab-drawio==0.9.0 \
    Pillow==8.2.0 \
    XlsxWriter==1.4.3 \
    pandas==1.2.4 \
    xlrd==2.0.1 \
    openpyxl==3.0.7 \
    ipywidgets==7.6.3 \
    ipympl==0.7.0 \
    jupyterlab-spellchecker==0.7.0 \
    aquirdturtle_collapsible_headings==3.0.1 \
    scipy==1.6.3 \
    lckr-jupyterlab-variableinspector==3.0.9 \
    jupyterlab-lsp==3.8.1 \
    'python-lsp-server[all]'==1.2.1 \
    ipycanvas==0.9.0\
    orjson==3.6.0

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
