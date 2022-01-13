#!/bin/sh

#example: ./deployment/scrips/build.sh server reubinoff baking-service 0.0.1

DOCKER_FILE=$1
IMAGE_REGISTRY=$2
IMAGE_NAME=$3
IMAGE_VERSION=$4

echo "Docker file location: $DOCKER_FILE"

echo docker build $DOCKER_FILE -t $IMAGE_REGISTRY/$IMAGE_NAME:$IMAGE_VERSION
docker build $DOCKER_FILE -t $IMAGE_REGISTRY/$IMAGE_NAME:$IMAGE_VERSION

echo $?