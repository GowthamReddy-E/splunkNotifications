#!/bin/bash

# Define the image name
IMAGE_NAME="data_digger_bot_image"

# Build the Docker image using Dockerfile.bot
echo "Building the Docker image using Dockerfile.bot..."
docker build -f Dockerfile.bot -t ${IMAGE_NAME} . > /dev/null 2>&1

# Check if the build was successful
if [ $? -eq 0 ]; then
    echo "Docker image ${IMAGE_NAME} built successfully."
else
    echo "Failed to build Docker image."
    exit 1
fi

# Run the Docker container in detached mode
echo "Running the Docker container in detached mode..."
docker run -d --name my_bot_container ${IMAGE_NAME} > /dev/null 2>&1

sleep 10
# Check if the container was started successfully
if [ $? -eq 0 ]; then
    echo "Docker container my_bot_container is running in detached mode."
else
    echo "Failed to run Docker container."
    exit 1
fi

echo "Done!"