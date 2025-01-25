FROM python:3.11.0-slim-buster
WORKDIR /app
copy . /app
RUN apt-get update -y && apt-get install awscli -y
RUN pip install -r requirements.txt
CMD ["python", "app.py"]