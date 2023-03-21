FROM python

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080
CMD [ "python3","server.py" ]