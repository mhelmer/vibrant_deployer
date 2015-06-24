
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

Example of a deploy hook with curl (on Gitlab CI):

```bash
curl -i -X POST -H "Content-Type: application/json" -d ''{"token":"CHANGEME", "ref": "''"$CI_BUILD_REF"''"}'' https://example.com:5000/deploy/
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
    ssl_certificate_key /etc/nginx/ssl/example.com.se.key;

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

