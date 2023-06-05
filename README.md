# Octal Educators Blog (Django Version)

Welcome to the Django backend for the Octal Educators Website project. This backend is responsible for handling all the server-side functionality and API endpoints required for our website.

## Getting Started

To get started with the project, follow these steps:

1; clone the repository :

'git clone https://github.com/Octal-Ideas/octal_educators_backend_django.git'

2; Change into the project directory:

cd octal_educators_backend_django

3; Create and activate a virtual environment

python3 -m venv env
source env/bin/activate

4; Install the project dependencies:

pip install -r requirements.txt

5; Apply the database migrations:

python manage.py migrate

6; Run the development server:

python manage.py runserver

The backend server should now be running at 'http://localhost:8000/'

## API Endpoints

- `admin/`: The default Django admin site. Used to manage the site's backend.
- `api/v1/`: The base URL for all API endpoints.
- `token/`: Endpoint for obtaining an access and refresh token. Used to authenticate and authorize API requests. To test, make a POST request to this endpoint with a valid username and password in the request body. The response should include a JSON object containing the access and refresh tokens.
- `token/refresh/`: Endpoint for refreshing an access token. Used to extend the lifetime of an access token. To test, make a POST request to this endpoint with a valid refresh token in the request body. The response should include a JSON object containing a new access token.
- `api/v1/users/`: Endpoint for listing all registered users. To test, make a GET request to this endpoint with a valid access token in the `Authorization` header. The response should include a JSON object containing a list of user objects.
- `api/v1/blogs/`: Endpoint for viewing all blogs. To test, make a GET request to this endpoint with a valid access token in the `Authorization` header. The response should include a JSON object containing a list of blog objects.

Please refer to the source code and documentation within each app for detailed information about the available API endpoints and their usage.

## Contributing

If you would like to contribute to this project, please follow these guidelines:

1; Fork the repository and clone it locally.

2; Create a new branch for your feature/bug fix.

3; Make your changes and test thoroughly.

4;Commit your changes with clear and concise commit messages.

5; Push your branch to your forked repository.

6; Submit a pull request from your branch to the main repository.

7; Provide a detailed description of your changes and the problem they solve.

8; Ensure your code follows the project's coding conventions and style guidelines.

9; Respond to any feedback or code review comments promptly and make necessary updates.

Please note that all contributions are subject to review and approval by the project maintainers. Your cooperation and adherence to these guidelines will help ensure a smooth and efficient contribution process.

## Issues and Bug Reports

If you encounter any issues or bugs while using the Octal Educators Website Django backend, please report them on the project's issue tracker. Provide a clear and detailed description of the problem, along with any relevant information or steps to reproduce the issue. This will help us identify and resolve the problem more effectively.

## License

The Octal Educators Website Django backend is released under the MIT License. 

## Contact

If you have any questions, suggestions, or feedback related to the backend, feel free to reach out to the us:

Email: [octalideas@gmail.com]