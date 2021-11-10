#!/bin/bash


#DB 
echo "Running migration..."
export CONFIG_NAME=""


cd ./baking
alembic upgrade head


echo "starting!!"