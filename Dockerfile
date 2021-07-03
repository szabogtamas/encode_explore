ARG NB_USER="encodex"
FROM jupyter/base-notebook:latest

RUN pip3 install awscli
RUN conda install --quiet --yes \
    jupytext numpy pandas matplotlib seaborn && \
    conda clean --all -f -y 
RUN conda install --quiet --yes \
    pybigwig -c bioconda && \
    conda clean --all -f -y

USER $NB_UID
ENV NB_USER=encodex \
  CHOWN_HOME=yes \
  JUPYTER_ENABLE_LAB=yes 