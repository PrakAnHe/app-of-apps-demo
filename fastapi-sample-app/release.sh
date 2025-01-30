#!/bin/bash

RANDOM_TAG=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 13; echo)

echo Building...
docker build -t fastapi-sample-app:$RANDOM_TAG .

echo Pushing to $RANDOM_TAG
docker tag fastapi-sample-app:$RANDOM_TAG prakahe/fastapi-sample-app:$RANDOM_TAG
docker push prakahe/fastapi-sample-app:$RANDOM_TAG

echo Pushing to latest
docker tag fastapi-sample-app:$RANDOM_TAG prakahe/fastapi-sample-app:latest
docker push prakahe/fastapi-sample-app:latest

echo "Updating app.yaml with new image tag: $RANDOM_TAG ..."
sed -i "s|image: prakahe/fastapi-sample-app:.*|image: prakahe/fastapi-sample-app:$RANDOM_TAG|g" .ao/k8s/app.yaml

echo "Committing app.yaml..."
git add .ao/k8s/app.yaml
git commit -m "Update image tag to $RANDOM_TAG"
git push origin main
