# financier

<h2>Installation</h2>

1. Clone repository
```bash
    git clone https://github.com/andywillmot/financier.git
```
2. Create environment files for dev and prod. For each file change `[RAND CHARS]` (can be different for each file), `[DEV_DB_PASSWORD]` and `[PROD_DB_PASSWORD]` to your own settings.
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
4. Make the entrypoint script executable (can't seem to get this to work within the Dockerfile)
```bash
    chmod +x mysite/entrypoint.sh
    chmod +x mysite/entrypoint.prod.sh
```
5. Build and run from compose file.  This is for the prod environment.  The docker-compose.yml builds a dev environment with DEBUG on, a clean DB each build and without the nginx proxy for static files.
```bash
    docker-compose -f docker-compose.prod.yml up -d --build
```
6. Setup database
```bash
    docker-compose exec docker-compose.prod.yml python manage.py migrate
```
7. Create admin user
```bash
    docker-compose exec docker-compose.prod.yml python manage.py createsuperuser
```
8. Test
```bash
    For api testing: `http://localhost:8000`
    For admin login: `http://localhost:8000/admin`
```


