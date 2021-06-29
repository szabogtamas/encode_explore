# encode_explore

A Docker container for projects exploring ENCODE data. Setup based on instuctions at [ENCODE-DCC](https://github.com/ENCODE-DCC/encode-data-usage-examples/blob/master/mount_s3_bucket_and_run_jupyter_on_ec2.ipynb)

## Usage

Run container calling the below command:
`docker run --rm -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v "${PWD}":/home/encodex/work encodex`
