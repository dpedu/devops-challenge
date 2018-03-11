# INSTRUCTIONS

How to build/test/deploy it


## Overview

This repository is structured as both a Python module and a Docker Image.


## Requirements

- Python 3.6 recommended
  - Known to work on 3.4+
- Pip + setuptools


## Basic installation

Install the application using Pip:

```
git clone https://github.com/dpedu/devops-challenge.git
cd devops-challenge
pip3 install .
```

## Configuration

Several environment vars containing AWS credentials must be set:

- `AWS_ACCESS_KEY_ID=<aws access key>`
- `AWS_SECRET_ACCESS_KEY=<aws key secret>`
- `AWS_DEFAULT_REGION=us-west-2`

Optionally, some additional environment vars may be set to alter the behavior of the app. By default, the app accesses a
specific DynamoDB table, looks for a value in a column, and returns another column from that row. The defaults shown
below can be overridden to alter behavior:

- `SECRET_DBNAME=devops-challenge`
- `LOOKUP_KEYNAME=code_name`
- `LOOKUP_KEYVALUE=thedoctor`
- `SECRET_KEYNAME=secret_code`


## Starting the App

Run the app:

- `doctorappd`

By default, it will listen over HTTP on 0.0.0.0:5000. This bind and port can be changed with flags:

```
$ doctorappd --help
usage: doctorappd [-h] [-l LISTEN] [-p PORT] [--debug]

doctorapp http server daemon

optional arguments:
  -h, --help            show this help message and exit
  -l LISTEN, --listen LISTEN
                        listen address
  -p PORT, --port PORT  tcp port to listen on
  --debug               enable development options
```

These flags may also by defined using env vars:

- `DOCTORAPP_LISTEN=0.0.0.0`
- `DOCTORAPP_PORT=5000`
- `DOCTORAPP_DEBUG=1`


## Docker

This repository also contains a Dockerfile and docker-compose.yml config. First install Docker and docker-compose; next
build the image by executing:

- `docker build -t doctorapp .`

And launch the image:

```
docker run -d -p 5000:5000 \
    -e "AWS_ACCESS_KEY_ID=<aws access key>" \
    -e "AWS_SECRET_ACCESS_KEY=<aws key secret>" \
    -e "AWS_DEFAULT_REGION=us-west-2"
```

However, it's easier and more secure to launch through docker-compose as this will not leave credential's in your
shell's history file.

In the root of the repository, copy `.env.example` to `.env` and modify it. It contains the environment vars mentioned
above that must be set for the app to function. After editing the `.env` file, run docker-compose:

- `docker-compose up`

Note: the port the docker-compose stack listens on may be changed by setting `DOCTORAPP_PORT=<port number>` before
running docker-compose.


## Testing

This repository uses [py.test](https://pytest.org/)! In order to run the test suite, first install some additional
python modules required for testing:

- `pip3 install -r requirements-test.txt`

Then, execute the test suite:

- `./run-tests.sh`

After a few seconds, you should have passing result :-)
