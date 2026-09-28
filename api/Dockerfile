FROM python:3.12-alpine

RUN mkdir -p /app /blog-template /data
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt
