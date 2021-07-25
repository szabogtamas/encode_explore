# encode_explore

A Docker container for projects exploring ENCODE data. Setup based on instuctions at [ENCODE-DCC](https://github.com/ENCODE-DCC/encode-data-usage-examples/blob/master/mount_s3_bucket_and_run_jupyter_on_ec2.ipynb)

## Usage

Recommended way is to run in a Docker container calling the below command (root user is needed if we want to save modifications):  
`docker run --rm -p 127.0.0.1:8888:8888 -v $PWD:/home/rstudio/local_files -e USERID=$UID -e PASSWORD=[YOUR_PASSWORD] szabogtamas/encodex`  

A simple case study is shown in [a notebook](notebooks/jupyter/encodex_example.ipynb) with RBFOX2, an RNA binding protein commonly used in tutorials and let-7d, an extensively studied miRNA.

To help exploring peak reagions, RCAS is also integrated. It is available via R, most conveniently in an RStudio session:
`docker run --rm -p 127.0.0.1:8787:8787 -v $PWD:/home/rstudio/local_files -e USERID=$UID -e PASSWORD=[YOUR_PASSWORD] szabogtamas/encodex`  
u can check out the [R version of the explorative notebook](notebooks/R/encode_s3db_basic_explorative_template.Rmd), for example.

## Dependencies

Files are downloaded from S3 using awscli.  
BigWig files are parsed with the help of [pyBigWig](https://github.com/deeptools/pyBigWig).  
Additionally, some common data analysis packages, such as NumPy, Pandas and Seaborn are also required.