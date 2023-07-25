+++
title = "Notes: Multi Stage Docker Build"
date = 2018-06-15T14:51:50-05:00
draft = false 
description = ""
subtitle = ""
header_img = ""
toc = true
categories = ["Technology", "Programming", "DevOps", "Web Development", "Cloud Computing"]
tags = ["Docker", "Miscellaneous", "docker", "Programming & Software Development", "GoLang", "Operating Systems & Environment Management", "Networking & Security"]
series = []
comment = true
+++

# Docker Multi-Stage Builds

Multi-stage builds are a new feature requiring Docker 17.05 or higher on the **daemon and client**. Multi-stage builds are useful to anyone who has struggled to optimize Dockerfiles while keeping them easy to read and maintain.

```
Things to remember:
- Dockerfile adds a layer to the image for each instruction
```

Multi-stage builds are helpful to reduce image-size, maintain readability, and reduces the need to have two Dockerfiles (one for dev and one for production, aka the builder pattern).

### Builder Pattern

[Example: Builder pattern on Docker.com](https://docs.docker.com/develop/develop-images/multistage-build/#before-multi-stage-builds):

This is the standard pattern that is followed with many development shops. Create a container to provide build-tools and support to the developer. A new container to deploy the artifact from the build.

`Dockerfile.build:`

```dockerfile
FROM golang:1.7.3
WORKDIR /go/src/github.com/alexellis/href-counter/
COPY app.go .
RUN go get -d -v golang.org/x/net/html \
  && CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .
```

`Dockerfile:`

```dockerfile
FROM alpine:latest  
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY app .
CMD ["./app"]  
```

`build.sh:`

```sh
#!/bin/sh
echo Building alexellis2/href-counter:build

docker build --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy \  
    -t alexellis2/href-counter:build . -f Dockerfile.build

docker container create --name extract alexellis2/href-counter:build  
docker container cp extract:/go/src/github.com/alexellis/href-counter/app ./app  
docker container rm -f extract

echo Building alexellis2/href-counter:latest

docker build --no-cache -t alexellis2/href-counter:latest .
rm ./app
```

### Multi-stage Build

`Dockerfile:`

```dockerfile
FROM golang:1.7.3
WORKDIR /go/src/github.com/alexellis/href-counter/
RUN go get -d -v golang.org/x/net/html  
COPY app.go .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

FROM alpine:latest  
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=0 /go/src/github.com/alexellis/href-counter/app .
CMD ["./app"]  
```

`Using build tags:`

```dockerfile
FROM golang:1.7.3 as builder
WORKDIR /go/src/github.com/alexellis/href-counter/
RUN go get -d -v golang.org/x/net/html  
COPY app.go    .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

FROM alpine:latest  
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /go/src/github.com/alexellis/href-counter/app .
CMD ["./app"] 
```

`Building a specific stage/target:`

```sh
$ docker build --target builder -t alexellis2/href-counter:latest .

```

In a Dockerfile you can also use an external image as a stage. The Docker client pulls the image if necessary and copies the artifact from there.

`Example:`

```sh
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf

```
