+++
draft = false
title = "Using Consul with Registrator"
date = "2016-09-10T15:03:44-07:00"
featuredimg = "https://www.consul.io/assets/images/logo_large-475cebb0.png"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Docker", "Miscellaneous", "DevOps", "docker", "Software Development"]

categories = ["DevOps", "Cloud Computing", "Containerization", "Distributed Systems", "Network Architecture"]
series = []
comment = true

+++

Service discovery is not new, but I still see plenty of shops storing their configuration in the form of configuration files or hardcoded objects. Connecting to an instance of MySQL or Redis and hard coding connection strings beforehand doesn't allow one to take full advantage of dynamic resources and also doesn't allow for treating them as backing resources.



We are going to take a quick walk through setting up a [consul](consul.io) cluster using docker-machine and have [registrator](http://gliderlabs.com/registrator/latest/) dynamically create entries in consul's service catalog. This post goes on the assumption that you have the Docker toolkit installed/configured with VirtualBox and some working knowledge of docker in general.



The first thing we need to do is get some instances to play with.

```bash
$ docker-machine create --driver virtualbox dev1
$ docker-machine create --driver virtualbox dev2
$ docker-machine create --driver virtualbox dev3
```

Once our machines are up and running we can then connect the Docker service by running:

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

Understanding consensus and Raft may not be necessary for this small walk-through, but if you are interested. I will do my best to explain it in another post, meanwhile, this is a great visualization and explanation of Raft consensus.

[The Secret Lives of Data - Raft](http://thesecretlivesofdata.com/raft/)

Once you have launched Consul on each node, let's check the logs from the first consul container we launched. We should see our leader elected.

```bash
$ eval $(docker-machine env dev1)
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
f594e58e3cad        consul              "docker-entrypoint.sh"   4 minutes ago       Up 4 minutes                            backstabbing_brown
$ docker logs --tail 20 f594
    2016/09/10 19:03:38 [ERR] agent: coordinate update error: No cluster leader
    2016/09/10 19:03:52 [ERR] agent: failed to sync remote state: No cluster leader
    2016/09/10 19:04:02 [ERR] agent: coordinate update error: No cluster leader
    2016/09/10 19:04:17 [ERR] agent: failed to sync remote state: No cluster leader
    2016/09/10 19:04:29 [ERR] agent: coordinate update error: No cluster leader
    2016/09/10 19:04:30 [INFO] serf: EventMemberJoin: dev3 192.168.99.102
    2016/09/10 19:04:30 [INFO] consul: adding LAN server dev3 (Addr: 192.168.99.102:8300) (DC: dc1)
    2016/09/10 19:04:30 [INFO] consul: Attempting bootstrap with nodes: [192.168.99.100:8300 192.168.99.101:8300 192.168.99.102:8300]
    2016/09/10 19:04:31 [WARN] raft: Heartbeat timeout reached, starting election
    2016/09/10 19:04:31 [INFO] raft: Node at 192.168.99.100:8300 [Candidate] entering Candidate state
    2016/09/10 19:04:31 [INFO] raft: Election won. Tally: 2
    2016/09/10 19:04:31 [INFO] raft: Node at 192.168.99.100:8300 [Leader] entering Leader state
    2016/09/10 19:04:31 [INFO] consul: cluster leadership acquired
    2016/09/10 19:04:31 [INFO] consul: New leader elected: dev1
    2016/09/10 19:04:31 [INFO] raft: pipelining replication to peer 192.168.99.102:8300
    2016/09/10 19:04:31 [INFO] raft: pipelining replication to peer 192.168.99.101:8300
    2016/09/10 19:04:31 [INFO] consul: member 'dev1' joined, marking health alive
    2016/09/10 19:04:31 [INFO] consul: member 'dev2' joined, marking health alive
    2016/09/10 19:04:31 [INFO] consul: member 'dev3' joined, marking health alive
    2016/09/10 19:04:32 [INFO] agent: Synced service 'consul'
```



 Let's test our consul installation first by logging into a node and attempting to query the API for some information.



```bash
$ docker-machine ssh dev1
                        ##         .
                  ## ## ##        ==
               ## ## ## ## ##    ===
           /"""""""""\___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
           \______ o           __/
             \    \         __/
              \____\_______/
 _                 _   ____     _            _
| |__   ___   ___ | |_|___ \ __| | ___   ___| | _____ _ __
| '_ \ / _ \ / _ \| __| __) / _` |/ _ \ / __| |/ / _ \ '__|
| |_) | (_) | (_) | |_ / __/ (_| | (_) | (__|   <  __/ |
|_.__/ \___/ \___/ \__|_____\__,_|\___/ \___|_|\_\___|_|
Boot2Docker version 1.12.1, build HEAD : ef7d0b4 - Thu Aug 18 21:18:06 UTC 2016
Docker version 1.12.1, build 23cf638
$ curl localhost:8500/v1/catalog/nodes
```



After the curl you should be greeted with some output similar to this:



```JSON
[{"Node":"dev1","Address":"192.168.99.100","TaggedAddresses":{"wan":"192.168.99.100"},"CreateIndex":3,"ModifyIndex":6},{"Node":"dev2","Address":"192.168.99.101","TaggedAddresses":{"wan":"192.168.99.101"},"CreateIndex":4,"ModifyIndex":7},{"Node":"dev3","Address":"192.168.99.102","TaggedAddresses":{"wan":"192.168.99.102"},"CreateIndex":5,"ModifyIndex":8}]
```



We can go ahead and proceed to launch Registrator on each node now.

```bash
$ eval $(docker-machine env dev1)
$ docker run -d --name=registrator --net=host --volume=/var/run/docker.sock:/tmp/docker.sock gliderlabs/registrator consul://localhost:8500
```

And repeat for all three nodes. Registrator automatically registers and deregisters services for any Docker container by inspecting containers as they come online. Notice we are mounting the Docker socket in our Registrator container, this is how we are able to see transactions going through docker.



Now that Registrator and Consul are running on all nodes, let's launch a new service...

How about Redis?



```bash
$ eval $(docker-machine env dev2)
$ docker run -d -p 6379:6379 --name redis redis
$ docker-machine ssh dev3
$ curl localhost:8500/v1/catalog/services
{"consul":[],"redis":[]}
$ curl localhost:8500/v1/catalog/service/redis
[{"Node":"dev2","Address":"192.168.99.101","ServiceID":"dev2:redis:6379","ServiceName":"redis","ServiceTags":[],"ServiceAddress":","ServicePort":6379,"ServiceEnableTagOverride":false,"CreateIndex":93,"ModifyIndex":93}]
```



Great! Now we know information about where Redis is running and the ports that it is listening on. The documentation on Registrator is well maintained and is invaluable when working with this setup. Even though I was able to stand up a Redis instance and retrieve the service information, I still need to supply health checks and other information.



Say we were standing up Nginx. We want to declare a health check at the time the container is launched. We can tell Registrator about our service at the time of launch using environment variables. Like so:



```bash
$ docker run -d --net=host -e SERVICE_CHECK_SCRIPT="curl --silent --fail localhost" -e SERVICE_TAGS="urlprefix-/nginx" -p 8081:80 -p 44300:443 nginx:1.10
```

If we check our consul entries we can see that there is a health now for Nginx

```bash
$ curl localhost:8500/v1/health/service/nginx-80
[{"Node":{"Node":"dev3","Address":"192.168.99.102","TaggedAddresses":{"wan":"192.168.99.102"},"CreateIndex":5,"ModifyIndex":145},"Service":{"ID":"dev3:nginx:80","Service":"nginx-80","Tags":["urlprefix-/nginx"],"Address":","Port":8081,"EnableTagOverride":false,"CreateIndex":145,"ModifyIndex":145},"Checks":[{"Node":"dev3","CheckID":"serfHealth","Name":"Serf Health Status","Status":"passing","Notes":","Output":"Agent alive and reachable","ServiceID":","ServiceName":","CreateIndex":5,"ModifyIndex":5},{"Node":"dev3","CheckID":"service:dev3:nginx:80","Name":"Service 'nginx-80' check","Status":"critical","Notes":","Output":","ServiceID":"dev3:nginx:80","ServiceName":"nginx-80","CreateIndex":145,"ModifyIndex":145}]}]
```



It really can be that easy. There is a lot happening under the hood, but at its core, service discovery really can be that easy. Now when configuring my app, I can make some calls to a Rest API about service data I need for inside my application. I will try to follow up with another post on using [Fabio](https://github.com/eBay/fabio) for load-balancing in this set-up.
