+++
date = "2016-03-31T16:03:39-04:00"
draft = false
title = "Container best practices from RedHat"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Docker"]
categories = ["System Administration", "Software Development"]
series = []
comment = true

+++

I came across this post in a slack channel earlier today and thought it was some pretty sound advice for those starting out in the container eco system.


>First: Containers are immutable – The OS, library versions, configurations, folders, and application are all wrapped inside the container. You guarantee that the same image that was tested in QA will reach the production environment with the same behaviour.

>Second: Containers are lightweight – The memory footprint of a container is small. Instead of hundreds or thousands of MBs, the container will only allocate the memory for the main process.

>Third: Containers are fast – You can start a container as fast as a typical linux process takes to start. Instead of minutes, you can start a new container in few seconds.

>However, many users are still treating containers just like typical virtual machines and forget that containers have an important characteristic: Containers are disposable.

[Read More Here @ Red Hat's Developer Blog](http://developerblog.redhat.com/2016/02/24/10-things-to-avoid-in-docker-containers/)
