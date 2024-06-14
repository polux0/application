## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- Cachetools
- python-jose[cryptography]
- passlib[bcrypt]
- email-validator

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/polux0/application

2. **Create and activate a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  

3. **Install the dependencies**

    ```
    pip install -r requirements.txt
    
4. **Start up MySQL via docker-compose**

    ```
    docker-compose up -d

## Running the Application

1. **Start the FastAPI server**
    
    ```bash
    uvicorn app.main:app --reload

2. **Access the API documentation**

    Open your browser and navigate to http://127.0.0.1:8000/docs to view the interactive API documentation provided by Swagger UI.


## Project Overview

### Main Application (`app/main.py`)

-   Initializes the FastAPI app.
-   Sets up the database and creates tables at startup.
-   Includes routers for authentication and post-related endpoints.

### Models (`app/models.py`)

-   Defines SQLAlchemy models for `User` and `Post`.

### Schemas (`app/schemas.py`)

-   Defines Pydantic models for data validation and serialization.

### Controllers (`app/crud.py`)

-   Contains CRUD operations for interacting with the database. ( Will be renamed to controller.py)

### Dependencies (`app/dependencies.py`)

-   Provides common dependencies, such as database sessions.

### Routers (`app/routers`)

-   **auth.py**: Handles authentication-related routes.
-   **posts.py**: Handles CRUD operations for posts.

### Database Configuration (`app/database.py`)

-   Configures the SQLAlchemy database engine and session.


