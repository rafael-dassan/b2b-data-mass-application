FROM python:3.6-alpine

RUN pip install -U pip
COPY data-mass/requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
RUN rm -rf /requirements.txt

COPY . /

WORKDIR /data-mass

ENTRYPOINT ["python", "populate.py"]
CMD ["--help"]
