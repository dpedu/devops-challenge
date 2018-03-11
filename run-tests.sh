#!/bin/sh -ex

export PYTHONPATH=.

py.test test/ $@

