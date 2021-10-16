#!/bin/bash
USER=test
ROOT_PWD=rootsql
docker run --name baking-pytest --rm -d -e MYSQL_ROOT_PASSWORD=$ROOT_PWD -e MYSQL_USER=$USER -e MYSQL_PASSWORD=sql -p 3306:3306 mysql 

docker ps | grep baking | awk '{print $1}'
sleep 10
mysql -h 127.0.0.1 -u root -p$ROOT_PWD -e  "GRANT ALL PRIVILEGES ON *.* TO 'test'@'%';"
