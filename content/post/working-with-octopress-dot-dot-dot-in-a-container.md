+++
date = "2015-09-25T05:33:56-04:00"
draft = false
title = "Working with octopress... in a container."
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Docker", "Miscellaneous", "Software Development", "Google", "System Administration", "docker"]

categories = ["Technology", "Software Development", "Docker", "Blogging", "System Administration", "Web Development", "Networking", "DevOps"]
series = []
comment = true

+++

So I have been on a bit of a kick with Docker. I have been in Boston talking 
about it, giving webinars on it, and using it just about everywhere in every 
which way I can.

One of the first things I realized is that I hate installing dependencies on 
all of my things. Installing ruby, git, gcc, and not to mention all the gems 
that I need to run. 

I decided the first thing I wanted to do was make it easier to write my blog
(which is already ridiculously easy, thanks Github!), I also just wanted to 
see if I could run my blog outside of Github pages if the need arises.
<!-- more -->
So here we go.

[www.octopress.org](Octopress) is/was a blogging framework largely based on 
[www.jekyllrb.com](Jekyll). Since then it has been replaced with a variety 
of Gems. 

Dockerfile
```
FROM debian:8.1

RUN apt-get update
RUN apt-get install -y \
  git \
  ruby \
  ruby-dev \
  rubygems \
  build-essential \
  nodejs \
  python

RUN git clone https://github.com/callmeradical/callmeradical.github.io
WORKDIR callmeradical.github.io

RUN git checkout source
RUN /bin/bash -l -c "gem install bundler"
RUN /bin/bash -l -c "bundle install"

EXPOSE 4000

RUN apt-get autoremove -y
RUN useradd -ms /bin/bash lars
USER lars
ENTRYPOINT ["/usr/local/bin/rake", "preview" ]
```
We can look at this a little closer for those that have never written a Dockerfile before.
The very first line:
```
FROM debian:8.1
```

Tells me that I am inheritting from another container. All the configuration that went into 
making that container can be viewed on [hub.docker.com](Docker Hub).

So that will get me to a base install of the OS. The next few lines are pretty self 
explanatory. I am installing packages necessary for the my application to run.

```
RUN apt-get update
RUN apt-get install -y \
  git \
  ruby \
  ruby-dev \
  rubygems \
  build-essential \
  nodejs \
  python


```

Now we are ready to clone in our project:

```
RUN git clone https://github.com/callmeradical/callmeradical.github.io
WORKDIR callmeradical.github.io

RUN git checkout source
```
I am using github pages to deploy my blog and it builds 'master' from 'source' so 
I check out the source branch and install my gems..

```
RUN /bin/bash -l -c "gem install bundler"
RUN /bin/bash -l -c "bundle install"
```
EXPOSE Docker that the container will listen on the specified network ports at runtime. 
Docker uses this information to interconnect containers using links, which is helpful if 
we decide we want to run our blog in a more traditional way fronted by Nginx or apache.

Finally I add a user with the same username as my local machine, this is pretty important.
```
EXPOSE 4000

RUN useradd -ms /bin/bash lars
USER lars
ENTRYPOINT ["/usr/local/bin/rake", "preview" ]
```

Now I add this file to my octopress blog repo and I can now build my container:

```
docker build --rm=true -t callmeradical/blog:latest .
```


That might take a little bit to install the packages and deps, but once that is complete 
I can now run my blog locally while editing/working on posts.

```
docker run -i -t \
-v ~/src/1_docker_callmeradical.github.io:/callmeradical.github.io \ 
-p 80:4000 \
-d --name blog callmeradical/blog              
```

This might look unusual at first but there is a reason why I am running it this way.
I can perform all my edits locally and the preview will continue to regenerate the view 
for me. Combine that my transparent terminal, I can see whats happening as I am posting.

Now if I have to interact in a different way to say do a deployment, or generate a new 
post, I can just use 
```
docker exec -ti <command>
```

