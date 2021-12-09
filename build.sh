#!/bin/sh
echo Building ml-container

cd ML_scripts

docker build -t ml-/python:1.0 .

cd ..

docker run -e assembly="37" --name ml-container ml/python:1.0

docker run -e assembly="38" --name ml-container ml/python:1.0

docker cp ml-container:/database/variant-37.json database/variant-37.json

docker cp ml-container:/database/variant-38.json database/variant-38.json

docker-compose up