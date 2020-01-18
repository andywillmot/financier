# financier

<h2>Installation</h2>

1. Clone repository
`git clone https://github.com/andywillmot/financier.git`
1. Create environment files for dev and prod. For each file change `[RAND CHARS]` (can be different for each file), `[DEV_DB_PASSWORD]` and `[PROD_DB_PASSWORD]` to your own settings.

'''bash
cd financier
cp .env.prod.default .env.prod && nano .env.prod
cp .env.prod.db.default .env.prod.db && nano .env.prod.db
cp .env.dev.default .env.dev && nano .env.dev
'''




