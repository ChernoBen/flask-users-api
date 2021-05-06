FROM python:alpine

WORKDIR /app

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt
#Define your env var here

COPY . /app

ENV FLASK_ENV=development

ENTRYPOINT ["python"]

CMD ["run.py"]