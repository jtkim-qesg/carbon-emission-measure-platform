# carbon-emission-measure-platform
탄소배출 측정 서비스 백엔드 레포지터리 입니다.


## How to run
### Local
```[bash]
docker compose --env-file env/.env.development -f docker-compose/docker-compose.development.yml up --build
docker compose --env-file env/.env.development -f docker-compose/docker-compose.development.yml down
```

### Production (테스트 필요)
```[bash]
docker compose --env-file env/.env.production -f docker-compose/docker-compose.production.yml up --build
docker compose --env-file env/.env.production -f docker-compose/docker-compose.production.yml down
```



## Application Structure


## 개발환경 세팅 가이드
> "틀릴수 있음"

#### 1. Pre-Requirements
- OS: Windows 10 / 11 (Intel CPU)
- 관리자 권한
- PowerShell 7 이상 또는 Git Bash 추천


#### 2. Windows 가상화 설정 및 WSL2 활성화
##### 1. BIOS에서 가상화(Virtualization) 활성화
- 재부팅 시 BIOS 진입 (보통 F2, F10, DEL 등)
- `Intel VT-x (Virtualization Technology)` 또는 `Intel Virtualization Technology` → Enable


##### 2. **Windows 기능 켜기**
   - [Windows 키] → "Windows 기능 켜기/끄기" 검색
   - ✅ `가상 머신 플랫폼`
   - ✅ `Windows 하위 시스템용 Linux`

##### 3. WSL2 및 Ubuntu 설치
```[bash]
wsl --install
```
- 설치 후 재부팅
- 기본 Ubuntu 설치됨
- 이후 wsl --set-default-version 2 로 버전 2 설정
PC 재부팅 후 Docker Desktop 설치


#### 🐋 4. Docker Desktop 설치

- 공식 링크: https://www.docker.com/products/docker-desktop/
- 설치 시 WSL2 backend 옵션 체크
- Docker Desktop 실행 후 정상 동작 확인
  ```[bash]
	docker version
	docker info
  ```

#### 🔧 5. 필수 툴 설치
##### 1. Python 설치 (pyenv을 사용한 설치 권장)
**pyenv-win 설치**
```[bash]
git clone https://github.com/pyenv-win/pyenv-win.git %USERPROFILE%\.pyenv
setx PYENV %USERPROFILE%\.pyenv
setx PATH "%PYENV%\pyenv-win\bin;%PYENV%\pyenv-win\shims;%PATH%"
```
재시작 후:
```[bash]
pyenv install 3.11.9
pyenv global 3.11.9
```


#### 5. 프로젝트 Clone 및 의존성 설치
```[bash]
git clone https://github.com/jtkim-qesg/carbon-emission-measure-platform.git
cd carbon-emission-measure-platform
```

#### 6. 개발환경 세팅
- 아래 **[Setting - Local]** 파트 참고




## Setting
### Local
#### env 세팅
`(root)/env/.env.development` 세팅 필요

##### variables
- APP_PORT: 백엔드 localhost port
- DATABASE_URL
	- local machine database url
	- SQLALCHEMY 연결용
- SYNC_DATABASE_URL
	- local machine database url
	- alembic 데이터베이스 


### Production (테스트 필요)
#### Nginx 구성
1. Nginx 설치
```[bash]
sudo apt update
sudo apt install nginx -y
```

2. 방화벽 확인 (Ubuntu UFW 사용 시)
```[bash]
sudo ufw allow 'Nginx Full'
```

3. Nginx 리버스 프록시 설정
```[bash]
sudo nano /etc/nginx/sites-available/carbon
```
```[nginx]
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:8000;  # FastAPI Docker 앱
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
심볼릭 링크로 활성화:
```[bash]
sudo ln -s /etc/nginx/sites-available/carbon /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```


#### env 세팅
(root)/env/.env.production 세팅 필요

##### variables
- APP_PORT
	- 백엔드 실서버 port (22, 8000, 443, 80 중 1개)
	- 보안 그룹에서 위 포트 인바운드 허용했는지 확인
	
- DATABASE_URL
	- local machine database url
	- SQLALCHEMY 연결용
- SYNC_DATABASE_URL
	- local machine database url
	- alembic 데이터베이스


#### 배포
1. EC2 서버 준비 및 접속
2. EC2 서버에 Docker 설치
```[bash]
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
newgrp docker
```

3. 깃허브 레포지터리 연결 및 다운로드
```[bash]
sudo apt install git -y
git clone https://github.com/jtkim-qesg/carbon-emission-measure-platform.git
```

4. .env 파일 구성
[Production - variables] 참조


5. Docker 빌드 및 실행
```[bash]
cd carbon-emission-measure-platform
docker compose -f docker-compose/docker-compose.production.yml up -d --build
```

6. Uvicorn 외부 접근 설정 확인
Dockerfile.production 또는 docker-compose.production.yml에서 반드시 다음 옵션 확인
```[yaml]
command: poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
ports:
  - "8000:8000"
```

7. EC2 방화벽 열려 있는지 확인
AWS 콘솔 → EC2 → 보안그룹 → 8000, 443, 80 포트 허용 설정


8. 접속 테스트
브라우저에서 접속:
```[bash]
http://your-ec2-ip:8000/docs
```


## DB 테이블 변경/신규 테이블 추가 작업을 Alembic으로 반영하는 절차 (테스트 및 추가 수정 필요)
1. 로컬 개발 환경에서 Alembic 마이그레이션 준비
```[bash]
# 예: 새로운 모델 추가 or 수정 후
poetry run alembic revision --autogenerate -m "Add new table or modify column"
poetry run alembic upgrade head
```
> 이 단계에서 versions/ 폴더 아래 .py 마이그레이션 스크립트가 생성됩니다.

2. Git 에 반영
```[bash]
git add alembic/versions/*.py
git commit -m "Add alembic migration for new table"
git push origin main
```

3. EC2 서버에서 코드 pull
```
# SSH or Personal Access Token 접속 후
cd ~/carbon-emission-measure-platform
git pull origin main
```

4. Docker 컨테이너에서 Alembic 실행
4-1. 컨테이너에 접속
```[bash]
docker exec -it carbon-dev bash
```

4-2. Alembic 커맨드 실행
```[bash]
poetry run alembic upgrade head
```
✅ 정상적으로 실행되면 마이그레이션이 Local MySQL 서버 또는 RDS(MySQL) 실서버에 반영됩니다.

