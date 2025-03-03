#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <Dockerfile name> <Image name>"
    exit 1
fi

DOCKERFILE=$1
IMAGE_NAME=$2

RANDOM_TAG=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 13; echo)

echo Building...
docker build -t $IMAGE_NAME:$RANDOM_TAG -f $DOCKERFILE .

echo Pushing to $RANDOM_TAG
docker tag $IMAGE_NAME:$RANDOM_TAG prakahe/$IMAGE_NAME:$RANDOM_TAG
docker push prakahe/$IMAGE_NAME:$RANDOM_TAG

echo Pushing to latest
docker tag $IMAGE_NAME:$RANDOM_TAG prakahe/$IMAGE_NAME:latest
docker push prakahe/$IMAGE_NAME:latest
