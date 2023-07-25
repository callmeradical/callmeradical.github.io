+++
date = "2013-11-25T16:07:14-04:00"
draft = false
title = "Consolidating Snapshots in vSphere when using VDP or AVDP"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["vmware", "vsphere"]
categories = ["Administration"]
series = []
comment = true

+++

Let me start by saying this, I can't stand vSphere Data Protection, however I feel that since it is offered for free, and there is little to no management or maintenance for the virtual appliance, I see no reason in keeping it from my vSphere environment. That being said I still prefer to use Veeam for reliable backups of our virtual infrastructure at least on a weekly basis.

So anyway lets get started. The few times that VDP really does give me problems is when I get a warning that tells me my VM snapshots need to be consolidated.

<!-- more -->

Like a good sysadmin, I listen to what the system is telling me and I attempt to do just that.

Inside the vSphere web interface I go to the VM, select actions, go to 'All vCenter Actions', navigate to snapshots, and click Consolidate. Voila!

Wrong.

I get a message stating that an unspecified file is locked. (Actual error message may vary, and at the bottom of this post you can see some of the messages that this applies to.)

Well, that isn't very helpful at all. So I shut down the VM in question and attempt to consolidate again. No joy.

After some googling, I found that this is really only specific to if you are using the VDP or AVDP appliance by VMware. The reason for this, exists in the process of by which VDP creates backups.
_Taken from vmware.com's knowledgebase_

>Before backing up a virtual machine, the backup software takes a snapshot of the virtual machine. The backup software then mounts the virtual machine disk (.vmdk) on the backup appliance virtual machine to perform the backup. After the data is backed up, the appliance remove the .vmdk and the snapshot is deleted from the virtual machine.

>In some cases, the backup appliance may not release the lock on the .vmdk after the backup process, and snapshot commit/consolidation operations fail due to the lock.

>Note: The issue described in this article is applicable only when the backup appliance is running on a virtual machine/appliance.

So if you are having a problem, try this...


To remove the .vmdk from the backup appliance and commit/consolidate the snapshot:

1. Right-click the backup appliance virtual machine and click Edit Settings.

2. Check if the affected virtual machine's hard disk is mounted on the backup appliance virtual machine.

3. If the hard disk is mounted, select the hard disk and click Remove.

_Note:_ Under Removal Options, ensure to select the Remove from virtual machine option.

Click OK to exit.

