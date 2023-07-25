+++
date = "2013-11-25T16:07:14-04:00"
draft = false
title = "Connecting to OS X VPN on Windows 7 and Later"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["System Administration"]
categories = ["System Administration"]
series = []
comment = true

+++

When setting up windows machine's for VPN access to OS X server's builtin VPN service there is some tweaking that I have always found necessary.


1. Add this to your registry:

`[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\PolicyAgent]
"AssumeUDPEncapsulationContextOnSendRule"=dword:00000002`

2. Open secpol.msc (click start > search for secpol.msc)

- Local Policies > Security Options
- Network Security : LAN Manager Auth Level…
- Set to: Send LM & NTLMv2 - UseNTLMv2…

And

- Network Security : Minimum session security… clients
- uncheck "Require 128-bit encryption"

3. Restart PC

4. Create VPN Connection on Windows 7

- Host Name: (server IP or yourhost.name.com)
- PPP Settings : Enable LCP (only)
- Type: L2TP/IPSec
- Pre-shared key : yoursharedsecret
- Data encryption : Optional encryption
- Allow CHAO and CHAPv2

5. Router on server-side must allow VPN Passthrough and forward ports: 50, 51, 500, 548, 1701, 1723, 4500 to the server box. Also, do not filter anonymous internet requests, multicast or NAT Redirection but enable SPI Firewall.

Following these steps should produce a working VPN connection on Windows 7 when connecting to a VPN provided by OS X server.



