FROM python 

WORKDIR /app

COPY requirments.txt /app/

RUN apt-get update -y && apt-get install ffmpeg -y
RUN pip install -r requirments.txt

COPY .  /app/


CMD [ "python","consumer.py" ]

