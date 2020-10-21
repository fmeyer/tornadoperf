FROM golang:alpine AS build-env
COPY . $GOPATH/src/fmeyer/upstream_server/
WORKDIR $GOPATH/src/fmeyer/upstream_server/
RUN go get -d -v
RUN go build -o /go/bin/upstream_server
ENTRYPOINT ["/go/bin/upstream_server"]
EXPOSE 8080

