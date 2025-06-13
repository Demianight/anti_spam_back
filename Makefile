build: 
	docker build -t demianight/anti_spam_back:latest .
run:
	docker run --name anti_spam_back -e KAFKA_BROKER=62.113.119.235:30092 -e DB_HOST=host.docker.internal -e DB_DB=messages -e DB_USER=xc -e DB_PASSWORD=mypassword -p 8000:8000 demianight/anti_spam_back:latest
kill:
	docker rm -f anti_spam_back
push:
	docker push demianight/anti_spam_back:latest
prod:
	docker buildx build --platform linux/amd64 -t demianight/anti_spam_back:latest --push .
test_db:
	docker run --rm --name pg-test -e POSTGRES_DB=messages -e POSTGRES_USER=xc -e POSTGRES_PASSWORD=mypassword -p 5432:5432 postgres:15
