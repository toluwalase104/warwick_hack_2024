FROM python:3.9
RUN pip install virtualenv
WORKDIR /app
COPY . .
RUN virtualenv venv
CMD gunicorn app:app -b 0.0.0.0:8080