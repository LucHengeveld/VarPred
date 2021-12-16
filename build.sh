#!/bin/sh
echo Building ml-container

cd ml_scripts/

docker build -t ml/python:1.0 .

cd ..

docker run -e assembly="37" --name ml-container-37 ml/python:1.0

docker run -e assembly="38" --name ml-container-38 ml/python:1.0

echo Copying JSON seed 37

docker cp ml-container-37:variant-37.json database/variant-37.json

echo Copying JSON seed 38

docker cp ml-container-38:variant-38.json database/variant-38.json

echo build web, mongodb and mongoseed

docker-compose up
