+++
date = "2017-07-23T13:51:34-04:00"
title = "Kubernetes: Resource Requests, Limits, and Quality of Service"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Kubernetes", "Open Source", "Resource Management", "CPU Management", "Memory Management", "Quality of Service", "Containerization"]
categories = ["Open Source", "Cloud Computing", "DevOps"]
series = []
comment = true
+++
# 
Caution, opinion ahead. Let me first state that I believe Kubernetes to be one of the most well designed projects in the open source community today. The depth of documentation and the understanding that goes into features and architecture is rare. We adopted Kubernetes as a platform a little over a year ago. Things have been running very smoothly and have had zero major incidents and a few maintenance issues (very minor) for the duration. We recently had our first service outage, and as such were asked to produce our first root cause analysis (RCA) for affected parties. All of the information I am talking about here is just a distillation of the documents located at [here](https://github.com/kubernetes/community/tree/master/contributors/design-proposals). We will be looking at how resource request and limits correlate to Kubernetes quality of service classes.

There are currently two types resources you can request in Kubernetes: CPU and Memory. CPU is compressible, while memory (currently) is incompressible. Compressible resources mean that throttling said resource is a fairly benign event. Incompressible resources, on the other hand, are likely to cause some level of grief when throttled. 

Compressible resources:

- Pods are guaranteed to get the amount of CPU they request, they may or may not get additional CPU time (depending on the other jobs running). This isn't fully guaranteed today because cpu isolation is at the container level. Pod level cgroups will be introduced soon to achieve this goal.
- Excess CPU resources will be distributed based on the amount of CPU requested. For example, suppose container A requests for 600 milli CPUs, and container B requests for 300 milli CPUs. Suppose that both containers are trying to use as much CPU as they can. Then the extra 100 milli CPUs will be distributed to A and B in a 2:1 ratio (implementation discussed in later sections).
- Pods will be throttled if they exceed their limit. If limit is unspecified, then the pods can use excess CPU when available.

Incompressible resources:

- Pods will get the amount of memory they request, if they exceed their memory request, they could be killed (if some other pod needs memory), but if pods consume less memory than requested, they will not be killed (except in cases where system tasks or daemons need more memory).
- When Pods use more memory than their limit, a process that is using the most amount of memory, inside one of the pod's containers, will be killed by the kernel.

Memory is fairly straight-forward on the surface. Memory values are measured in bytes, and can use the following suffixes: Ei, Pi, Ti, Gi, Mi, Ki.

CPU is not so straight forward and is an abstraction layer for a few different knobs. Let’s examine what CPU means in Kubernetes. 


                        1 AWS vCPU
    1 Kubernetes CPU =  1 GCP Core
                        1 Azure vCore
                        1 Hyperthread w/ bare-metal

CPU is always requested as an absolute quantity, never relative. This means that 1 CPU is the same on a single core, dual-core, or 48-core machine. When assigning resources fractional values are allowed, but more commonly the use of whole numbers with the suffix `m` is used to denote a unit called `millicores`.

For Example:

    0.1 CPU == 100m

When pods are submitted to Kubernetes with resource requests for CPU they can be translated to flags that are being set when launching Docker containers (I do not know the equivalent in RKT, although I intend to follow up on that, sorry!).

Docker Flags:

    --cpu-shares == CPU Requests
    --cpu-quota  == CPU Limits
    --cpu-period == Is always set to the default value of 100,000 (100ms)

Then the way that Kubernetes calculates the core value(which is potentially a fractional number). It is then multiplied by 1024. If the number is larger than 2 it is used, otherwise the number of CPU Shares is 2.
When handling CPU shares in Docker, this refers to weighted distribution.

Weighted Distribution:

      c1 = 1024 Shares
      c2 = 512  Shares
      c3 = 512  Shares

When all three containers request 100% of their CPU, c1 would receive 50% while c2 & c3 would only receive 25%. 
Furthermore if we added an additional container with 1024 shares:

      c1 = 1024 Shares
      c2 = 512  Shares
      c3 = 512  Shares
      c4 = 1024 Shares

This time, all four containers request 100% of their CPU, c1 & c4 will each receive 33% while c2 & c3 would receive only 16.5% of a core.

When scheduling pod with resource requests, each node has a maximum capacity for each resource type. Scheduling is based on requests, not limits. In Kuberentes v1.6 the concept of `node-allocatable` was introduced to pods.


> Allocatable will be computed by the Kubelet and reported to the API server. It is defined to be:
>
> `[Allocatable] = [Node Capacity] - [Kube-Reserved] - [System-Reserved] - [Hard-Eviction-Threshold]`
>
> The scheduler will use `Allocatable` in place of `Capacity` when scheduling pods, and the Kubelet will use it when performing admission checks.
        [— Node-allocatable proposal](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/node-allocatable.md)


The scheduler ensures that for each resource type, the sum of the resource requests of the containers in the pod, do not exceed the capacity of the node (not exactly, but more on this later). Based on the resource requests of a pod Kubernetes provides different classes for quality of service (QoS). 

Pods that need to stay up can request resources and set limits. When the resources requested are equal to the resource limits, resources are guaranteed, this is the most static type of QoS kubernetes provides and is called you guessed it; Guaranteed.

 If pods have one or more resources requested and limits are set, the class would be Burstable. This is more dynamic and allows for greater resource utilization. 

 The last class of pods are Best-Effort. There are no limits set for any resources across a pods containers. This means that the container is able to use up to the node’s capacity provided other pods or processes don’t request more memory or CPU.
