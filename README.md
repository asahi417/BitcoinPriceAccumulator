# BTC Price Accumulator
Get bitcoin price from [bitflyer API](https://lightning.bitflyer.com/docs?lang=en) and accumulate to postgres SQL.

## Get started
Clone and setup some environment variables for DB.

``
git clone 
cd btc_price_accumulator
export DB_HOST="host for postgres"
export DB_USER="user for postgres",
export DB_PORT="port for postgres",
export DB_NAME="db name for postgres" 
``

Start postgres service and create db,

```
sudo service postgresql
createdb btc_price
```

Note that to access Postgres DB by sqlalchemy,
you need to edit `/var/lib/pgsql/9.6/data/pg_hba.conf` to change the all access method to `trust`.

Then, setup the database by
```
>>> python initialize_db.py
```
