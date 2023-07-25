+++
date = "2013-11-25T16:07:14-04:00"
draft = false
title = "Command of the Day, purge!"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Operating Systems & Environment Management", "Miscellaneous"]
categories = ["Command Line", "Linux"]
series = ["Command of the Day"]
comment = true

+++

This is a common favorite of mine, especially when running VM’s locally. I have noticed with VMware fusion and Parallels there seems to be a delay in freeing up memory. If you you like things that make you happy, you will likely enjoy this:

``` bash
$ purge
```

1. Open up activity monitor
2. Open a terminal window
3. Issue the purge command
4. Watch your memory usage plummet after issuing the purge command.
5. Profit... Is this still relevant?

<!--More-->
<hr></hr>
Check out the man page of purge for more insight to what this actually does

NAME
     purge -- force disk cache to be purged (flushed and emptied)

SYNOPSIS
     purge

DESCRIPTION
     Purge can be used to approximate initial boot conditions with a cold disk
     buffer cache for performance analysis. It does not affect anonymous mem-
     ory that has been allocated through malloc, vm_allocate, etc.

