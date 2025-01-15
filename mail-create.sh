#!/bin/bash

# 스크립트 실행 중 오류 발생 시 중단
set -e

# 1. Git에서 최신 코드 가져오기
echo "Pulling latest code from Git..."
git pull origin main

# 2. Docker 이미지 빌드
echo "Building Docker image for batch job..."
docker build -f Dockerfile.mail.create -t batch-job-create:latest .

# 3. 기존 배치 작업 컨테이너 중지 및 삭제
echo "Stopping and removing existing batch container..."
docker stop article-batch || true
docker rm article-batch || true

# 4. 배치 작업 컨테이너 실행
echo "Running batch job container..."
docker run --rm --name article-batch --env-file .env batch-job-create:latest

# 완료 메시지
echo "Batch job executed successfully!"
