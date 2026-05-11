FROM python:3.7

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y locales vim \
    && mkdir /src \
    && mkdir /src/STP00-dev \
    && rm -rf /var/lib/apt/lists/* \
    && echo "ja_JP UTF-8" > /etc/locale.gen \
    && locale-gen

ENV PYTHONUNBUFFERED 1

COPY --chown=root:root ./STP00-dev /src/STP00-dev

WORKDIR /src/STP00-dev

RUN pip install -r requirements/local.txt

CMD ["python"]
