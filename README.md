
Install Flask in virtualenv

```bash
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```

Customize local_settings.py. Make sure that the remote repository etc is set up accordingly in the deploy tree.

```bash
cp local_settings.py.example local_settings.py
```

Example of a deploy hook with curl (on Gitlab CI) with `SECRECT_KEY` set up as a variable:

```bash
curl -i -X POST -H "Content-Type: application/json" -d ''{"key":"''"$SECRET_KEY"''", "ref": "''"$CI_BUILD_REF"''"}'' https://example.com:5000/deploy/
```

This will however give a return code of 0 for all HTTP status codes. To account for non-200 status codes, we can use a script that checks for it and outputs the data to stderr.

```bash
/usr/bin/env bash

statuscode=$(curl --silent --output /dev/stderr --write-out "%{http_code}" -i -X POST -H "Content-Type: application/json" -d '{"key":"'"$DEPLOY_KEY"'", "ref": "'"$CI_BUILD_REF"'"}' https://example.com:5000/deploy/)

if [ $statuscode -ne 200 ]
then
	exit 1
fi
```

Example nginx site-config:
```nginx
upstream vibrant_deployer {
    server unix:///var/www/run/vibrant_deployer.sock;
}

server {
    listen              5000 ssl;
    server_name         example.com;
    ssl on;
    ssl_certificate     /etc/nginx/ssl/example.com.crt;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;

    access_log /var/log/nginx/vibrant_deployer.access.log;
    error_log /var/log/nginx/vibrant_deployer.error.log;
    charset utf-8;

    client_max_body_size 300M;


    location / {
        include uwsgi_params;
        uwsgi_pass vibrant_deployer;
    }
}
```

