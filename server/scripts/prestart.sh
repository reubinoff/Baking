#!/bin/bash


#DB 
echo "Running migration..."

cd ./baking
alembic upgrade head


echo "starting!!"