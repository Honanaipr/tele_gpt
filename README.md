# Telegram bridge to chatGPT

## Configuration
```sh
mv .env.dist .env
```
replace **<BOT_TOKEN>** with your bot token in **.env**

## Install dependencies
```sh
poetry install
```

## Run
```sh
poetry run python -m tele_gpt
```
or
```sh
. start
```

## Build and run with Docker
```sh
docker build -t tele-gpt .
docker run -d tele-gpt
```

## Build and run with Docker-compose
```sh
docker-compose up -d --force-recreate
```

## Misc
### Install docker
```sh
apt install -y wget
wget -qO- https://get.docker.com/ | sh
```

### Update pip
```sh
pip install -U pip
```

### Install poetry
```sh
pip install poetry
```

### Load all from .env
```sh
set -o allexport && source .env && set +o allexport
```
