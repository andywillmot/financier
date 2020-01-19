# financier

<h2>Installation</h2>

1. Clone repository
```bash
    git clone https://github.com/andywillmot/financier.git
```
2. Create environment files for dev and prod. For each file change `[RAND CHARS]` (can be different for each file), `[DEV_DB_PASSWORD]` and `[PROD_DB_PASSWORD]` to your own settings. Optionally, you may also want to change the location of the DB data.  Change `postgres_data` to a location of your choice. 
```bash
    cd financier
    cp .env.prod.default .env.prod && nano .env.prod
    cp .env.prod.db.default .env.prod.db && nano .env.prod.db
    cp .env.dev.default .env.dev && nano .env.dev
```
3. Optionally, you may also want to change the location of the DB data.  Change "postgres_data" to a location of your choice.
```bash
    nano docker-compose.prod.yml
```
5. Build and run from compose file.  This is for the prod environment.  The docker-compose.yml builds a dev environment with DEBUG on, a clean DB each build and without the nginx proxy for static files.
```bash
    docker-compose -f docker-compose.prod.yml up -d --build
```
6. Setup database
```bash
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```
7. Create admin user
```bash
    docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```
8. Test
```bash
    For api testing: `http://your-docker-host-ip-address:1337`
    For admin login: `http://your-docker-host-ip-address:1337/admin`
```

<h2>Using Financier</h2>

<h3>API Auth Tokens</h3>
1. Get a auth token by calling this.  The <user> can be the user you setup in createsuperuser step above:
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py drf_create_token <user>
```

