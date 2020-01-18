# financier

<h2>Installation</h2>

1. Clone repository
`git clone https://github.com/andywillmot/financier.git`
1. Create environment files for dev and prod. For each file change `[RAND CHARS]` (can be different for each file), `[DEV_DB_PASSWORD]` and `[PROD_DB_PASSWORD]` to your own settings.
    cd financier
    cp .env.prod.default .env.prod && nano .env.prod
    cp .env.prod.db.default .env.prod.db && nano .env.prod.db
    cp .env.dev.default .env.dev && nano .env.dev
1. Build and run from compose file
    docker-compose -f docker-compose.prod.yml up -d --build
1. Setup database
    docker-compose exec docker-compose.prod.yml python manage.py migrate
1. Create admin user
    docker-compose exec docker-compose.prod.yml python manage.py createsuperuser
1. Test
    For api testing: `http://localhost:8000`
    For admin login: `http://localhost:8000/admin`


