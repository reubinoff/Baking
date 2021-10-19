#!/bin/bash
USER=postgres
ROOT_PWD=rootsql
docker run --name baking-pytest --rm -d -e POSTGRES_PASSWORD=$ROOT_PWD  -p 5432:5432 postgres 

# docker ps | grep baking | awk '{print $1}'
# sleep 10
# mysql -h 127.0.0.1 -u root -p$ROOT_PWD -e  "GRANT ALL PRIVILEGES ON *.* TO 'pytest_db_user'@'%';"
