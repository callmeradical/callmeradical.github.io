+++
title = "Adding the version number of your rails app using git"
type = "post"
draft = false
date = "2013-11-25T16:07:14.000Z"

+++

An easy methodology of "stamping" your commits would be to create an environment varible to store the return value of:
    git describe --always

This should by default always return the most recent tagged release or branch name.

You can store this variable in the environment.rb file of your project by appending this line of code:
    APP_VERSION = `git describe --always` unless defined? APP_VERSION

This was originally retrieved from this fine human being [Daniel Pietzsch](http://blog.danielpietzsch.com/post/1209091430/show-the-version-number-of-your-rails-app-using-git) 

