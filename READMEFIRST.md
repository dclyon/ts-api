Flask API Application README
Introduction

This README provides guidance on how to interact with the Flask-based API application locally using HTTP and Flask's built-in server. The application supports various endpoints for user authentication, item management, log retrieval, and group information.
Getting Started
Prerequisites

    Ensure you have Python 3 and Flask installed on your system.
    Install the required dependencies listed in requirements.txt.

Installation

    Install Dependencies:
    Run the following command to install the required Python packages:

    pip install -r requirements.txt


The requirements.txt file includes the following packages:



    black==23.11.0
    blinker==1.7.0
    click==8.1.7
    Flask==3.0.0
    Flask-JWT-Extended==4.5.3
    Flask-Login==0.6.3
    itsdangerous==2.1.2
    Jinja2==3.1.2
    jq==1.6.0
    MarkupSafe==2.1.3
    mod-wsgi==4.9.4
    mypy-extensions==1.0.0
    packaging==23.2
    pathspec==0.11.2
    platformdirs==4.0.0
    PyJWT==2.8.0
    tomli==2.0.1
    typing_extensions==4.8.0
    Werkzeug==3.0.1

Running the Application Locally

    Located in the /scripts directory, I have included token.sh which can be used to login to
    and interact with the API. Note that token.sh must be executed with the source command.

    If you prefer a more manual approach, continue below.

    Start the Flask application by running the following command in your terminal:


    python app.py

    This will start the application on http://localhost:5000.
    (Open another terminal window to begin entering curl commands.)

Authenticating and Obtaining Tokens

To authenticate and obtain access and refresh tokens:


    curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username":"user1", "password":"password1"}'

        -X POST: Specifies a POST request.
        -H "Content-Type: application/json": Sets the Content-Type header to application/json.
        -d '{"username":"user1", "password":"password1"}': Provides login credentials as a JSON object.

    After executing this command, you will receive an access token (valid for 1 day), a refresh token (valid for 30 days), and a list of available routes.

API Endpoints

The API provides the following endpoints:

    /protected: Access a protected page.
    /api/items: Get or add items.
    /logs: View logs.
    /groups: View groups.
    /primarygroup: Get the primary group for a user.
    /token/refresh: Refresh your access token.

Using the Access Token

    export ACCESS_TOKEN='your-access-token'



Accessing Protected Routes:
For example, to access the /primarygroup endpoint:



    curl -X GET http://localhost:5000/primarygroup?user=alfred -H "Authorization: Bearer $ACCESS_TOKEN"

        -X GET: Specifies a GET request.
        http://localhost:5000/primarygroup?user=alfred: The URL with the specific endpoint and user parameter.
        -H "Authorization: Bearer $ACCESS_TOKEN": Passes the access token in the authorization header.

