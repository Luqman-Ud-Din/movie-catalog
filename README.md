# movie-catalog

## Tech Stack
1. Python 3.8.6
1. Django 3.1.2

## Setup

#### Pre-requisites
You need to install `docker` and `docker-compose` according to your OS from following links
1. [Docker](https://docs.docker.com/engine/install/)
    1. Tested with Docker version `19.03.12, build 48a66213fe`
1. [Docker Compose](https://docs.docker.com/compose/install/)
    1. Tested with docker-compose version `1.26.2, build eefe0d31`

#### Run Server
1. `docker-compose build --no-cache`
1. `docker-compose up`

#### Run Tests
`docker exec -it movie_catalog bash -c "python manage.py test"`

#### Test Coverage Report
`docker exec -it movie_catalog bash -c "coverage run --omit=*/migrations/* --source='.' manage.py test && coverage report"`

#### How it Looks in Browser
`http://localhost:8000/movies/`

![movie-catalog](movie-catalog-browser.png)

## Architecture
![architecture](movie-catalog-architecture.png)

## What can be Improved?
1. We can make use of `celery` instead of `django-crontab`
1. We can optimize update database operations in cron job by designing some mechanism to fetch only those movies which don't exists in our system.
1. We can make a separate container for database in order to allow our system to horizontally scale.
1. We can open socket communication with the client, so that whenever a new movie is fetched from `Studio Ghibli Server`, we can notify our users in near real time.