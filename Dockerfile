FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app

RUN pip install -y && apt install awscli -y
RUN apt-get update && apt-get install -r requirements.txt
CMD ["python3", "app.py"]