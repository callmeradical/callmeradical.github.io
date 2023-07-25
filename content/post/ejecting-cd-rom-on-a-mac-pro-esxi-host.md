+++
date = "2013-11-25T16:07:14-04:00"
draft = false
title = "Ejecting CD-rom on a Mac Pro ESXi Host"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["System Administration", "Miscellaneous", "Cloud Engineering"]
categories = ["System Administration"]
series = []
comment = true
+++

So if you are ever in a pinch and need to use a piece of optical media, you can operate the CD-rom door via Command Line when you SSH into your ESXi Mac Pro.

For instance:
(Enable ssh in the Security Profile of the Configuration tab on the vSphere client. Remember to turn this off after you are done.)

``` bash
$ ssh root@esxi.host.machine
# cd /dev/cdroom
# ls
# eject vmp.*.*
```
That will then eject your tray, leaving you to wondrously explore legacy optical media that no one wants.

Cheers!

