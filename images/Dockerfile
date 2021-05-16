FROM jupyter/minimal-notebook:latest


LABEL maintainer="hfr"
LABEL version="0.1"
LABEL description="Jupyter Notebook image with debugging support"

# all additional pip packages
RUN pip3 install --no-cache \
    jupyterhub==1.4.1 \
    smartphone-connector==0.0.115 \
    notebook==6.3.0 \
    playsound==1.2.2 \
    numpy==1.20.3 \
    gTTs==2.2.2 \
    jupyterlab-drawio==0.9.0 \
    jupyterlab-topbar==0.6.1 \
    jupyterlab-system-monitor==0.8.0 \
    Pillow==8.2.0 \
    XlsxWriter==1.4.3
    


# modify the playsound and gtts package to work on jupyter
COPY playsound_extension.py .
COPY gtts_extension.py .

# the following command returns the install location of the given pip package
#       `python3 -c "import playsound as _; print(_.__file__)"`
# `tee -a` appends the piped output of the `cat` command to the specified file
RUN cat playsound_extension.py | tee -a $(dirname "$(python3 -c "import playsound as _; print(_.__file__)")")/playsound.py
RUN cat gtts_extension.py | tee -a $(dirname "$(python3 -c "import gtts as _; print(_.__file__)")")/tts.py
