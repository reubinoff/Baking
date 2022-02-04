#!/bin/bash


#DB 
# echo "hello $db_host"
# while ! pg_isready 
# do
#     echo "$(date) - waiting for database to start"
#     sleep 10
# done
echo "Running migration..."


cd ./baking
# alembic upgrade head


echo "starting!!"