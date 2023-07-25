+++
date = "2015-10-28T00:59:36-04:00"
draft = false
title =  "Lambda, Docker/ECS, and S3... sitting in a tree."
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["AWS"]
categories = ["Cloud Engineering", "Software Development"]
series = []
comment = true
+++

To go along with a talk I am doing this week, I created a demo project to reinforce the idea behind ephemeral architecture and infrastructure as code. 

We create two S3 buckets for the purpose of intake and another to serve out a static site we will be generating using ECS. 

The first bucket is a place to drop photos which then triggers a lambda function, we will call this photo_bucket.

This piece of nodejs code will be the lambda we use to launch our ECS task:

```prettyprint lang-nodejs
console.log('Loading function');
var aws = require('aws-sdk');
exports.handler = function(event, context) {
  var ecs = new aws.ECS();
  var params = {
    taskDefinition: 'arn:account:::ecstask',
    count: 1,
    startedBy: 'lambda'
  };
ecs.runTask(params, function(err, data) {
  if (err) console.log(err, err.stack);
  else    { console.log(data); context.succeed('yew!');}
  });
};
```
 
To launch the static site I decided on Jekyll, which is the basis for a lot of Github hosted blogs, to generate a static site. I forked the code-base for Jekyll to my own repository and containerized it. Here is the Dockerfile:

```prettyprint lang-bash
FROM gliderlabs/alpine

RUN apk update
RUN apk upgrade

RUN apk add \
    git \
    imagemagick-dev \
    ruby-dev \
    build-base \
    libffi-dev \
    nodejs \
    python

RUN curl -sq "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
RUN unzip awscli-bundle.zip
RUN ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws

RUN git clone https://github.com/callmeradical/aws_techconnect /src

WORKDIR /src

RUN chmod +x scripts/sync.sh

RUN /usr/bin/gem install bundler

RUN bundle install

RUN bundle exec jekyll build

ENTRYPOINT /usr/bin/ruby scripts/set_env.rb && source creds && ./scripts/sync.sh 
```

There is some other stuff in here that I added to the repository since we are running on AWS. Namely a small script to grab credentials from the EC2 metadata of the docker host so we don't have to worry about storing credentials in the container or rebuilding it.

```prettyprint lang-ruby
require 'json'
url = '-sq http://169.254.169.254/latest/meta-data/iam/security-credentials/'
role = `curl #{url}`
doc = `curl #{url}/#{role}/`

creds = JSON.parse(doc)
File.open('creds', 'w') do |file|
  file.write("export AWS_KEY=\"#{creds['AccessKeyId']}\"\n")
  file.write("export AWS_SECRET=\"#{creds['SecretAccessKey']}\"\n")
  file.write("export BUCKET=\"s3://photo_bucket\"\n")
  file.write("export SITE=\"s3://demo_site\")
end
```

We use the credentials as environment variables and perform a sync from S3 to the container, build the site, and ship it.

```prettyprint lang-bash
aws s3 sync $BUCKET photos/
bundle exec jekyll build
aws s3 sync _site $SITE
```

This isn't the best way to do this but it helps illustrate an easy use case or model for performing batch processing.

If you want to stand this up yourself, the cloudformation templates are located in the [GitHub Repo](https://github.com/callmeradical/aws_techconnect) under the scripts folder.

Note: I didn't externalize the bucket names, so you may have to change the names of the buckets in the template and the set_env.rb file.
