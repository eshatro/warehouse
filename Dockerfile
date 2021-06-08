FROM python:3.9-slim-buster

COPY requirements.txt /tmp/requirements.txt

RUN python -m venv /opt/virtualenv \
  && . /opt/virtualenv/bin/activate \
  && pip install -r /tmp/requirements.txt

ENV PYTHONUNBUFFERED=on
ENV PATH="/opt/virtualenv/bin:$PATH"

COPY . /opt/warehouse

WORKDIR /opt/warehouse

RUN pip install .

CMD ["bash"]
