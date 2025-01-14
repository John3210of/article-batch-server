#!/bin/bash

# 스크립트 실행 중 오류 발생 시 중단
set -e

# 1. Git에서 최신 코드 가져오기
echo "Pulling latest code from Git..."
git pull origin main

# 2. Docker 이미지 빌드
echo "Building Docker image..."
docker build -t article-server:latest .

# 3. 기존 컨테이너 중지 및 삭제
echo "Stopping and removing existing container..."
docker stop article-server || true
docker rm article-server || true

# 4. 새 컨테이너 실행
echo "Starting new container..."
docker run -d --name article-server --env-file .env -p 8000:8000 article-server:latest

# 완료 메시지
echo "Deployment completed successfully!"
