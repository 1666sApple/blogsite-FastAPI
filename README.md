# Blogsite FastAPI

This project is a simple blog platform built using **FastAPI**. It includes features such as user authentication, blog post management, article handling, and file uploads. The project also demonstrates exception handling for custom errors, such as story violations and terms violations.

## Features

- **Authentication:** User login and signup functionality
- **Blog Management:** Create, read, update, and delete blog posts
- **Article Management:** Manage articles, including adding and retrieving them
- **File Handling:** Upload and retrieve files
- **Custom Exceptions:** Story and terms violation exceptions handling

## Installation

### Prerequisites

- Python 3.9+(Used 3.12.5 here)
- FastAPI
- SQLAlchemy
- Other dependencies listed in `requirements.txt`

### Clone the repository

```bash
git clone https://github.com/1666sApple/blogsite-FastAPI.git
cd blogsite-FastAPI
```

### Install dependencies

Use pip to install all required Python packages:

```bash
pip install -r requirements.txt
```

### Set up the database

The project uses SQLAlchemy for ORM and SQLite as the default database engine. You can modify `db/database.py` to use a different database engine if required.

Create the tables by running:

```bash
python main.py
```

### Running the server

Run the FastAPI server with:

```bash
uvicorn main:app --reload
```

By default, the server will start at `http://127.0.0.1:8000`.

## Project Structure

- `main.py`: The entry point of the application. It includes route registrations and custom exception handlers.
- `auth/`: Handles user authentication.
- `routers/`: Contains different routers for handling blog posts, articles, users, and files.
- `db/`: Contains database models and the database connection logic.
- `exception/`: Defines custom exception classes for story and terms violations.

## API Endpoints

### Authentication

- `POST /auth/login`: User login
- `POST /auth/signup`: User signup

### User Management

- `GET /user/{id}`: Get user details by ID

### Blog Management

- `GET /blogs`: Retrieve all blog posts
- `POST /blogs`: Create a new blog post

### Article Management

- `GET /articles`: Retrieve all articles
- `POST /articles`: Create a new article

### File Upload

- `POST /upload`: Upload a file

## Custom Exceptions

- `StoryException`: Handles story-related issues. Returns a status code 418 (I'm a teapot).
- `TermsViolationException`: Handles violations of terms and conditions. Returns a status code 403 with additional details.

## Contributing

Feel free to fork the repository and submit pull requests. Any contributions that help improve functionality, structure, or performance are welcome!

## License

This project is licensed under the MIT License.