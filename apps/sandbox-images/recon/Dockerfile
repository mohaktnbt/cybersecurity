FROM golang:1.22-alpine AS builder
RUN go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install github.com/projectdiscovery/httpx/cmd/httpx@latest

FROM alpine:3.19
RUN apk add --no-cache ca-certificates
COPY --from=builder /go/bin/subfinder /usr/local/bin/
COPY --from=builder /go/bin/httpx /usr/local/bin/
RUN adduser -D scanner
USER scanner
