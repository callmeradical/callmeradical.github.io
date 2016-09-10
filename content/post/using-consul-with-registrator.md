+++
draft = true
title = "Using Consul with Registrator"
date = "2016-08-26T09:03:44-07:00"

+++

Service discovery is not new, but I still see plenty of shops storing their configuration in the form of configuration files or hardcoded objects. Connecting to an instance of MySQL or Redis and hard coding connection strings beforehand doesn't allow one to take full advantage of dynamic resources and also doesn't allow for treating them as backing resources.



We are going to take a quick walk through setting up a [consul](consul.io) cluster using docker-machine and have [registrator](http://gliderlabs.com/registrator/latest/) dynamically create entries in consul's service catalog. This post goes on the assumption that you have the docker toolkit installed/configured with VirtualBox and some working knowledge of docker in general.



The first thing we need to do is get some instances to play with.

```bash
$ docker-machine create --driver virtualbox dev1
$ docker-machine create --driver virtualbox dev2
$ docker-machine create --driver virtualbox dev3
```

Once our machines are up and running we can then connect the docker service by running:

```bash
$ docker-machine env <boxid>
```

You will see some output similar to this:

```bash
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.100:2376"
export DOCKER_CERT_PATH="/Users/demo/.docker/machine/machines/dev1"
export DOCKER_MACHINE_NAME="dev1"
# Run this command to configure your shell: 
# eval $(docker-machine env dev1)
```

Now we have our shell configured for the first host we are going to work on. The last piece of information we will need before we can begin launching our consul service is the IP addresses of the machines or nodes.

```bash
$ docker-machine ls
NAME   ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER    ERRORS
dev1   -        virtualbox   Running   tcp://192.168.99.100:2376           v1.12.1   
dev2   -        virtualbox   Running   tcp://192.168.99.101:2376           v1.12.1   
dev3   -        virtualbox   Running   tcp://192.168.99.102:2376           v1.12.1      
```

Now we can begin launching our consul service on each node.

```bash
$ docker run -d --net=host \
 -e 'CONSUL_LOCAL_CONFIG={"skip_leave_on_interrupt": true}' \
 --name=consul \
 consul agent -server \
 -bind=192.168.99.100 \
 -retry-join=192.168.99.101 \
 -bootstrap-expect=3 
```



For an explanation of the options when running the agent, I highly encourage you to look over the [consul documentation](https://www.consul.io/docs/agent/options.html). The team over at Hashicorp has done a really great job maintaining their docs. 

When supplying the retry-join option, you can enter the first IP-address of the node, or another node. Meaning, you can either have all nodes point to the first node, or have each one point to another node, either method seems to work fine. 

*Note: If this is not the case someone please comment on accepted best practice.*

Understanding consensus and Raft may not be necessary for this small walk-through, but if you are interested. I try to explain it here.



