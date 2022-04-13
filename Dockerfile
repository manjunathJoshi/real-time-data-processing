FROM ubuntu:18.04
MAINTAINER "subham.kapoor@growthsourceft.com"
ENV DEBIAN_FRONTEND=noninteractive

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential \
        libxml2-dev \
        libldap2-dev \
        libxmlsec1-dev \
        libsasl2-dev \
        libffi-dev \
        libpq-dev \
        xorg \
        wget \
		vim\
		git

RUN apt-get install -y --no-install-recommends libssl-dev

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python 

RUN apt-get install -y --no-install-recommends postgresql postgresql-contrib
RUN apt-get install -y --no-install-recommends libcurl4-nss-dev libssl-dev
RUN pip3 install --upgrade setuptools


ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /rest/Butterfly/
RUN pip3 install --upgrade pip


COPY requirements.txt /rest/Butterfly


RUN pip3 install -r requirements.txt

COPY Butterfly /rest/Butterfly/

COPY webserver.sh /rest/Butterfly/webserver.sh
RUN chmod +x webserver.sh
