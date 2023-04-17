FROM alpine:3.17

ENV REVIEWDOG_VERSION=v0.14.1

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

RUN wget -O - -q https://raw.githubusercontent.com/reviewdog/reviewdog/master/install.sh| sh -s -- -b /usr/local/bin/ ${REVIEWDOG_VERSION}

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY entrypoint.sh /entrypoint.sh
COPY convert.py /convert.py

ENTRYPOINT ["/entrypoint.sh"]
