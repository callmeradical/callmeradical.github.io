+++
title = "Everything is Software"
type = "post"
draft = false
date = "2018-06-08T16:07:14.000Z"
description = "Revisiting Past Conferences: Evolving Perspectives and the Rise of Serverless Technology"
subtitle = ""
header_img = ""
toc = true
tags = ["AWS", "Miscellaneous", "DevOps", "Productivity", "Cloud Engineering", "Google", "Azure"]
categories = ["Conference Reflections", "Technology Trends", "Infrastructure Modernization", "Serverless Computing"]
series = []
comment = true
+++

Perhaps it's just nostalgia but I love listening to talks from old conferences
and meetups I have been to. When attending you have one frame on mind and
depending on the environment or situation you were in when attending, you
receive the information one way but as time goes on you arrive at a different
place. How do those conclusions change when you revisit them? 

In 2015, I had been working on a large scale modernization project for a
customer. The engagement was largely focused on an implementation of Chef. We
were automating all the things. We were practicing good software practices. We
had unit tests with 100% coverage on all of our recipes. Integration suites to
run for each flavor of OS we were supporting. We were regularly deploying to
production multiple times a day. It felt good.

Werner Vogels took the stage of the AWS Summit in New York in 2015 quoting a
paper Nick Carr wrote in May 2003 titled "IT Doesn't Matter."

In his paper Carr outlines how information technology follows a pattern
incredibly similar to that of earlier technologies such as railroads and
electricity. 

For a brief period, as they are being built into the infrastructure of
commerce, these "infrastructural technologies", as I call them, open
opportunities for forward-looking companies to gain strong competitive
advantages. But as their availability increases and their cost decreases - as
they become ubiquitous - they become commodity inputs. They may be more
essential than ever to society, but from a strategic business standpoint, they
become invisible; they no longer matter.

In Werner's talk he draws the conclusion that "Only if you are able to focus on
really building the products you want to build can you actually compete in
today's marketplace."

I had to reflect a little bit about what we were doing. Was it really
important? How did it benefit the customer? I was delivering value afterall.
Our code shepered software from environment to environment on it's way to
production. If we didn't write our code, the new features would never ship.

In 2016, I found myself sitting in a very similar seat when Werner took the
stage in New York, this time he was on a roll talking about Lean manufacturing
principals and eliminating waste. He stated that "Waste is anything that
doesn't benefit the customer." then once again calling back to Nick Carr's
paper, this time he drew a similar conclusion, but phrased it in a way that I
feel was more meaningful.

There is a certain amount of IT that everyone else has to do and as such it is
not a competitive differentiator and if it doesn't differentiate you, it
doesn't matter to your customers.

This tells me a few things. First, I should probably read that paper he keeps
referencing (I have since read said paper). Second, that there is going to be a
certain amount of waste that is necessary for business to function. Lastly, the
waste you want to eliminate is in value streams that eventually end in customer
benefit, that is agility.

Now, let's finally talk a little bit about serverless. Serverless covers two
separate areas, with the older of the two being Backend as a Service (BaaS).
This is used to describe applications that use third-party or SaaS solutions to
manage server-side logic: cloud-accessible databases, authentication services,
etc. The newer, and often more recognized meaning is Functions as a Service
(FaaS). This puts the control of server-side logic back in the hands of the
developer without the need to manage infrastructure. All the hype is currently
around Functions as a Service. Every cloud provider has their own flavor of
this and all of them have a portfolio of serverless offerings. Amazon Web
Services with things like AWS Lambda and Amazon DynamoDB, while Google has
Firebase and Google Functions, and Azure has CosmosDB and Azure Functions. It
seems like serverless is taking off everywhere. 

I think this is the beginning of the realization that Werner was talking about.
When you abstract the underlying infrastructure, you remove a significant
portion of concerns that can be seen as waste. Operational metrics in regards
to infrastructure do not matter to the customer, it is IT that everyone has to
do. By eliminating this function or concern in IT you  have given your
developers and engineers the ability to focus on the things that matter most.
Your customers.







