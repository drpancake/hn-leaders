# HN Leaders

## Running locally

Prerequisites:

- Python 3.10
- virtualenv
- pip
- Git
- Heroku Toolbelt

Create a virtual environment:

    $ arch -x86_64 bash
    $ source ~/.bash_profile
    $ mkvirtualenv --python=`which python3.10` hn-leaders
    $ pip install --upgrade pip
    $ pip install -r requirements.txt
    $ (ctrl-d to close bash)

Run locally:

```sh
gunicorn run:app
```
