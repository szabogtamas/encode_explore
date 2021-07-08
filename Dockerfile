FROM szabogtamas/jupy_rocker

RUN sudo apt-get update -y
RUN sudo apt-get install -y libxt-dev
RUN sudo apt-get install -y libx11-dev
RUN sudo apt-get install -y libcairo2-dev
RUN sudo apt-get install -y libxml2-dev
RUN sudo apt-get install -y bedtools

RUN pip3 install numpy && \
    pip3 install pandas && \
    pip3 install matplotlib && \
    pip3 install seaborn && \
    pip3 install awscli && \
    pip3 install pyBigWig

RUN mkdir -p /usr/local/dev_scripts/encodex
ADD ./scripts/encodex /usr/local/dev_scripts/encodex

RUN install2.r --error \
    --deps TRUE \
    devtools \
    rlang \
    optparse \
    docstring \
    plotly \
    heatmaply \
    RColorBrewer \
    ggsci \
    pROC \
    openxlsx \
    readxl \
    googledrive \
    aws.s3

RUN R -e "devtools::install_github('kassambara/ggpubr')"
RUN R -e "BiocManager::install('ggbio')"
RUN R -e "BiocManager::install('RCAS')"

RUN chmod a+rwx -R /home/rstudio
ADD ./configs/rstudio-prefs.json /home/rstudio/.config/rstudio/rstudio-prefs.json