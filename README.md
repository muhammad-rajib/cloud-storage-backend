# Setup CloudStorage Application

## Step: 01

### Clone `Git` Project

> git clone https://github.com/project.git \
> cd your_project

## Step 02:

### Install Dependencies

Before you start, ensure that `pipenv` is installed. If not, you can install it using the following command:

> `run:` pip install pipenv

Create virtualenv using pipenv:

> `run:` pipenv install

Activate the virtual environment created by pipenv:

> `run:` pipenv shell \
> OR \
> `run:` source $(pipenv --venv)/bin/activate

Install dependencies using pipenv

> `run:` pipenv install -r requirements.txt

## Step: 03

### Manage .env file for `FastAPI` Application

Create .env file in project root dir and put all necessary values.

> `run:` touch .env

### OR create .env file using scripts/create_env.sh bash file

This bash file will create .env and put basic depedencies for you.
Modify .env file based on your application required depedencies.

> `move:` create_env.sh file to home(~) directory

Run below commands:

> `run:` chmod +x create_env.sh \
> `run:` ./create_env.sh \
> `run:` vim .env (add application depedencies and save)

## Step: 04

### Run Database Migrations

for database migrations, run the migration commands to set up the database schema:

Generate migration script for new changes

> `run:` alembic revision --autogenerate -m "applied new changes in db migration"

Adpat new changes into Database

> `run:` alembic upgrade head

## Step: 05

### Run the `FastAPI` Application

> `run:` uvicorn main:app --reload
