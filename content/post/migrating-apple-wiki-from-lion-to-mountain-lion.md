+++
date = "2013-11-25T16:07:14-04:00"
draft = false
title = "Migrating Apple Wiki from Lion to Mountain Lion"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["System Administration", "Miscellaneous", "Database", "Cloud Engineering"]
categories = ["IT Solutions", "Server Management", "Operating Systems"]
series = []
comment = true
+++

Well here is the first post to this blog with some substance to it!

Here is a little backstory on the situation. I found myself almost immediately scouring the internet one morning when my boss had told me there was a problem with our server (at this point in time it was our only server) that was currently running OS X 10.7, Lion. I was not a fan of Lion server as it was a major departure from the server OS we all knew and loved. I was initially brought in to move to a virtual infrastructure in a vCenter managed environment. After many internet searches turned up incomplete instructions I figured I would post the exact steps I went through the get the job done.
<!--More-->
<hr></hr>

These are the steps that were necessary to migrate information from OS X 10.7 Lion (Tamman Server) to OS X 10.8 Mountain Lion (TMN108SVR-1)
First step is done on the source OS X server, perform this command in Terminal as an administrator this will dump the Postgres database to a file:

```  bash
sudo pg_dump --format=c --compress=9 --blobs --username=collab --file=/tmp/collab.pgdump collab
```

Once that finishes, copy /tmp/collab.pgdump from the source server to /tmp/collab.pgdump on the destination server, then copy the contents of /Library/Server/Wiki/FileData on the source server to /Library/Server/Wiki/FileData on the destination server.


*** Note: you may also need to copy /usr/share/collabd/server to the destination server (see below)

Log in to the destination server as an administrator and execute the following commands in Terminal to ensure correct ownership and permissions, start the Postgres database, populate it with the data dumped from the source server, and finally start up the wiki service:

``` bash
sudo chown -R _teamsserver:_teamsserver /Library/Server/Wiki/FileData
sudo chmod -R +a "www allow read" /Library/Server/Wiki/FileData
sudo serveradmin stop wiki
sudo serveradmin start postgres
sudo rake -f /usr/share/collabd/server/Rakefile db:drop
sudo serveradmin stop wiki
sudo serveradmin start postgres
sudo rake -f /usr/share/collabd/server/Rakefile db:drop
```

This file may not be present and needs to be created on the server in order for this last command to complete successfully. This is why we copy the directory and files from the previous install.

``` bash
sudo createuser -U _postgres -d -s collab
sudo createdb -U collab collab
sudo -u _postgres pg_restore -d collab -U collab --single-transaction /tmp/collab.pgdump
sudo serveradmin start wiki
```

** Important: These steps will cause any wikis already present on the destination server to be lost.
Note: Migrating wikis does not migrate users or groups. This will either have to been done as an Open Directory or Active Directory. 

