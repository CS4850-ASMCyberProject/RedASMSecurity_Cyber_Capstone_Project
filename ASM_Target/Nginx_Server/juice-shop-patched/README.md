## Patched OWASP Juice Shop Nginx Server Configuration

After downloading nginx, under `/etc/nginx/sites-enabled/juice-shop:patched`, Add:

```bash

server {
  server_name secure-shop.redasmsecurity.cloud;

  location / {
     proxy_pass http://127.0.0.1:3001;
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

The implementation of parameterized queries simplifies the server configuration as blocks and hardening are no longer needed with a patched backend.

The `# managed by Certbot` code lines are added automatically after certbot is used to make the service discoverable to public DNS databases & subfinder.
```bash
sudo certbot --nginx -d shop.redasmsecurity.cloud
```
