FROM python:3.7.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /rpc_server
WORKDIR /forum
ADD .. /forum/
RUN pip install -r requirements.txt
