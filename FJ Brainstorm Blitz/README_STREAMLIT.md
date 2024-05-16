FJ Brainstorm Blitz
FJ Brainstorm Blitz is an interactive application built using Streamlit, providing users with the ability to generate multiple-choice questions (MCQs), answer them, and receive evaluated results. The application incorporates authentication functionalities for user login and registration to ensure secure access to its features.

Features
User Authentication: Users can securely login or register for an account to access the MCQ generation and result evaluation features.

MCQ Generation: Users can generate MCQs by entering a topic of interest. The application utilizes an external API to generate relevant MCQs dynamically.

Answer Submission: Users can provide answers to the generated MCQs directly within the application.

Result Evaluation: The application evaluates user-provided answers against the correct ones to generate a summarized result.


Install Dependencies:

bash
Copy code
poetry install
Run the Application:

bash
Copy code
poetry run streamlit run app.py
Explore the Interface:

Upon running the application, you'll be greeted with the FJ Brainstorm Blitz interface.
If you're not logged in, you'll be prompted to either login or register for an account.
After logging in or registering, you can generate MCQs by providing a topic of interest and clicking the "Generate MCQs" button.
Once the MCQs are generated, you can view them and submit your answers.
Finally, you can generate the result based on your submitted answers by clicking the "Generate result" button.
Dependencies
Streamlit: A Python library that allows you to create interactive web applications with simple Python scripts.
Requests: A Python library for making HTTP requests to external APIs.
Poetry: A dependency management tool for Python projects.
Contributors
Your Name
License
This project is licensed under the MIT License - see the LICENSE file for details.