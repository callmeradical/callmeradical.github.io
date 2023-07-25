+++
date = "2013-11-25T16:07:14-04:00"
draft = false
title = "Understanding boxen, a Sysadmin's realization..."
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Boxen", "Puppet", "System Administration", "Version Control", "Software Development", "DevOps"]
categories = ["Technology", "Software Development", "DevOps", "System Administration"]
series = []
comment = true

+++

So I had a hard time understanding what exactly [boxen](http://boxen.github.com) was used for at first. I also didn't really see much value other than setting a "base" system.

<!--More-->

However after working with puppet and reading some of the other posts by [Gary Larizza](http://garylarizza.com/blog/2013/02/15/puppet-plus-github-equals-laptop-love/ "Blog from Gary Larizza, an Engineer at Puppet Labs with a lot to say.") I think that boxen can really be summed up into an intelligently designed way to run puppet in an organization that requires more freedom for its users than typical. This is particularly true of development shops.



So often system administrators want to lock everything down and provide the least amount of options to the end user. Updates, software, websites are all controlled because this is the easiest way to manage all of the systems in one's environment.

Now throw in a monkey wrench, there is a small group of people that are working on this project and they all need mysql installed with some particular databases and they need to be able to quickly access data dumps on a remote server. The rest of your organization has no need for any of this and you really don't want to confuse more users. So what do you do? This, I think is where boxen really shines.

You can give the keys to the castle to your users and still make sure that the basic essence of your environment remains intact by having specialized puppet manifests run on each users machine according to the project or person. Boxen enables this through version control of puppet manifests and modules.

When you update the source code, your users run ‘boxen’  which will pull down the updated code and run it on the machine kind of like a super-powerful ‘puppet apply’


So I guess the easiest way to explain boxen is a puppet-managed environment with no master.

