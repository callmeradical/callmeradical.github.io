+++
date = "2013-11-25T16:07:14-04:00"
draft = false
title = "Failed to connect to VMware Lookup Service"
+++

I had a problem logging into the vCenter vSphere web client earlier this week and was greeted with a message stating "Failed to connect to VMware Lookup Service."

More after the jump for the solution.
<!--More-->
At first I tried this method, which is outlined here, [Yellow-bricks](http://www.yellow-bricks.com/2012/12.1/19/failed-to-connect-to-vmware-lookup-service-ssl-certificate-verification-failed/)

>Precise error:
>Failed to connect to VMware Lookup Service.
>SSL certificate verification failed.
>I had been playing around in my lab and I am guessing this error was caused by the fact that I changed the hostname of my vCenter Server Appliance after configuring it. When I rebooted the VCVA I bumped in to this issue. Luckily it is very easy to solve:
>Go to http://<vcenter ip address or fqdn>:5480
>Click “Admin” Tab
>Click “Toggle certificate setting” under “Actions”
>Restart the vCenter Server Appliance
>During the restart the certificates will be regenerated
>Click “Admin” Tab and disable the “Toggle certificate setting”

This would have been awesome, and I have seen this work in the past. However, If you are not seeing the specific failure for "SSL Certificate verification failed."
This probably will not do anything for you.

Instead the only way I have been able to recover from this is to drop my database contents and reset.

The set-up is not arduous, but can be a little annoying. If any knows of a better way to go about this, please shoot me a message.

