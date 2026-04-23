## Original OWASP Juice Shop Nginx Server Configuration

After downloading nginx, under `/etc/nginx/sites-enabled/juice-shop`, Add:

```bash

server {
  server_name shop.redasmsecurity.cloud;

  include /etc/nginx/sites-enabled-block-rules/juice-shop-search-block;

  modsecurity on;
  modsecurity_rules_file /etc/nginx/modsec/juice_shop_modsec_main.conf;

  location / {
     proxy_pass http://127.0.0.1:3000;
     proxy_http_version 1.1;

     proxy_set_header Host $host;
     proxy_set_header X-Real-IP $remote_addr;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;

     proxy_set_header Upgrade $http_upgrade;
     proxy_set_header Connection "upgrade";

   }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/shop.redasmsecurity.cloud/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/shop.redasmsecurity.cloud/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

```

juice-shop-search-block is where the slack button "Contain Path" writes the temporary sql injection block using the remote automated script

Modsecurity is turned on and it's config file is included named modsecurity_rules_file

The `# managed by Certbot` code lines are added automatically after certbot is used to make the service discoverable to public DNS databases & subfinder.
```bash
sudo certbot --nginx -d shop.redasmsecurity.cloud
```
