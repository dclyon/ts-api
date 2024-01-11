# ts-api readme
DOCKER: docker run -p 5000:5000 <docker image>


Getting Started:

- From the terminal, enter:
> curl -k -X POST https://localhost:443/login -H "Content-Type: application/json" -d '{"username":"user1", "password":"password1"}'

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
> curl -X GET https://localhost:443/primarygroup?user=alfred -H "Authorization: Bearer $ACCESS_TOKEN"
- command breakdown:
1. -X GET: Specifies that this is a GET request.
2. .../primarygroup?user=alfred: Indicates the primarygroup route and takes a user argument (alfred is in the example database)
3. -H "Authorization: Bearer $ACCESS_TOKEN": Indicates that you are passing a custom authorization header along with access token.

