#!/bin/bash

if docker-compose -p flask-cc-api-staging.proj down --rmi all >/dev/null 2>&1;then
	echo "Container and image removed."
else
	echo "Clean failed."
	exit 1
fi

if docker build -t flask_cc_api_staging . ;then
	echo "Build successfully."
else
	echo "Build failed."
	exit 1
fi

if docker-compose -p flask-cc-api-staging.proj up -d;then
	echo "Compose started successfully."
else
	echo "Compose started failed."
	exit 1
fi

sleep 8s

docker-compose -p flask-cc-api-staging.proj logs
