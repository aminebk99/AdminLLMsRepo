#!/bin/sh

# Create the Docker network if it does not exist
# docker network inspect llm_network || docker network create llm_network

# Start the Docker daemon
dockerd &

# Wait for the Docker daemon to initialize (adjust the sleep time as needed)
sleep 5

# Run the Python application
python3 app.py