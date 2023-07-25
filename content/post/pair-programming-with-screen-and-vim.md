+++
date  = "2015-03-07T02:05:52-04:00"
draft = false
title  = "Shared environments and toolsets"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Software Development", "Miscellaneous", "System Administration", "DevOps"]
categories = ["Technology", "Programming", "Coding", "Development", "Teamwork", "Workstation"]
series = []
comment = true
+++

Hey Andre, Look at this!


Over the past 5 months I have been working on a team of about five people on a shared workstation. 

Originally I had my reservations about other people working on the same machine as everyone else, but was
quickly swaying to use it myself. 
Rather than set everyone up on their windows laptops (which I still think is a huge barrier for entry) our workstation 
was originally set up to help other people start coding, developing, and learning ruby. 

A local IRC client and server on the box allows us all to converse and share ideas while working or ask for help. For 
people that have been a linux sysadmin you know how great `wall` can be when post notices to a workstation. So as I was
testing out this machine for our client, I rapidly started to see how much easier it is to work with a group of 
people using the same tools. I traded Atom for Vim and my multiple desktops in OS X for screen. The world is a great place.

This is a common occurence recently:

As I am writing some code, I get a bell in my screen 0 window (IRC), 
someone is having an issue with ChefSpec and wants a second set of eyes. 
Since everyone on the workstation has sudo access we run screen with 
setuid root (This sounds much worse than it is) so all John or Jane Doe has to do is:

```bash
Ctrl + A : multiuser on
Ctrl + A : acladd lars
```

and I follow suit and run this:

```bash
$ screen -x johndoe/[session_name]
```
I now have a direct window into everything John or Jane is working with and 
seeing the code he or she is running. I have used screen sharing before and
sometimes it works well, but I think this shared workstation has gotten the whole team
into a certain type of workflow and by using all the same tools it has become much easier to
support one another.

Probably not a huge surprise.

