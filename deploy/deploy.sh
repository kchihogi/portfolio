#!/bin/bash
rsync -acvz --delete ./deploy/ $USER@$HOST:/workspace
ssh $USER@$HOST "date > /workspace/log.txt"
ssh $USER@$HOST "docker-compose -v >> /workspace/log.txt"
ssh $USER@$HOST "cp /env/.env /workspace/.env"
ssh $USER@$HOST "cd /workspace; docker-compose up -d;"
ssh $USER@$HOST "date >> /workspace/log.txt"
