# article-batch-server
article &amp; batch service

### how to get local test
docker build -t article-server . 
docker run --env-file .env -p 8000:8000 article-server 