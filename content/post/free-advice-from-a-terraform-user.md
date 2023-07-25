+++
date  = "2016-03-31T20:40:23-04:00"
draft = false
title = "Free advice from a Terraform user"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Terraform"]
categories = ["Advice"]
series = []
comment = true
+++

Firstly a huge thank you goes out to [@mipsytipsy](https://twitter.com/mipsytipsy?lang=en) for this awesome post mortem on what appears to be or what could have been one of the worst outages of her career.


>Some context: our terraform config had been pretty stable for a few weeks.  After I got it set up, I hardly ever needed to touch it.  This was an explicit goal of mine.  (I have strong feelings about delegation of authority and not using your orchestration layer for configuration, but that’s for another day.)

>And then one day I decided to test drive Aurora in staging, and everything exploded.


[Read more @ Charity.wtf](http://charity.wtf/2016/03/30/terraform-vpc-and-why-you-want-a-tfstate-file-per-env/)
