### Patched OWASP Juice Shop Container
A hardened version of OWASP Juice Shop was created by modifying the application source code and rebuilding it as a custom Docker image.

#### Steps

1. Clone/download the OWASP Juice Shop source code from GitHub

2. Modify the vulnerable application code

3. Rebuild the application into a custom Docker image

4. Run the patched container on a separate local port


#### Add Parameterized Queries

- `/routes/search.ts`

Under the function searchProducts in search.ts, Patch the code:

Add a parameter which santizes user input. This treats user input as a string instead of SQL code, protecting against SQL Injection.

Replace:
```bash
models.sequelize.query(`SELECT * FROM Products WHERE ((name LIKE :criteria OR description LIKE :criteria) AND deletedAt IS NULL) ORDER BY name`{replacements: {criteria: likeCriteria}})
```
With:
```bash
const likeCriteria = `%${criteria}%`
models.sequelize.query(`SELECT * FROM Products WHERE ((name LIKE :criteria OR description LIKE :criteria) AND deletedAt IS NULL) ORDER BY name`{replacements: {criteria: likeCriteria}})
```

#### Build Command

Build the new docker image with the patched code and run the juice-shop:patched website.

```bash

docker build -t juice-shop:patched .


sudo docker run -d --name juice-shop-patched --restart unless-stopped -p 127.0.0.1:3001:3000 juice-shop:patched
```
