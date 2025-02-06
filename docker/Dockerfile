# Python 3.9 기반 이미지 사용
FROM python:3.9

# 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# 필요하면 시스템 패키지 설치 (예: gcc, libpq-dev 등)
# RUN apt-get update && apt-get install -y <패키지명>

# 로컬의 requirements.txt를 컨테이너에 복사 후 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 현재 프로젝트 코드 복사
COPY . .

# 실행할 기본 명령어 (예: main.py 실행)
CMD ["python", "main.py"]
