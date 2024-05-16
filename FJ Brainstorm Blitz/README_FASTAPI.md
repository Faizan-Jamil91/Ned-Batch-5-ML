Authentication and MCQ Generation Service
This service provides authentication functionalities such as user registration, login, and token generation, alongside the capability to generate multiple-choice questions (MCQs) and evaluate user-provided answers.

Features
User Registration: Allows users to register by providing a unique username, email, and password. Passwords are securely hashed using bcrypt.

User Authentication: Registered users can authenticate themselves using their username and password.

Token Generation: Upon successful authentication, users receive a JSON Web Token (JWT) for subsequent authorized requests. Tokens have a configurable expiration time.

MCQ Generation: The service can generate MCQs based on user-provided topics. It utilizes Google's Generative AI for content generation.

Result Evaluation: Users can provide answers to the generated MCQs, and the service evaluates these answers to provide a summarized result.

Setup and Configuration

Install Dependencies:

bash
Copy code
poetry install
Configure the Service:

Database Connection: Set the DATABASE_URL variable in auth.py with your actual database connection string.
Secret Key: Replace the SECRET_KEY variable with a securely generated key for JWT token generation.
Token Expiration Time: Adjust the TOKEN_EXPIRATION variable to set the expiration time for JWT tokens.
Salt Rounds: Set the SALT_ROUNDS variable to define the number of salt rounds for bcrypt hashing.
Google Generative AI API Key: Replace the API key in the ContentGenerator class with your Google Generative AI API key.
Usage
Run the Service:

bash
Copy code
poetry run uvicorn auth:app --reload
Explore API Documentation:

Access the API documentation at http://localhost:8000/docs in your browser to explore available endpoints and test the functionality.

Endpoints
Register User: POST /register/

Accepts username, password, password confirmation, and email.
Returns a success message upon successful registration.
Login: POST /login/

Accepts username and password.
Returns a JWT token upon successful authentication.
Generate MCQs: POST /generate_mcqs/

Accepts a topic input.
Generates multiple-choice questions based on the provided topic.
Generate Result: POST /generate_result/

Accepts the result string and collected answers.
Evaluates the provided answers against the correct ones and returns a summarized result.
Dependencies
FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.
SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
bcrypt: A password hashing library for Python.
PyJWT: A library for encoding and decoding JSON Web Tokens (JWT).
Google Generative AI: A powerful text generation model from Google.
Contributors
Your Name
License
This project is licensed under the MIT License - see the LICENSE file for details