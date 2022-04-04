FROM ubuntu:18.04
RUN apt-get update && apt-get install -y \
        software-properties-common
    RUN add-apt-repository ppa:deadsnakes/ppa
    RUN apt-get update && apt-get install -y \
        python3.7 \
        python3-pip
    RUN python3.7 -m pip install pip
    RUN apt-get update && apt-get install -y \
        python3-distutils \
        python3-setuptools
    RUN python3.7 -m pip install pip --upgrade pip
ADD . /application
WORKDIR /application/application
RUN pip install -r requirements.txt
WORKDIR /application/application/app
EXPOSE 5000
CMD ["python3", "app.py"]
