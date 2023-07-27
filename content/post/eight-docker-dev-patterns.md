+++
date  = "2015-09-29T02:36:55-04:00"
draft = false
title = "Eight Docker Development Patterns"
header_img = ""
toc = true
tags = ["docker"]
categories = ["Software Development"]
series = []
comment = true
+++

This was a post I had stashed away a while ago by [Vidar Hokstad](http://www.hokstad.com).

He goes into some of the uses he has been seeing/using docker for. I have used some of these and I am sure there are even more development patterns out there now. The one I am most  interested in is the 'installer' container as he calls it.

There are so many installers that come in the form of...

```bash
$ curl http://what.is.this.bullsh.it | sudo sh
```

I can't stand it, I know I can't be alone on this.
<!-- more -->


>6. The Installation Container
This is not my own, but really deserves a mention. The excellent nsenter and docker-enter tools comes with an installation option that is a nice step forward from the popular but terrifying "curl [some url you have no control over] | bash" pattern. It does this by providing a Docker container that implements the "Build Container" pattern from above, but goes one step further. It deserves a look.<sup>1</sup>
<div align=right>~Vidar Hokstad
</div>

This post is a little old and while I don't necessarily agree with the 'mount' my home folder in this container too frequently, I think there are some good uses for docker in there (as if you needed anymore).

<sup>1</sup>Vidar Hokstad - [Eight Docker Development Patterns](http://www.hokstad.com/docker/patterns)
