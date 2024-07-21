# HN Leaders

## Running locally

Prerequisites:

- Python 3.10
- virtualenv
- pip
- Git
- Heroku Toolbelt

Create a virtual environment:

```sh
mkvirtualenv --python=`which python3.10` hn-leaders
pip install --upgrade pip
pip install -r requirements.txt
```

Run locally:

```sh
./scripts/run-local.sh
```

## Deploy

```sh
git push heroku master
```

## Logs

```sh
./scripts/logs-production.sh
```

## First time setup

```sh
heroku create --buildpack heroku/python --region us hn-leaders
heroku dyno:type web=hobby  # don't sleep
```
