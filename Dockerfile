# from https://github.com/Kalimaha/simple_flask_dockerizer
FROM ubuntu:14.04
MAINTAINER Kim Duffy "kimhd@mit.edu"

RUN apt-get update

# Install Python.
RUN apt-get install -y -q build-essential python-gdal python-simplejson
RUN apt-get install -y python python-pip wget
RUN apt-get install -y python-dev

# Create a working directory.
RUN mkdir cert-provider

# Install VirtualEnv.
RUN pip install virtualenv

# Add requirements file.
ADD requirements.txt /cert-store/requirements.txt

# Add the script that will start everything.
ADD run.py /cert-store/run.py

# Run VirtualEnv.
RUN virtualenv /cert-store/env/
RUN /cert-store/env/bin/pip install wheel

RUN /cert-store/env/bin/pip install -r /cert-store/requirements.txt

COPY . /cert-store

RUN pip install /cert-store

ADD cert_data /etc/cert_data