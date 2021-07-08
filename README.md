# encode_explore

A Docker container for projects exploring ENCODE data. Setup based on instuctions at [ENCODE-DCC](https://github.com/ENCODE-DCC/encode-data-usage-examples/blob/master/mount_s3_bucket_and_run_jupyter_on_ec2.ipynb)

## Usage

Recommended way is to run in a Docker container calling the below command (root user is needed if we want to save modifications):  
`docker run --rm -p 127.0.0.1:8888:8888 -v $PWD/notebook:/home/encodex -e NB_UID=$UID --user root szabogtamas/encodex`  

A simple case study is shown in [a notebook](notebooks/jupyter/encodex_example.ipynb) with RBFOX2, an RNA binding protein commonly used in tutorials and let-7d, an extensively studied miRNA.

## Dependencies

Files are downloaded from S3 using awscli.  
BigWig files are parsed with the help of [pyBigWig](https://github.com/deeptools/pyBigWig).  
Additionally, some common data analysis packages, such as NumPy, Pandas and Seaborn are also required.