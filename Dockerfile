# Use the official Python image as a base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the local code to the container
COPY . .

# Install project dependencies
RUN pip install -r requirements.txt

# Expose the port your app will run on
EXPOSE 5000

# Command to run your application
CMD ["python", "app.py"]
