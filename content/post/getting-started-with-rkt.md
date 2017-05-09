+++
date = "2017-04-18T09:36:05-04:00"
draft = true
title = "Getting Started With RKT"
image = "https://dl.dropbox.com/s/yth2fdpjb6q7me9/rkt.png"
+++


I remember a while back, there was a bunch of back and forth in the container community around container runtimes.
At this point Docker was the defacto standard, largely because of it's image format, but otheres were
critical that Docker was trying to do too much. Mixing the network stack and adding in volumes and a ton
of other stuff, that quite frankly just make it easier to adopt containers.

Not long after this back and forth started,in June of 2015, Docker had open-sourced a significant portion of it's code base
to the newly formed Open Container Initiative [OCI](https://www.opencontainers.org). This wasn't that surprising, when considering
almost 50% of the codebase was based off of LXC at the time.

So by my own admission I had used Docker almost exclusively for the past two years. I had never really given RKT a chance. 
I wanted to see exactly how different it was running RKT as opposed to Docker, not just for the novelty, but to really see
if there was something fundamentally different in the experience.

Let's begin.



## Getting Started

I am following the tutorial/getting started guide from [CoreOS](https://coreos.com/rkt/docs/latest/trying-out-rkt.html)

