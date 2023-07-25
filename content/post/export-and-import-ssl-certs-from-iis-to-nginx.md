+++
date = "2013-11-25T16:07:14-04:00"
draft = false
title =  "Export and Import SSL Certs from IIS to nginx"
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Networking & Security", "Operating Systems & Environment Management", "Miscellaneous"]
categories = [".NET", "Linux", "Server Migration", "SSL Certificates"]
series = []
comment = true

+++

While transitioning a website built in .NET there came a time to move the server to something a little more robust... like Linux! The following steps are more for my benefit but they may help in a pinch.
<!-- More -->
<hr></hr>

To export the SSL certificate from your Windows Server:

1. Run "mmc.exe" from Start->Run menu;
2. Open "File"->"Add/Remove Snap-in";
3. Click on "Add..." button, select "Certificates" option, click "Add", select "Computer account"; Next; Finish;
4. Close "Add standalone snap-in"; close "Add/Remove snap-in" by "Ok" button;
5. Open "Personal" folder and find corresponding certificate;
6. Right click on "Certificates", select "All tasks"->"Export";
7. On "Certificate export wizard" click Next, select "Yes, export the private key", select "Personal Information Exchange" format, click Next, enter password, select file, click Finish.

Copy the Certificate files to your server to the directory on your server where you will keep your certificate and key files. Make them readable by root only to increase security.

Concatenate the primary certificate and intermediate certificate.

You need to concatenate the primary certificate file (your_domain_name.crt) and the intermediate certificate file (DigiCertCA.crt) into a single pem file by running the following command:

``` bash
cat DigiCertCA.crt >> your_domain_name.crt
```

Edit the Nginx virtual hosts file:

Now open your Nginx virtual host file for the website you are securing. If you need your site to be accessible through both secure (https) and non-secure (http) connections, you will need a server module for each type of connection. Make a copy of the existing non-secure server module and paste it below the original. Then add the lines in bold below:

```
server {

listen 443;

ssl on;
ssl_certificate /etc/ssl/your_domain_name.crt; (or .pem)
ssl_certificate_key /etc/ssl/your_domain_name.key;

server_name your.domain.com;
access_log /var/log/nginx/nginx.vhost.access.log;
error_log /var/log/nginx/nginx.vhost.error.log;
location / {
root /home/www/public_html/your.domain.com/public/;
index index.html;
	}
}
```

Adjust the file names to match your certificate files:

ssl_certificate should be your primary certificate combined with the intermediate certificate that you made in the previous step (e.g. your_domain_name.crt).
ssl_certificate_key should be the key file generated when you created the CSR.
Restart Nginx.

``` bash
sudo /etc/init.d/nginx restart
```

