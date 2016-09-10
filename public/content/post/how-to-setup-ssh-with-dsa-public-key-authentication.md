+++
date = "2013-11-25T16:07:14-04:00"
draft = false
title = "How-to Setup SSH with DSA public key authentication"

+++

* Generate a DSA Key Pair

	    $ ssh-keygen -t dsa

The output should look like like this:

		Enter file in which to save the key (/home/my_computer/.ssh/id_dsa):  Press [Enter] key
		Enter passphrase (empty for no passphrase): myPassword
		Enter same passphrase again: myPassword
		Your identification has been saved in /home/my_computer/.ssh/id_dsa.
		Your public key has been saved in /home/my_computer/.ssh/id_dsa.pub.
		The key fingerprint is:
		04:be:15:ca:1d:0a:1e:e2:a7:e5:de:98:4f:b1:a6:01 my_computer@my_computer-desktop

* Next we have to set the permissions for the directory 
CD to the .ssh directory and modify the permissions.
    
    	$ cd ~/.ssh && chmod 755 .ssh
   
* Now we copy the public key.

		$ scp ~/.ssh/my_computer/id_dsa.pub user@my_server:.ssh/authorized_keys
             
* After that finishes we can remote in to the remote server and set the correct permissions for the key.
			
            $ chmod 600 ~/.ssh/authorized_keys
    
 * Finally on your local machine...
 
 `exec /usr/bin/ssh-agent $SHELL` and then `ssh-add`
 
 
 Enjoy logging in without interuption.

