FROM python:3.9-slim

WORKDIR /app

# project source
COPY . /app

# dependencies
RUN pip3 install -r /app/requirements.txt

# run
CMD [ "python3", "-m", "src.app"]
