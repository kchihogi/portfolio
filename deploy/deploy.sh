#!/bin/bash
rsync -acvz --delete ./deploy/ $USER@$HOST:/workspace
ssh $USER@$HOST "date > /workspace/log.txt"
ssh $USER@$HOST "docker-compose -v >> /workspace/log.txt"
ssh $USER@$HOST "cp /env/.env /workspace/.env"
ssh $USER@$HOST "cd /workspace; docker system prune -f; docker-compose pull; docker-compose up -d --force-recreate;"
ssh $USER@$HOST "date >> /workspace/log.txt"
