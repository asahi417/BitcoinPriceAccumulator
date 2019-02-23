# BTC Price Accumulator
Micro service to get bitcoin price from [bitflyer API](https://lightning.bitflyer.com/docs?lang=en) and accumulate to postgres SQL.

## Get started
Firstly, start ppostgres service and create db,

```
sudo service postgresql
createdb {DB_FOR_STORE_PRICE}
```

Note that to access Postgres DB by sqlalchemy,
you need to edit `pg_hba.conf` to change the all access method to `trust`.

Clone and setup some environment variables for DB.

```
git clone 
cd btc_price_accumulator
pip install .
export DB_HOST="host for postgres"
export DB_USER="user for postgres"
export DB_PORT="port for postgres"
export DB_NAME={DB_FOR_STORE_PRICE} 
```

Run server

```
python bin/run_accumulator.py
```

### Slack webhook
You can post log of accumulation via slack webhook by add following environment variable before running server.

```
export SLACK_WEBHOOK='slack webhool url for channel to post log'
``` 