+++
date = "2015-09-30T02:39:08-04:00"
draft = false
title =  "Tetris... err... Getting Started with Kubernetes"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Kubernetes", "AWS", "Miscellaneous", "DevOps", "Golang"]
categories = ["Cloud Computing", "DevOps", "Container Orchestration"]
series = []
comment = true
+++

After watching [@kelseyhightower's](https://twitter.com/kelseyhightower) speech at [Strangeloop 2015.](https://www.youtube.com/watch?v=pozC9rBvAIs) I was really impressed at the ease of instruction and demonstration he showed. I had not played with Kubernetes aside from using the kube-up.sh script in the github repo with the EC2 provider.

He starts off the talk by saying:
> How would you design your infrastructure if you could never login?

I have worked with clients and have said these exact words. It immediately grabbed my attention. 

Kelsey goes on to talk briefly about abstraction, containers,a sample application in Golang, and begins demonstrating application deployment to Kubernetes. 

After walking through the basic workings of Kubernetes, he provides an awesome illustration of resource utilization using Kubernetes, using Tetris.

Overall this is a great introduction to how Kubernetes works and the problems it aims at solving. Much to Hightower's credit, he also says what Kubernetes won't solve, if not in a kind of tongue and cheek way.

>If your in the enterprise and all your stuff is written in Java, and you have to deploy to Oracle... I have to be honest, there is nothing Kubernetes can do for you if you have that particular setup.

Now obviously he doesn't mean that, but it does paint a picture of when to use the tool and when not to. 

Overall if you haven't had a chance to play with Kubernetes or you don't know what all the hype is about. Check out his talk at Strangeloop. Head on over to [Kubernetes.io](http://kubernetes.io) and look through the getting started guide. They have providers for most of the major IaaS; AWS, GCE, Azure, and even Vagrant.

I am going to be working on getting started with AWS. The supported method, while if you have read my previous post I am not a fan of.

```bash
$ export KUBERNETES_PROVIDER=aws; curl -sS https://get.k8s.io | bash
```
 
Though supported, I opted to not go this route and clone the repo here [kubernetes @ github](https://github.com/kubernetes/kubernetes)

```
$ git clone https://github.com/kubernetes/kubernetes.git
$ cd kubernetes
$ export KUBERNETES_PROVIDER=aws
$ ./cluster/kube-up.sh
```

This will launch a combination of bash, cloudformation, salt and some other potpourri. After about 5 minutes or so you will be greeted with this output :
```
Kubernetes cluster is running.  The master is running at:

https://XX.XX.XX.XX


The user name and password to use is located in ...
... calling validate-cluster
Found 4 nodes.
      
Elasticsearch is running at https://XX.XX.XX.XX/api/v1beta3/proxy/namespaces/default/services/elasticsearch-logging
Kibana is running at https://XX.XX.XX.XX/api/v1beta3/proxy/namespaces/default/services/kibana-logging
KubeDNS is running at https://XX.XX.XX.XX/api/v1beta3/proxy/namespaces/default/services/kube-dns
Grafana is running at https://XX.XX.XX.XX/api/v1beta3/proxy/namespaces/default/services/monitoring-grafana
 is running at https://XX.XX.XX.XX/api/v1beta3/proxy/namespaces/default/services/monitoring-heapster
influxGrafana is running at https://XX.XX.XX.XX/api/v1beta3/proxy/namespaces/default/services/monitoring-influxdb
```
At this point if you cloned the repo, you can now navigate to the examples folder and begin playing around with creating pods, services, and exposing them.  For a little more direction I highly recommend [this walk through](http://kubernetes.io/v1.0/examples/guestbook/).
