FROM nginx/unit:1.29.1-python3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements ./requirements

RUN apt update \
  && cp /usr/bin/python3 /usr/bin/python \
  && python -m pip install --upgrade pip \
  && pip3 install -r requirements/base.in \
  && apt autoremove --purge -y \
  && rm -rf \
    /var/lib/apt/lists/* \
    /etc/apt/sources.list.d/*.list \
    /root/.cache/

COPY schema_viewer ./schema_viewer
COPY tests ./tests
COPY manage.py ./

COPY docker/unit_config.json /docker-entrypoint.d/unit_config.json
