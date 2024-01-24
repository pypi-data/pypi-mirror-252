# PWBM_Cloud_Utils

## Introduction
This Python module provides a convenient interface for handling input/output configurations, reading from different sources (local or cloud), and writing data to cloud storage (Amazon S3) or locally. It is designed to be flexible, supporting various data formats and compression options.

## Installation
To use this module, ensure that you have the required dependencies installed. You can install them using the following command:
```bash
pip install PWBM_Cloud_Utils
```
# Setting
## Environment Setup

To configure the environment, create an instance of `IO_Config` by providing the path to your environment file (`.env`), which should contain the necessary configuration variables. If no environment file is provided, default values will be used.

```bash
from dotenv import load_dotenv
from io_util import IO_Config

# Load environment variables from .env file
load_dotenv(".env")

# Create config
config = IO_Config(".env")
```


# Usage
## Reading Data
The IO_Reader class allows you to read data from either cloud storage (Amazon S3) or a local file, depending on the configuration.

```bash
from io_util import IO_Reader

## Create reader instance
reader = IO_Reader(config)

## Read data as bytes
data_bytes = reader.read("bucket_name", "path/to/file", compress=True)

## Read data as a string
data_string = reader.read_string("bucket_name", "path/to/text_file", compress=False)
```

## Writing Data

The IO_Writer class enables you to write data to cloud storage (Amazon S3) or a local file.

```bash
from io_util import IO_Writer

## Create writer instance

writer = IO_Writer(config)

## Write data to cloud storage
success = writer.write("bucket_name", "path/to/output/file", "data_to_write", compress=True, cache=False)

# Check if an object exists in cloud storage
exists = writer.object_exists("path/to/file", "recipe")
```

# Notes
Ensure that your environment file (.env) contains the necessary variables, such as Region_Name, AWS_ACCESS_KEY_ID, and AWS_ACCESS_KEY_SECRET.
Compression options (compress) are available for both reading and writing, allowing you to handle compressed data.
The module uses the boto3 library for Amazon S3 interactions.
