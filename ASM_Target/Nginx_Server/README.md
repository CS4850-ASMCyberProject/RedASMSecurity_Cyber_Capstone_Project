## Nginx Download

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Slack Contain Path folder 

Create a folder where the automated script for the Slack button `Contain Path` will write the temporary block to block sql injection key words

In /etc/nginx:

```bash
mkdir sites-enabled-block-rules
```

## Check & Reload Nginx After Any Alertations

This command should be used after changing any code inside nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```
