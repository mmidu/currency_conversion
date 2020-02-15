1) cd into the root directory
2) copy the .env.dev file into a .env file
3) check the environment variables defined in the .env file and change them if needed
 3.1) the env file contains a port definition, this is the port from which you can reach the app from the host, mapped to the container's internal 8000 port
4) run the command docker-compose up --build from the root directory
5) you can now visit the webapp from your computer at localhost:DJANGO_PORT
