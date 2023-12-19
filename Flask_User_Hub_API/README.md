Project Overview:
This Flask application provides user authentication and profile management functionalities. Users can register, log in, view and update profiles. 
The application ensures password security, uses JWT for authentication, and integrates Swagger UI for API documentation. 
The backend interacts with a MySQL database using SQLAlchemy.

FlaskAPI Project Setup:
This document provides step-by-step instructions for setting up and running a FlaskAPI project along with its dependencies. 
Ensure that you follow each step carefully.

## Getting Started

1. **Set up a Virtual Environment:-**
    - Create a virtual environment named `venv` using the command:- `python -m venv venv`.
    - Activate the virtual environment by running:- `venv\Scripts\activate`.
    - On macOS/Linux:- source `venv/bin/activate`


2. **Install Required Python Packages:-**
    - Install the necessary Python packages using pip. You can install all the required 
    - packages from the provided requirements.txt file:
    - `pip install -r requirements.txt`



3. **Configure File:-**
 - The file is used to configure various settings for your application. 
 - Replace the placeholders (**********) with actual values:

   - app.config['MAIL_SERVER'] = '**********'  # Your SMTP server
   - app.config['MAIL_PORT'] = ********** # Your SMTP server's port (587 for TLS)
   - app.config['MAIL_USERNAME'] = '**********'  # Your email username
   - app.config['MAIL_PASSWORD'] = '**********'  # Your email password
   - app.config['MAIL_DEFAULT_SENDER'] = 'Desired Name <**********>'  # Your default sender email
   - mail = Mail(app)

   # Configure your database connection URL
   - app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dbname'
     first create database on mysql and put the dbname on app.config


4. **Run the FlaskAPI Server**
 Start the FlaskAPI server using Uvicorn. You can use one of the following commands:
  1. For development with automatic reload:   flask run --reload



5. **Swagger API Documentation**
    The Swagger UI provides an interactive documentation interface for the API endpoints in this project.
    To access the Swagger documentation, follow these steps:
    
    1. Make sure the Flask application is running.
    2. Open a web browser.
    3. Enter the following URL in the address bar: http://127.0.0.1:5000/swagger
    4. You'll be redirected to the Swagger UI, displaying the API endpoints, their descriptions, and methods.
    5. Register the user using registerAPI and than login with valid credentials, you will get JWT token form login API , Put the Jwt     token on Authorize to get access permission. 


 These instructions should help you set up and run your FlaskAPI project with the required dependencies. 
 Make sure to follow each step carefully, 
 and ensure that your virtual environment is activated while working on the project.




