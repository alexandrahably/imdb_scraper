FROM python:3.9-slim

WORKDIR /app

# project source
COPY . /app

# dependencies
RUN pip install -r /app/requirements.txt

# run
CMD [ "python", "./test.py"]
