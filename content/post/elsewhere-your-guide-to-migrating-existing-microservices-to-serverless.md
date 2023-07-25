+++
title = "Shared: How to Migrate Existing Microservices to Serverless"
type = "post"
draft = false
date = "2018-06-15T19:35:14.000Z"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Miscellaneous", "Cloud & Serverless Technologies"]
categories = ["Cloud Engineering"]
series = []
comment = true
+++

> When you have a set of microservices running on VMs or inside Docker containers, consider moving some of them to serverless. Here are some commonly cited reasons:
>
> Cost: Services with low traffic, or cron jobs, are cheaper with serverless. This is because you don’t pay for them when they’re idle.  
>
> Time to market: You get more done, faster. Free yourself of the undifferentiated heavy lifting of managing infrastructure. Focus on your users’ needs instead.  
>
> Scalability: You can scale faster and more aggressively because you’re not constrained by the amount of spare capacity you reserve (and have to pay for) for scaling.  
>
> Easier ops: You get logging and monitoring out of the box. You can also integrate with other services for tracing, alerting, and visualization.  
>
> Security: You have more fine-grained control of access. Give each function only the permissions it needs to minimize attack surface.  
>
> Resilience: You get multi-AZ out of the box with AWS Lambda.  
>
> Suffice to say that there are many benefits to moving some of your microservices to serverless. But, there are also challenges you need to
overcome as you make the transition. You will find that many of the practices
and tools you rely on are no longer suitable. And you need to rethink how you
approach building production-ready microservices with serverless.

[Keep Reading @ blog.binaris.com - Yan Cui](https://blog.binaris.com/your-guide-to-migrating-existing-microservices-to-serverless/)
