# Blogsite FastAPI

A robust and scalable blog platform built with FastAPI, featuring user authentication, blog management, and file handling.

## Features

- **User Authentication:** Secure login and signup functionality
- **Blog Management:** CRUD operations for blog posts
- **Article Handling:** Create and retrieve articles
- **File Uploads:** Support for file uploading and retrieval
- **Custom Exception Handling:** Tailored exceptions for business logic violations
- **RESTful API:** Well-structured API endpoints for all functionalities
- **Database Integration:** SQLAlchemy ORM with SQLite (easily extendable to other databases)

## Installation

### Prerequisites

- Python 3.10+ (Used Python 3.12.5 with all the latest Python packages. Use the mentioned versions for easier access.)
- pip (Python package manager)

### Clone the repository

```bash
git clone https://github.com/1666sApple/blogsite-FastAPI.git
cd blogsite-FastAPI
```

### Set up a virtual environment

It's recommended to use a virtual environment to keep the dependencies required by this project separate from your global Python environment.

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS and Linux:
source .venv/bin/activate
```

### Install dependencies

With the virtual environment activated, install the required Python packages:

```bash
pip install -r requirements.txt
```

### Set up the database

The project uses SQLAlchemy with SQLite by default. To set up a different database, modify `db/database.py`.

Create the database tables:

```bash
python main.py
```

### Running the server

Start the FastAPI server with:

```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Project Structure

```
blogsite-FastAPI/
│
├── main.py                 # Application entry point
├── schemas.py
├── exception.py
├── requirements.txt        # Project dependencies
├── .gitignore
├── .blog.db                # Database
├── LICENSE.md
│
├── auth/                   # Authentication related modules
│   ├── __init__.py
│   ├── auth.py
│   ├── oauth2.py
│   └── authentication.py
│
├── routers/                # API route definitions
│   ├── __init__.py
│   ├── blog_get.py
│   ├── blog_post.py
│   ├── article.py
│   ├── user.py
│   └── file.py
│
├── db/                     # Database models and connection
│   ├── __init__.py
│   ├── database.py
│   ├── db_article.py
│   ├── db_fileupload.py
│   ├── db_user.py
│   ├── hash.py
│   └── models.py
│
└── Files/              # Custom File Upload
```

## API Endpoints

### Authentication
- `POST /auth/login`: User login
- `POST /auth/signup`: User registration

### User Management
- `GET /user/{id}`: Retrieve user details

### Blog Management
- `GET /blogs`: List all blog posts
- `POST /blogs`: Create a new blog post
- `GET /blogs/{id}`: Retrieve a specific blog post
- `PUT /blogs/{id}`: Update a blog post
- `DELETE /blogs/{id}`: Delete a blog post

### Article Management
- `GET /articles`: List all articles
- `POST /articles`: Create a new article
- `GET /articles/{id}`: Retrieve a specific article

### File Handling
- `POST /upload`: Upload a file
- `GET /files/{filename}`: Retrieve a file

## Custom Exceptions

- `StoryException`: Handles story-related violations (Status Code: 418)
- `TermsViolationException`: Manages terms and conditions violations (Status Code: 403)

## Contributing

We welcome contributions to the Blogsite FastAPI project! Here's how you can contribute:

1. **Fork the Repository:** Create your own fork of the project.

2. **Create a Feature Branch:** `git checkout -b feature/AmazingFeature`

3. **Make Your Changes:** Implement your feature or bug fix.

4. **Run Tests:** Ensure your changes don't break existing functionality.

5. **Commit Your Changes:** `git commit -m 'Add some AmazingFeature'`

6. **Push to the Branch:** `git push origin feature/AmazingFeature`

7. **Open a Pull Request:** Submit your changes for review.

### Contribution Guidelines

- Follow PEP 8 style guide for Python code.
- Write meaningful commit messages.
- Update documentation for any new features or changes in functionality.
- Add appropriate unit tests for new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI for the excellent web framework
- SQLAlchemy for powerful ORM capabilities
- All contributors who have helped shape this project

For any questions or support, please open an issue on the GitHub repository.