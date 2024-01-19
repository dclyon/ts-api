## Flask API with Apache Reverse Proxy Setup Guide

This guide will walk you through setting up a simple Flask API with an Apache reverse proxy using Docker. This setup ensures that your API is accessible via HTTPS.
Prerequisites

Before you begin, ensure you have the following installed on your system:

    Docker
    Docker Compose
    Git

## Getting Started

Follow these steps to get your API up and running:
1. Clone the Repository

First, clone the project repository to your local machine. This repository contains the necessary Dockerfiles and configuration files.



>git clone https://github.com/dclyon/ts-api.git
> 
>cd ts-api

2. Switch to the Correct Branch

If you need to switch to a specific branch (e.g., containerize), run the following command:

>git checkout containerize

3. Build and Run the Containers

Navigate to the project root directory (where docker-compose.yml is located) and run the following command to build and start the Docker containers:


>docker-compose up --build

This command builds the Docker images for the Flask app and Apache server and starts the containers.
4. Accessing the API

Once the containers are up and running, you can access the API through your web browser or using tools like curl:

    Web Browser: Go to https://localhost (or https://localhost:8443 if a custom HTTPS port is used).
    Curl Command: You can use a command like curl -k https://localhost to test the API.

Note: The -k flag in curl is used to bypass SSL certificate verification, which might be necessary if you're using self-signed certificates.
5. Stopping the Containers

To stop the running containers, use the following command:

docker-compose down


## Additional Information

The Flask app runs in its own container and is proxied through the Apache server for HTTPS.
    The Apache server is configured as a reverse proxy to forward requests to the Flask app.
    SSL configuration in Apache requires valid SSL certificates and keys.

## Using the API

- From the terminal, enter:
> curl -k -X POST https://localhost:8443/login -H "Content-Type: application/json" -d '{"username":"user1", "password":"password1"}'

command breakdown:
1. -k -X POST: Specifies to accept insecure connection (to avoid self signed SSL cert err) and that  this is a POST request.
2. -H "Content-Type: application/json": Sets the Content-Type header to application/json to indicate that the request body is a JSON object
3. -d '{"username":"user1", "password":"password1"}': Provides requested data (username/password) as a JSON object. (user1 and password1 are valid login credentials)

- After issuing the above command you will be met with a 269 character access token which expires after 1 day, a refresh token (30 days), and an available routes list (shown below).
```

'/protected: 'Access to protected page' (for testing purposes)
'/api/items: 'Get or add items' (will work once DB created)
'/logs': 'View logs' (working, protected)
'/groups': 'View groups' (working, protected)
'/primarygroup': 'Get primary group for a user' (working, protected)
'/token/refresh': 'Refresh your access token' (working, protected)

```
- You can store your access token in an env variable by issuing the following command:
> export ACCESS_TOKEN='your-access-token'
- The following command is an example of using the curl command to access a protected route:
> curl -X GET https://localhost:8443/primarygroup?user=alfred -H "Authorization: Bearer $ACCESS_TOKEN"
- command breakdown:
1. -X GET: Specifies that this is a GET request.
2. .../primarygroup?user=alfred: Indicates the primarygroup route and takes a user argument (alfred is in the example database)
3. -H "Authorization: Bearer $ACCESS_TOKEN": Indicates that you are passing a custom authorization header along with access token.

