#!/bin/bash
docker build -t search-analytics-api:0.0.1 .
docker stop search-analytics-api-container
docker rm search-analytics-api-container
docker run -d  --name search-analytics-api-container -p 8080:8080 -v /Users/elshaddhai/my_works/search-analytics/api:/usr/src/app/api search-analytics-api:0.0.1