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
3. Build and run from compose file
```bash
    docker-compose -f docker-compose.prod.yml up -d --build
```
4. Setup database
```bash
    docker-compose exec docker-compose.prod.yml python manage.py migrate
```
5. Create admin user
```bash
    docker-compose exec docker-compose.prod.yml python manage.py createsuperuser
```
6. Test
```bash
    For api testing: `http://localhost:8000`
    For admin login: `http://localhost:8000/admin`
```


