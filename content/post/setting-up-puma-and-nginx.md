+++
date = "2013-11-25T16:07:14-04:00"
draft = false
title = "Setting up Puma and Nginx"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Software Development", "System Administration", "Miscellaneous", "DevOps"]
categories = ["Technology", "Web Development", "Servers", "Programming"]
series = []
comment = true
+++

*(This article assumes familiarity with reverse proxy software such as Varnish or Nginx)*

For those of you not familiar with puma you can check out more information [here - Puma.](http://puma.io) and if that is too much to read, it can be summarized here…

* Puma is a very lightweight and incredibly fast web server that was built for speed and parallelism. For comparisions of other webservers check out the link above.

As scability and multi-tenancy issues arise, the benefits of using a stack which utilizes a reverse proxy and web server tends to make more sense. The reverse proxy can feed into a pool of web apps as opposed to an instance of apache which would act as both load balancer and route the request to a single web server instance that would fork more processes to meet the demand. The diagram below generally depicts how this works.

<!-- more -->


**A reverse proxy: Example**

									+---> web app 1 process --> threads
									|
    [requests]<-->[reverse proxy server]--+---> web app 2 process -> threads
									|
									+---> web app 3 process -> threads


**Traditional Apache: Example** 

				+---  web app process fork
				|
    [requests]-------  web app process fork
				|
				+--- web app process fork
				
				
There have been some debates and I have read conflicting reports of which way is better. Quite honestly I don't think we are ever going to find a one size fits all solution for these problems. Take a look at your application and try to figure out which makes sense for that project and put in your implementation, or do some research and benchmark each. I just want to put this out there so maybe some of you can get behind it.

# Installing Puma 

Installation is very quick and easy…

In any Rails 3+ app add the following to your Gemfile.
	
	gem 	'puma',	'~> 2.5.1'
	
Then issue a quick `bundle install`

When in that directory you can type `rails s` to start your app and you should be greated with something that looks similar to this:

	Puma starting in single mode...
	blah blah blah blah
	
Congratulations Puma is installed!

# Installing Nginx

Nginx is the reverse proxy server we are going to be using. Mainly beceause we can utilize its `HttpProxyModule` to pass requests to any number of virtual hosts.

Installation varies from distro to distro I recommend compiling from source because generally what is available in the package managers is out of date.

If you would like to see these methods go ahead and [look here - Nginx installation](http://wiki.nginx.org/install).

# Configuring Nginx
The particular configuration I use is to utilize the `upstream` directive to tell Nginx where to proxy parse the request to. Then we will add the virtual host and use `proxy_address` directive to tell Nginx to pass the request to the pool of processes defined in the `upstream` section.

***Warning: these instructions will vary from distro to distro***

First remove the default virtual hosts files.

`sudo rm /etc/nginx/confi.d/default.conf`

Next we have to create a new host config file. This will typically be located at `/etc/nginx/conf.d/project_name.conf` for our rails app fill in this file with this code, you can replace the sections labeled project_name with your own project name.

	upstream project_name {
	  server unix:///var/run/project_name.sock;
	}
	
	server {
	  listen 80;
	  server_name project_name_url.com; # change to match your URL
	  root /var/www/project_name/public; # I assume your app is located at this location
	
	  location / {
	    proxy_pass http://project_name; # match the name of upstream directive which is defined above the server block
	    proxy_set_header Host $host;
	    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	  }
	}
	
*note: You may need to modify the permissions of the /var/run directory if  the user is not a member of wheel.*

Then you can restart your Nginx server:

	sudo /etc/init.d/nginx restart
	
# Starting Puma 

`cd` to your project's directory and bind Puma to a unix socket.

	RAILS_ENV=production bundle exec puma -e production -b unix:///var/run/project_name.sock
	
This is of course of little use to us outside of a testing scenario, we really want to run this as a daemon. We can do this very easily by supplying the `-d` parameter, like so:
	
	RAILS_ENV=production bundle exec puma -e production -d -b unix:///var/run/project_name.sock


And that is essentially it! You should now be up and running!

Managing puma requires a little bit of Unix-fu or command line mastery, some basic commands:

* This will show you the PID in use by puma.
	`ps aux | grep puma`

* This will stop and and restart puma. 
	`kill -s SIGUSR2 #pid_number_from_ps_aux`
	*note: this will kill itself and fork a new process with a new PID*
* This will terminate the puma daemon.
	`kill -s SIGTERM #pid_number_from_ps_aux`	
	
	
That is it for now, you can expect an in depth view of managing puma in the days to come. We will look at managing your pid's, sockets, and other built in functions in Puma. 


Cheers!
		

