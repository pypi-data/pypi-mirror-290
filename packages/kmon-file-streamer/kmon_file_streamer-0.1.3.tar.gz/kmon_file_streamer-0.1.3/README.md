# README #

A Python package that read file from AWS S3 bucket and stream data back to the caller immediately 

## Table of Contents

## Installation

You can install the package using pip:

```bash
  pip install kmon-file-streamer
```


## Usage
```
from kmon.kmsf_stream import kmsf_data_stream

for json in kmsf_data_stream("bucket-name",
                             "tar file_name",
                             {"clazz": "RC-textile_fabricProductionStatus"}):
    #DO YOUR STUFF
```

```
from kmon.utility import find_latest_file

file_name = find_latest_file("bucket-name", 'object_prefix')
```
