# encode_explore

A Docker container for projects exploring ENCODE data. Setup based on instuctions at [ENCODE-DCC](https://github.com/ENCODE-DCC/encode-data-usage-examples/blob/master/mount_s3_bucket_and_run_jupyter_on_ec2.ipynb)

## Usage

Run container calling the below command (need root user if we want to save modifications, privlileged flag needed by s3fuse):
`docker run --rm -p 127.0.0.1:8888:8888 -v $PWD/notebook:/home/encodex -e NB_UID=$UID --user root --privileged encodex`
