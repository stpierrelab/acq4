FROM python:3.7

RUN apt-get update
RUN apt-get install -y python3-pyqt4 python3-pyqt4.qtopengl python3-pyqt4.qtsql python3-serial python3-scipy python3-pyparsing python3-h5py python3-pil python3-opengl python3-sip

RUN apt-get install -y python3-setuptools python3-pip

ENV PATH /bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
RUN mkdir /code
WORKDIR /code

#### Usage
# docker build -f tools/Dockerfile.py3 -t acq4:py3 .
# docker run -it --rm -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 -v $PWD:/code -v /tmp/.X11-unix:/tmp/.X11-unix --user="$(id --user):$(id --group)" acq4:py3 python3 -m acq4
