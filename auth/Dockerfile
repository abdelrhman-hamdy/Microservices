FROM python:3.10-slim-bullseye

USER root
RUN apt-get update -y && apt-get install -y build-essential default-libmysqlclient-dev && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirments.txt ./

RUN pip install --no-cache-dir -r requirments.txt 

COPY server.py ./

EXPOSE 5000

CMD ["python3","server.py"]

