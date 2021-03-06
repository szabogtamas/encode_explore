FROM szabogtamas/jupy_rocker

RUN sudo apt-get update -y && \
    sudo apt-get install -y libxt-dev && \
    sudo apt-get install -y libx11-dev && \
    sudo apt-get install -y libcairo2-dev && \
    sudo apt-get install -y libxml2-dev && \
    sudo apt-get install -y libbz2-dev && \
    sudo apt-get install -y liblzma-dev && \
    sudo apt-get install -y bedtools

RUN pip3 install numpy && \
    pip3 install pandas && \
    pip3 install matplotlib && \
    pip3 install seaborn && \
    pip3 install awscli && \
    pip3 install pyBigWig

ENV PATH=/usr/local/bin:$PATH

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
    ggridges \
    pROC \
    openxlsx \
    readxl \
    googledrive \
    aws.s3

RUN R -e "devtools::install_github('kassambara/ggpubr')"
RUN R -e "BiocManager::install('ggbio')"
RUN R -e "BiocManager::install('wiggleplotr')"
RUN R -e "BiocManager::install('RCAS')"
RUN R -e "BiocManager::install('Rsubread')"
RUN R -e "BiocManager::install('Gviz')"
RUN R -e "BiocManager::install('plyranges')"
RUN R -e "BiocManager::install('EnsDb.Hsapiens.v86')"
RUN R -e "BiocManager::install('EnsDb.Mmusculus.v79')"
RUN R -e "BiocManager::install('clusterProfiler')"

RUN chmod a+rwx -R /home/rstudio

ADD ./scripts /usr/local/dev_scripts
ADD ./notebooks /usr/local/notebooks
ADD ./configs/rstudio-prefs.json /home/rstudio/.config/rstudio/rstudio-prefs.json