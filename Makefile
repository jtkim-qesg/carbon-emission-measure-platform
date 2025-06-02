# 서비스 시작
dev-up:
	docker compose --env-file env/.env.development -f docker-compose/docker-compose.development.yml up --build

# 서비스 종료
dev-down:
	docker compose --env-file env/.env.development -f docker-compose/docker-compose.development.yml down

# 로그 보기용
# 지정한 컨테이너(carbon-dev)의 실시간 로그 출력을 봅니다. -f 옵션은 follow로, 로그가 계속 출력되도록 tail -f와 같은 동작입니다.
logs:
	docker logs -f carbon-dev

# 마이그레이션 명령
migrate:
	docker compose exec app alembic upgrade head

# 서비스 리소스 정리용
# docker-compose가 띄운 모든 컨테이너를 종료하고, 거기에 연결된 볼륨까지 같이 삭제합니다. (MySQL 데이터도 날아갈 수 있음)
down-volumes:
	docker compose --env-file env/.env.development -f docker-compose/docker-compose.development.yml down --volumes

# 서비스 재시작
restart:
	docker compose --env-file env/.env.development -f docker-compose/docker-compose.development.yml down && \
	docker compose --env-file env/.env.development -f docker-compose/docker-compose.development.yml up --build