+++
date = "2013-11-25T16:07:14-04:00"
draft = false
title = "Fixing mystery Kerberos log message in OS X"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Miscellaneous", "Operating Systems & Environment Management", "Networking & Security"]
categories = ["Operating Systems", "macOS", "Troubleshooting"]
series = []
comment = true
+++

I didn't notice this message popping up until I upgraded a couple machines to Lion, however once they were upgraded I began to see this message repeatedly in the log, roughly every 10 seconds.

>com.apple.launchd:(com.apple.Kerberos.kdc) Throttling respawn: Will start in 10 seconds

launchd spawns a process that continually attempts to authenticate with resources on the network.

I haven't done enough digging to know what exactly caused this change. Regenerating the localKDC stopped this message all together so far. You can do that by running this command.


`sudo /usr/libexec/configureLocalKDC`


Some people over on the Apple forums have seemed to point out that the launchd rule defined in...

>/System/Library/LaunchDaemons/com.apple.configureLocalKDC.plist

is broke, I haven't checked any newer installations but I would have to think that this is fixed in Mountain Lion and Mavericks.

