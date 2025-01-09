# article-batch-server
article &amp; batch service 가 존재하는 도메인입니다.
<br>
<br>
### 로컬 환경에서 article-server 실행하기

```
git clone https://github.com/nine-docs/article-batch-server.git
```

.env 파일을 루트 디렉토리에 추가하고 아래 명령어를 이용해 테스트 합니다.
```
docker build -t article-server . 
docker run --env-file .env -p 8000:8000 article-server 
```
