# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in pyproject.toml
RUN pip install --no-cache-dir .

# Run cicd-test when the container launches
CMD ["cicd-test"]