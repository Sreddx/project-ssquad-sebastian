#!/bin/bash

cd /root/project-ssquad-sebastian
git fetch && git reset origin/main --hard  
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build

