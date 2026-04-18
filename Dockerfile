# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run calculatoronline.py when the container launches
# Use gunicorn for production deployments
CMD ["gunicorn", "--bind", "0.0.0.0:80", "calculatoronline:app"]
