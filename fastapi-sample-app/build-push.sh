#!/bin/bash

echo "Building..."
docker build -t fastapi-sample-app .

echo "Tagging..."
docker tag fastapi-sample-app:latest prakahe/fastapi-sample-app:latest

echo "Pushing..."
docker push prakahe/fastapi-sample-app:latest
