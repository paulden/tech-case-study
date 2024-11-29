FROM python:3.13-alpine

RUN addgroup -g 1001 -S url_extractor && \
    adduser -u 1001 -S url_extractor -G url_extractor

COPY --chown=url_extractor:url_extractor src/url_extractor /opt/url_extractor
COPY --chown=url_extractor:url_extractor requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

USER 1001

ENTRYPOINT [ "/usr/local/bin/python", "/opt/url_extractor/cli.py" ]