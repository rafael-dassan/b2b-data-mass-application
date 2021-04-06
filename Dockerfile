FROM python:3.7-buster

LABEL maintainer="Data Mass Team"

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./data_mass /app/data_mass

WORKDIR /app/

ENTRYPOINT ["python", "-m", "data_mass.populate"]
CMD ["--help"]
