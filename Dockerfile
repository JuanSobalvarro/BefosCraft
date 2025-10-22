FROM python:3.11-slim

WORKDIR /server

RUN apt-get update && apt-get install -y openjdk-21-jdk curl

RUN pip install --no-cache-dir requests

EXPOSE 25565

CMD ["python", "/server/start-server.py"]
