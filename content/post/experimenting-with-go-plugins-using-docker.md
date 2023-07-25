+++
title = "Experimenting With Go Plugins Using Docker"
date = 2017-10-13T11:32:07-04:00
draft = false
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Go Plugin", "Linux", "Docker", "Build Process", "Make", "Toolchain", "Cross-Platform Development"]
categories = ["Go Programming", "Docker", "Software Development"]
series = []
comment = true
+++

I was learning about the plugin package from a number of sources and decided to 
follow along with this article - 
[Writing Modular Go Programs with Plugins](https://medium.com/learning-the-go-programming-language/writing-modular-go-programs-with-plugins-ec46381ee1a9)

One of the things that immediately hit me was that there is a caveat to using Go plugin.

> As of version 1.8, the Go plugin only works on Linux.

Well I am not one to be deterred by something like "only works on Linux."
So I went through and created a small project to show how you might be able to continue
doing Go plugin development on any system that can run Docker.

The way we do this is by first creating a base Dockerfile that we can use for various 
stages of development.

```Dockerfile
FROM golang:1.9.1-alpine

RUN apk add --update git build-base

RUN mkdir /source
RUN mkdir -p /go/src/github.com/callmeradical
```

Next we abstract our operations in the build process via Make. Now I can't take credit for this.
At 2ndWatch, [Craig Monson](https://github.com/craigmonson) came up with the idea to use Make to 
abstract the sprawl of our tools. We use a number of specialized tools for various things.
Sometimes it can be daunting to a new developer that is coming to a new project. We shouldn't
have to spend time just to learn the toolchain. So in an effort to decrease the barrier of 
entry we have used Make in this way. It has been incredibly convenient for us and yielded some
excellent results. This is just an extension of that idea.

```make
PROJECT=$(shell basename $$PWD)
PROJECT_DIR=$(shell if [[ $$PWD =~ \/go\/src  ]]; then echo $$PWD | sed 's/.*\(\/go\/.*\)/\1/g'; else echo '/go/src/github.com/callmeradical/$(PROJECT)'; fi)
.PHONY: build_docker_image plugins
plugins:
	docker run -tP \
		-v $(PWD):$(PROJECT_DIR) \
		-w $(PROJECT_DIR) \
		plugin_builder:latest /bin/sh -c        \
		"go build -buildmode=plugin -o eng/eng.so eng/greeter.go && \
		go build -buildmode=plugin -o chi/chi.so chi/greeter.go"

.PHONY: build_docker_image
build_docker_image:
	docker build -t plugin_builder:latest .

.PHONY: greeter
greeter:
	docker run -tP \
		-v $(PWD):$(PROJECT_DIR) \
		-w $(PROJECT_DIR) \
		plugin_builder:latest /bin/sh -c "go run main.go english"
	docker run -tP \
		-v $(PWD):$(PROJECT_DIR) \
		-w $(PROJECT_DIR) \
		plugin_builder:latest /bin/sh -c "go run main.go chinese"
```

Now once this is in place we can simply run:
```bash
$ make build_docker_image
$ make build_plugins
$ make greeter
```

By abstracting out the build process and where the commands actually run, we can now 
safely develop Go plugins on not only linux, but also Windows and Mac OS X. Also note 
that using make self documents common commands we use from our disparate tools, and 
provides working examples of those commands.

