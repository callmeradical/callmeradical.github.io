+++
draft = false
date = "2016-11-15T21:10:46-05:00"
title = "AWS API Gateway with Kubernetes Ingress Map"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["AWS", "Kubernetes"]
categories = ["Cloud Engineering", "Kubernetes"]
series = []
comment = true
+++

Working on large scale unified APIs seems to be a popular trend. Recently I was working with 
Microsoft's Graph API, which is their unified API. It is not unreasonable to think that many 
different teams contribute to the different resources available; mail, calendars, contacts, 
directories. However many resources, the idea is to have all of them referenced from the same 
endpoint.

Ideally each team could use whatever language, whatever technology best worked for them. AWS API
Gateway fullfills that easily.

*Note: This post makes the assumption that you have a functional Kubernetes cluster*

First we are going to create a new api in Service Gateway.

```bash
$ aws apigateway create-rest-api --name demo

$ export API_ID=<created api id>

$ aws apigateway get-resources --rest-api-id=$API_ID

$ export PARENT_ID=<resource id>

$ aws apigateway create-resource \
	--rest-api-id=$API_ID \
	--parent-id=$PARENT_ID \
	--path-part="health"

$ export HEALTH_ID=<resource id>

$ aws apigateway put-method \
	--rest-api-id=$API_ID \
	--resource-id $HEALTH_ID \
	--http-method GET \
	--authorization-type NONE
```

We are going to stop with the API gateway for now, but we will come back to it.

Let's take a look at the app we are going to be running.

[Source Code @ Github](https://github.com/callmeradical/healthy)

``` go
package main

import (
	"encoding/json"
	"log"	
	"net/http"
)

type Response struct {
	Version	string `json:"version"`
	Message string `json:"message"`
}

func healthz(w http.ResponseWriter, r *http.Request) {
	res := Response{
		Version: "v1.0",
		Message: "We are Healthy!",
 	}

	str, err := json.MarshalIndent(&res, ", "\t")
	if err != nil {
		log.Println(err.Error())
	}

	w.Write(string(str))
}

func main() {
	http.HandleFunc("/health", healthz)
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
``` 

The app we are going to use is a restful application that responds to a GET on the /health endpoint
on port 8080 and prints "We are healthy!"

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  labels:
    app: healthy
  name: healthy
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: healthy
      name: healthy
    spec:
      containers:
        - name: healthy
          image: "callmeradical/healthy:1.0.0"
---
apiVersion: v1
kind: Service
metadata:
  name: healthy-app
  labels:
    app: healthy
spec:
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: healthy
```

So now this little snippet of yaml will create a deployment in kubernetes and 
expose it. Let's go ahead and deploy our app. While we are at it we can verify our 
app is in fact actually running and serving traffic.	

From the root of the cloned project:

```bash
$ kubectl create -f kubernetes/healthy-deployment-svc.yml

$ kubectl get pods

$ kubectl port-forward <name of pod here> 8080:8080

$ curl localhost:8080/health
{
	"version": "v1.0",
	"message": "We are Healthy!"

}
```

> A Deployment provides declarative updates for Pods and Replica Sets (the next-generation 
> Replication Controller). You only need to describe the desired state in a Deployment object, 
> and the Deployment controller will change the actual state to the desired state at a 
> controlled rate for you. You can define Deployments to create new resources, 
> or replace existing ones by new ones.
>
>   -- Kubernetes Documentation @ (http://kubernetes.io/docs/user-guide/deployments/#what-is-a-deployment)

Now we have our app and a skeleton for API Gateway, but we aren't quite done, everything is still very disjointed. 
We still need to create our ingress map, our nginx controller, and finish creating the API gateway. 

Let's start working on deploying the ingress controller. An ingress controller is a daemon that is deployed 
as a kubernetes pod. That pod watches the API server's /ingresses endpoint for updates to the ingress resource. 
Its job is to satisfy requests for ingress.

We aren't going to write our own controller, that is out of the scope of this post (maybe down the road :) , but we are going to use 
the example controller used on the Kubernetes site, the nginx controller. The nginx controller does the following:

- Poll until apiserver reports a new ingress
- write the nginx config file based on a go text/template
- Reload nginx

Using the example nginx controller requires that we deploy a default-backend. Luckily that is also provided from 
their example. [default-backend @ github.com/kubernetes](https://github.com/kubernetes/contrib/tree/master/404-server)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: default-http-backend
  labels:
    k8s-app: default-http-backend
spec:
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  selector:
    k8s-app: default-http-backend
---
apiVersion: v1
kind: ReplicationController
metadata:
  name: default-http-backend
spec:
  replicas: 1
  selector:
    k8s-app: default-http-backend
  template:
    metadata:
      labels:
        k8s-app: default-http-backend
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: default-http-backend
        # Any image is permissable as long as:
        # 1. It serves a 404 page at /
        # 2. It serves 200 on a /healthz endpoint
        image: gcr.io/google_containers/defaultbackend:1.0
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 30
          timeoutSeconds: 5
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: ReplicationController
metadata:
  name: nginx-ingress-controller
  labels:
    k8s-app: nginx-ingress-lb
spec:
  replicas: 1
  selector:
    k8s-app: nginx-ingress-lb
  template:
    metadata:
      labels:
        k8s-app: nginx-ingress-lb
        name: nginx-ingress-lb
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - image: gcr.io/google_containers/nginx-ingress-controller:0.8.3
        name: nginx-ingress-lb
        imagePullPolicy: Always
        readinessProbe:
          httpGet:
            path: /healthz
            port: 10254
            scheme: HTTP
        livenessProbe:
          httpGet:
            path: /healthz
            port: 10254
            scheme: HTTP
          initialDelaySeconds: 10
          timeoutSeconds: 1
        # use downward API
        env:
          - name: POD_NAME
            valueFrom:
              fieldRef:
                fieldPath: metadata.name
          - name: POD_NAMESPACE
            valueFrom:
              fieldRef:
                fieldPath: metadata.namespace
        ports:
        - containerPort: 80
          hostPort: 80
        - containerPort: 443
          hostPort: 443
        # we expose 18080 to access nginx stats in url /nginx-status
        # this is optional
        - containerPort: 18080
          hostPort: 18080
        args:
        - /nginx-ingress-controller
        - --default-backend-service=$(POD_NAMESPACE)/default-http-backend
```


Now we want to expose our load balancer so we can forward traffic to it from our API Gateway. There are a couple of ways 
to create a Kubernetes service; You can create a spec file like we have been doing above, or you can just issue the command 
directly to the Kubernetes API via kubectl. Let's go with the second option. 

```bash
$ kubectl get rc
NAME                       DESIRED   CURRENT   AGE
default-http-backend       1         1         30m
nginx-ingress-controller   1         1         30m
$ kubectl expose rc nginx-ingress-controller --type=LoadBalancer --port=80 --target-port=80
$ kubectl get svc -o wide
```

The last command should give you something like this:

```bash 
NAME                       CLUSTER-IP       EXTERNAL-IP                                                               PORT(S)    AGE       SELECTOR
nginx-ingress-controller   100.71.197.180   < aws classic loadbalancer cname here >			  	                      80/TCP     4m        k8s-app=nginx-ingress-lb
healthy-app                100.68.182.151   <none>                                                                    80/TCP     6d        app=healthy
default-http-backend       100.68.139.29    <none>                                                                    80/TCP     5d        k8s-app=default-http-backend
```
Let's hit our load balancer and see what we get so far.	

![default-http-backend](https://dl.dropboxusercontent.com/s/r4yzfxja74z9eex/k8s_default_backend.png?)

Great so we now have our nginx controller exposed, looks like it is working... 

Let's set up our ingress to verify that we can route traffic to our application. 
An Ingress is a collection of rules that allowi inbound connections to reach the cluster services.
I am using Route53 for my DNS for this example. I created an entry in the callmeradical.com hosted zone 
for an alias to my nginx load balancer that we created just before this. When I hit this record with the 
"/health" endpoint, it will route traffic to our healthy-app and provide a health check.

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: demo-app-ingress
spec:
  rules:
    - host: demo.callmeradical.com
      http:
        paths:
          - path: /health
            backend:
              serviceName: healthy-app
              servicePort: 80
```


So now we have our basic app, an nginx controller, default web backend, an ingress map that is currently mapping 
our "/health" endpoint to our healthy-app service. If you were only using Kubernetes in your organization you could 
probably stop here and start building out a really flexible API leveraging microservices. However, the guy next to you 
is probably saying something along the lines of:

> "Containers are so last year, serverless is where it's at." 

Hey everyone is entitled to their opinion, and we know it actually is servers all the way down, but let's help this guy out. 

We are going to front our services using API Gateway so other teams can use whatever delivery method they choose. We are now going 
to finish our API Gateway service we started building out. This includes creating our method, integration, integration-response, 
method-response, and deploying our API.


```bash 
$ aws apigateway put-method \
	--rest-api-id $API_ID \
	--resource-id $HEALTH_ID \
	--http-method GET \
	--authorization-type NONE

$ aws apigateway put-integration \
	--rest-api-id $API_ID \
	--resource-id $HEALTH_ID \
	--http-method GET \
	--type HTTP \
	--integration-http-method GET \
	--uri http://demo.callmeradical.com/health \
	--passthrough-behavior WHEN_NO_MATCH

$ aws apigateway put-integration-response \
	--rest-api-id $API_ID  \
	--resource-id $HEALTH_ID 
	--http-method GET \
	--status-code 200 \
	--response-templates '{"application/json": "}'

$ aws apigateway put-method-response \
	--rest-api-id $API_ID \
	--resource-id $HEALTH_ID \
	--http-method GET \
	--status-code 200 \
	--response-models '{"application/json": "Empty"}'

$ aws apigateway create-deployment \
	--rest-api-id $API_ID \
	--stage-name v1 \
	--stage-description 'v1 of our api' \
	--description 'first deployment'
```

Now that we have our API deployed we can navigate to the invoke URL of the API, or just curl it. The invoke URL 
is in the following form:

> https://$API_ID.execute-api.$REGION.amazonaws.com/$STAGE

*Note: you can also set up a custom domain for the API if you so choose*

![API Gateway Health](https://dl.dropboxusercontent.com/s/n6r1q2n7ce7rhgw/k8s_api_gateway_health.png?dl=0)



That's it. We now have a service running in Kubernetes and being fronted by API Gateway. In this example, API gateway also happens to 
be running in another account. This is now ready to be extended to other teams and services. With API gateway you get some neat features 
like throttling, authentication/authorization, lifecycle management, SDK generation, and more. This tutorial/demo may seem like a lot of 
work, but in reality a good deal of this content is fairly "out-of-the-box" so to speak. Kubernetes and the community as a whole has 
provided a ton of useful tools. For example, I created my route53 entry manually, but you could just as easily use a controller like 
the one provided [here by the folks of wearemolecule @ Github] (https://github.com/wearemolecule/route53-kubernetes). Kubernetes is truly an 
amazing project, and the future looks very bright.

Thanks,<br>
Lars
