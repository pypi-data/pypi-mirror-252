# Spyglass Web API

This is a web API for interacting with a Spyglass database. It is written in Python and uses FastAPI.

## Developer setup

Start a local spyglass instance. Instructions taken from [this notebook](https://github.com/LorenFrankLab/spyglass/blob/master/notebooks/00_Setup.ipynb).

```bash
# one time
docker pull datajoint/mysql:8.0
docker volume create dj-vol

# start the database
bash devel start-spyglass-database.sh
```

Clone spyglass and install it in development mode.

```bash
cd spyglass
pip install -e .
```

Configure spyglass.

```bash
cp dj_local_conf_example.json dj_local_conf.json
# Then edit dj_local_conf.json to set the database credentials and the directories for the data.

# Make sure to set "custom.no_prompts_mode": true, in the config file.
```

Set SPYGLASS_CONFIG_PATH to point to the spyglass config file, then run:

```bash
python devel/check-config.py
```

Install sgwa in development mode

```bash
pip install -e .
```

Start the web API.

```bash
# start the web API
bash devel/start-sgwa.sh
```

Check the database connection

```bash
python devel/check-db-connection.py
```