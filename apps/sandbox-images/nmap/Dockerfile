FROM alpine:3.19
RUN apk add --no-cache nmap nmap-scripts
RUN adduser -D scanner
USER scanner
ENTRYPOINT ["nmap"]
