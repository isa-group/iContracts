FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN python3 -m spacy download en_core_web_sm

COPY . .

CMD ["uwsgi", "app.ini"]
