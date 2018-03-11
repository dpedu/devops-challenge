FROM library/python:3.6-slim

ADD . /tmp/code/

RUN cd /tmp/code && \
    python3 setup.py install

USER nobody

ENTRYPOINT ["doctorappd"]
