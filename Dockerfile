FROM jupyter/base-notebook:latest

RUN sudo apt-get update -y && \
    sudo apt-get install -y s3fs

RUN pip3 install jupytext
RUN pip3 install numpy>=1.15.4
RUN pip3 install pandas>=1.0.4
RUN pip3 install matplotlib>=2.0.0
RUN pip3 install seaborn
RUN pip3 install pyBigWig
RUN pip3 install awscli

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