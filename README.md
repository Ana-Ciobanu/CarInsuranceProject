# Car Insurance Project

## Overview
This project is for managing car insurance data, including cars, owners, claims, policies, and insurance validity. It is built with Flask, SQLAlchemy, and Pydantic, and is designed for production use with Gunicorn and Docker.

## Features
- Manage cars and owners
- Create and track insurance claims and policies
- Validate insurance status for cars
- Health check endpoint
- PostgreSQL and Redis integration
- Environment-based configuration

## Tech Stack
- Python 3.11
- Flask & Flask-Smorest
- SQLAlchemy
- Pydantic (v2)
- PostgreSQL
- Redis
- Docker & Gunicorn

## Setup Instructions
1. **Clone the repository:**
	```sh
	git clone <repo-url>
	cd CarInsuranceProject
	```
2. **Configure environment variables:**
	- Edit `.env` file with your database and Redis settings.
3. **Install dependencies:**
	```sh
	pip install -r requirements.txt
	```
4. **Run with Docker (recommended):**
	```sh
	docker-compose up --build
	```
5. **Run locally (development):**
	```sh
	flask run
	```
6. **Run in production:**
	```sh
	gunicorn --bind 0.0.0.0:5000 app.main:create_app()
	```

## API Endpoints

### Owners
- `POST /api/owners` — Create a new owner

### Cars
- `GET /api/cars` — List all cars
- `POST /api/cars` — Add a new car
- `DELETE /api/cars/<carId>` — Delete a car

### Claims
- `POST /api/cars/<carId>/claims` — Create a claim for a car

### Policies
- `POST /api/cars/<carId>/policies` — Create a policy for a car

### History
- `GET /api/cars/<carId>/history` — Get car history

### Insurance Validity
- `GET /api/cars/<carId>/insurance-valid?date=YYYY-MM-DD` — Check insurance validity for a car on a specific date

### Health Check
- `GET /health` — Service status

## Docker Usage
The project includes a `Dockerfile` and can be run with Gunicorn for production. Use `docker-compose` for easy setup of all services.
