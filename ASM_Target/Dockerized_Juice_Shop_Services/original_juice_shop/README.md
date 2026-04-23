### Standard OWASP Juice Shop Container

The standard vulnerable Juice Shop instance was deployed directly from the official Docker image without modifying the application source code.

#### Run Command
```bash
sudo docker run -d --name juice-shop --restart unless-stopped -p 127.0.0.1:3000:3000 bkimminich/juice-shop
```

-p 127.0.0.1:3000:3000 keeps local port 3000 secure, opening it up only to the ASM_Target's loopback address.
The service is exposed to the Internet through an Nginx reverse proxy server; The server acts as a VPN for a service similar to a VPN for a user. 

--restart unless stopped keeps the service running automatically through system crashes and reboots

