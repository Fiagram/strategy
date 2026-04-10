#!/bin/sh

docker run --name mongodb \
  -p 27017:27017 \
  -d mongodb/mongodb-community-server:8.0-ubi9-slim