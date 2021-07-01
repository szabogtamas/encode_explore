ARG NB_USER="encodex"
FROM jupyter/base-notebook:latest

USER root

RUN apt-get update -y && \
    apt-get install -y s3fs

USER 1000

RUN pip3 install awscli
RUN conda install jupytext numpy pandas matplotlib seaborn
RUN conda install pybigwig -c bioconda

# Empty credentials file, needed to access public datasets of ENCODE
RUN mkdir -p ~/.aws
RUN echo '[default] \
  \naws_access_key_id= \
  \naws_secret_access_key=' \
  > ~/.aws/credentials
RUN echo '[default] \
  \nregion=eu-central-1 \
  \noutput=json' \
  > ~/.aws/config

RUN chmod a+rwx -R /home/jovyan/work