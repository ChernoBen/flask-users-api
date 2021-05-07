FROM python:3.7.0-stretch

RUN pip install zope.interface constantly incremental attrs Automat twisted pymodbus3 pendulum redis influxdb msgpack-python toml python-etcd falcon waitress greenlet gevent logbook

WORKDIR /app

RUN pip install --upgrade pip

COPY ./requirements.txt .

#RUN apk add --no-cache bash pkgconfig gcc && rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt
#Define your env var here

COPY . /app

ENV FLASK_ENV=development

ENTRYPOINT ["python"]

CMD ["run.py"]