FROM python:2-onbuild
COPY scr/ /usr/src/app
COPY rsa/ /usr/local/lib/python2.7/dist-packages