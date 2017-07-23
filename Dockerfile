FROM python:3.5

RUN pip install nltk sanic
ADD app /app
WORKDIR /app
CMD ["python", "server.py"]
