The aim of this project is to build a simple, light-weight environment for a basic Web API in Django.
The project features a light-weight development environment containerised with Docker. The reason of using docker-compose instead of just an image and one container is due to possible further expansion of the project.

1) cd into the root directory
2) copy the .env.dev file into a .env file
3) check the environment variables defined in the .env file and change them if needed
 3.1) the env file contains a port definition, this is the port from which you can reach the app from the host, mapped to the container's internal 8000 port
4) run the command docker-compose up --build from the root directory
5) you can now visit the webapp from your computer at localhost:DJANGO_PORT

EXAMPLE CURL: http://localhost:8080/convert/amount=10/src_currency=JPY/dest_currency=INR/reference_date=2020-02-14
