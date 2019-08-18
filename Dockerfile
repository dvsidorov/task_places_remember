# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install git -y
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN cd ./src

# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME places_remember

# Run app.py when the container launches
CMD cd ./src && DJANGO_SETTINGS_MODULE=config.dev python manage.py migrate && DJANGO_SETTINGS_MODULE=config.dev python manage.py runserver 0.0.0.0:8080