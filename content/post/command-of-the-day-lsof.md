+++
date = "2013-11-25T16:07:14-04:00"
draft = false
title = "Command of the Day, lsof!"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["System Administration", "Miscellaneous"]
categories = ["Command Line", "Linux"]
series = ["Command of the Day"]
comment = true
+++

How often have you ever moved a file to trash, attempted to empty the trash only to be greeted with an awesome message that states "Cannot delete this file its in use blah blah" nonsense?

While lsof can definitely help in these scenarios. I prefer to use it for looking at ports, examples after the break.

<!--More-->
<hr></hr>

lsof can...

List all open files

``` bash
lsof
```

Find out who is using a file...
``` bash
lsof /path/to/file
```

Find all open files in a directory recursively...
``` bash
lsof +D /path/to/search
```

List all open files by a user...
``` bash
lsof -u username
```

The list goes on and on and is almost unlimited. This here is what I consider to be the gem of this command though.

``` bash
lsof -i -n -P
```

This will output all currently open ports, the processes using them, and the user that launched the process. This makes it very easy to troubleshoot network connections with various database software.

Thats all for now.
