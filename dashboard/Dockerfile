# syntax=docker/dockerfile:1

# Base image
FROM python:3.9-slim-bullseye

# switch working directory
WORKDIR /app

# copy the requirements file into the image
COPY requirements.txt requirements.txt

# install the dependencies and packages in the requirements file
RUN pip3 install -r requirements.txt

COPY app.py app.py

EXPOSE 5102
EXPOSE 6379

CMD [ "python", "app.py"]