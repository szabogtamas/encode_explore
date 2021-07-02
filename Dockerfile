ARG NB_USER="encodex"
FROM jupyter/base-notebook:latest

USER root

RUN apt-get update -y && \
    apt-get install -y s3fs

RUN pip3 install awscli
RUN conda install --quiet --yes \
    jupytext numpy pandas matplotlib seaborn && \
    conda clean --all -f -y 
RUN conda install --quiet --yes \
    pybigwig -c bioconda && \
    conda clean --all -f -y

# Empty credentials file, needed to access public datasets of ENCODE
RUN mkdir -p /home/encodex/.aws
RUN echo '[default] \
  \naws_access_key_id= \
  \naws_secret_access_key=' \
  > /home/encodex/.aws/credentials
RUN echo '[default] \
  \nregion=eu-central-1 \
  \noutput=json' \
  > /home/encodex/.aws/config

USER $NB_UID
ENV NB_USER=encodex \
  CHOWN_HOME=yes \
  JUPYTER_ENABLE_LAB=yes 