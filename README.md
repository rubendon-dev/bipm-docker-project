# Titanic Web App

A simple Flask web application that combines data analysis with Docker containerization.

## Tech Stack

* Flask
* Redis
* Pandas
* Matplotlib
* Docker Compose

## Features

* Visitor counter powered by Redis
* Titanic dataset overview
* Survivor visualization by gender
* Dockerized deployment

## Run Locally

```bash
docker compose up --build
```

Open the application at:

```text
http://localhost:4000
```

## Pages

### Home

Displays a live visitor counter using Redis.

### Titanic

Shows Titanic dataset records and a chart of survivors grouped by gender.
