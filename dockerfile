FROM python:3

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY /food_app /app

COPY .env /app

CMD python3 app.py
