# BulletinBoardMMORPG

## Description

BulletinBoardMMORPG is a web application for creating and managing advertisements in MMORPGs. Users can create ads, respond to them, and manage the status of ads and responses.

## API Features

The API provides the following features:

- Adding a new advertisement.
- Retrieving an advertisement by ID.
- Updating advertisement data.
- Retrieving advertisements by user email.
- Working with advertisement images.

## Technologies

- **Django** – for creating the web application.
- **Django REST Framework** – for creating the API.
- **PostgreSQL** – for data storage.
- **Celery** – for asynchronous task processing.
- **Redis** – for Celery task broker.
- **TinyMCE** – for content editing in advertisements.

## Installation

1. Clone the repository:
    ```sh
    git clone <your repository URL>
    cd bulletinboard
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # For Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    Create a [`.env`](.env ) file in the root directory of the project and add the following lines:
    ```env
    DB_LOGIN=<your login>
    DB_PASSWORD=<your password>
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=mmorpg

    DJ_SCRT_KEY=<your Django secret key>

    FROM_EMAIL_USER=<your email>
    FROM_EMAIL_PASSWORD=<your email password>
    FROM_DEFAULT_EMAIL=<your email>
    ```

5. Apply migrations:
    ```sh
    python manage.py migrate
    ```

6. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

7. Start the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

1. Go to `http://localhost:8000` in your browser.
2. Register or log in.
3. Create ads, respond to them, and manage them.

## Project Structure

- [`announcement/`](mmorpg/announcement) - application for managing ads and responses.
- [`users/`](mmorpg/users) - application for managing users and email verification.
- [`mmorpg`](mmorpg) - main project application containing settings and configurations.

## Setting up Celery

Celery is used for sending notifications. Make sure you have Redis installed and running:

1. Install Redis:
    ```sh
    sudo apt-get install redis-server
    ```

2. Start Redis:
    ```sh
    sudo service redis-server start
    ```

3. Start Celery:
    ```sh
    celery -A mmorpg worker --loglevel=info
    ```
    
