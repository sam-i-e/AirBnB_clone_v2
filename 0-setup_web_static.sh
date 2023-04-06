#!/usr/bin/env bash
# Sets up the webserrver for the deployment of web_static

# Installs Nginx
apt-get update
apt-get install -y nginx

# Create respective folders to be served by Nginx
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Hello Brian. Welcome!" > /data/web_static/releases/test/index.html

# Creates a symbolic link
ln -s /data/web_static/releases/test/ /data/web_static/current

# Sets permissions for user and group
chown -R ubuntu /data/
chgrp -R ubuntu /data/

# Sets configurations details to server and location blocks
printf %s "server {
	listen      80 default_server;
	listen      [::]:80 default_server;
	root        /var/www/html;
	index       index.html index.htm;
	add_header  X-Served-By $HOSTNAME;
	location /hbnb_static {
		alias /data/web_static/current/;
		index index.html index.htm;
	}
	location /redirect_me {
		return 301 http://cuberule.com/;
	}
	error_page 404 /404.html;
	location /404 {
		root /var/www/html;
		internal;
	}
}
" > /etc/nginx/sites-available/default

# Restarts nginx after loading configuration changes
service nginx restart
