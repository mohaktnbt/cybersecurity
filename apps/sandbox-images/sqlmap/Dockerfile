FROM python:3.12-alpine
RUN pip install --no-cache-dir sqlmap
RUN adduser -D scanner
USER scanner
ENTRYPOINT ["sqlmap"]
