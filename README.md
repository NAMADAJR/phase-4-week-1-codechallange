# Phase 4 week 1 Code Challenge - Superheroes
## By Namada Jr
## Project Overview
This project involves building an API for tracking superheroes and their powers using Flask for the backend and React for the frontend. The API manages heroes, powers, and their associations.

## Features
- Flask API with models: `Hero`, `Power`, `HeroPower`
- Supports basic CRUD operations for superheroes and their powers
- Validations for hero powers and power descriptions
- Pre-built React frontend for API testing

## Setup

Install backend dependencies:
```bash
pipenv install
pipenv shell
```
Install frontend dependencies:

```bash
npm install --prefix client
```

Run the Flask server:

```bash
python server/app.py
```

Start the React frontend:
```bash
npm start --prefix client
```

## Routes
### Heroes:
- `GET /heroes` - Returns all heroes.
- `GET /heroes/:id` - Returns a hero by ID, including powers.
### Powers:
- `GET /powers` - Lists all powers.
- `GET /powers/:id` - Fetches power details by ID.
- `PATCH /powers/:id` - Updates a power’s description.
### Hero Powers:
- `POST /hero_powers` - Associates a hero with a power.

## Testing
Run tests with pytest:

```bash
pytest -x
```
Alternatively, use the provided Postman collection for API testing.

