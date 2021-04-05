FROM python:3.8-slim

RUN pip install -U pip
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
RUN rm -rf /requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . /

WORKDIR /data-mass

ENTRYPOINT ["python", "populate.py"]
CMD ["--help"]
