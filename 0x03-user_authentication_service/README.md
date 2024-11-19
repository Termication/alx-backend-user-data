# Flask Guide: Working with API Routes, Cookies, Form Data, and HTTP Status Codes

##### A quick overview of how to perform the following tasks in a Flask application:

-Declare API routes
-Get and set cookies
-Retrieve request form data
-Return various HTTP status codes

#### Table of Contents

    Prerequisites
    Declaring API Routes
    Working with Cookies
        Setting Cookies
        Getting Cookies
    Retrieving Form Data
    Returning HTTP Status Codes
    Example Application

## Prerequisites

To follow this guide, ensure you have:

    Python installed (version 3.7 or later recommended)
    Flask installed:
```bash
    pip install flask
```
## Declaring API Routes

In Flask, routes define the URLs that the app responds to. To declare a route:
```python
from flask import Flask

app = Flask(__name__)

@app.route('/example', methods=['GET', 'POST'])
def example():
    return "Hello, World!"
```
    @app.route: Decorator used to bind a URL to a function.
    methods: Optional parameter specifying allowed HTTP methods (default is GET).

### Example:
```python
@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, GET request!"
```
## Working with Cookies
#### Setting Cookies

Use the Response object to set cookies.
```python
from flask import Flask, make_response

@app.route('/set-cookie')
def set_cookie():
    response = make_response("Cookie is set!")
    response.set_cookie('key', 'value', max_age=3600)  # Expires in 1 hour
    return response
```
#### Getting Cookies

Access cookies from the request object.
```python
from flask import request

@app.route('/get-cookie')
def get_cookie():
    value = request.cookies.get('key')
    return f"Cookie Value: {value}"
```
#### Retrieving Form Data

Use the request.form object to retrieve form data sent via POST.
```python
from flask import request

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')  # Retrieve form data
    return f"Form submitted with name: {name}"
```
    Accessing Form Data: Use request.form.get('key') for a specific field or request.form to access all fields.

#### Returning HTTP Status Codes

Flask provides an easy way to return custom HTTP status codes alongside responses.
```python
@app.route('/not-found')
def not_found():
    return "Resource not found", 404
```
    Common HTTP Status Codes:
        200 OK: Successful requests
        201 Created: Resource successfully created
        400 Bad Request: Invalid request
        401 Unauthorized: Authentication required
        404 Not Found: Resource not found
        500 Internal Server Error: Server-side error

#### Example Application

Here’s a complete example that combines all the above concepts:
```python
from flask import Flask, request, make_response

app = Flask(__name__)

# API Route
@app.route('/api', methods=['GET', 'POST'])
def api_route():
    if request.method == 'GET':
        return "This is a GET request"
    elif request.method == 'POST':
        data = request.form.get('data')
        return f"POST request received with data: {data}"

# Set Cookie
@app.route('/set-cookie')
def set_cookie():
    response = make_response("Cookie set!")
    response.set_cookie('username', 'flask_user', max_age=3600)
    return response

# Get Cookie
@app.route('/get-cookie')
def get_cookie():
    username = request.cookies.get('username', 'Guest')
    return f"Hello, {username}!"

# HTTP Status Code
@app.route('/error')
def error():
    return "Something went wrong", 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
```
#### How to Test

Start the Flask app:
```bash
python app.py
```
## Use a tool like Postman or curl to test the endpoints.

    API Route: GET /api or POST /api with form data.
    Cookies: Test /set-cookie and /get-cookie.
    HTTP Status Codes: Visit /error.
