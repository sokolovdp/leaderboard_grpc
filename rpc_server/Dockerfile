FROM python:3.7.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /rpc_server
WORKDIR /rpc_server
ADD . /rpc_server
RUN pip install -r requirements.txt
