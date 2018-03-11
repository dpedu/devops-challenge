#!/bin/sh -ex

export PYTHONPATH=.
export AWS_DEFAULT_REGION="us-east-1"

py.test test/ $@

