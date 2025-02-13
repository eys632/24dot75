# 24dot75 프로젝트

## 프로젝트 개요
Django 기반 웹 애플리케이션으로, **챗봇 인터페이스**를 제공하여 사용자가 대화 기록을 관리하고, 파일을 업로드하여 정보를 검색할 수 있도록 지원. LangChain과 Upstage의 embedding 모델을 활용하여 데이터를 벡터화하고, 이를 기반으로 질문에 대한 응답을 생성하는 기능을 포함하고 있음음.

## 주요 기능
### 1. **사용자 인증 시스템**
- Django의 `auth` 시스템을 활용하여 로그인/회원가입/로그아웃 기능을 제공
- 관리자(Admin) 계정 요청 기능 포함

### 2. **챗봇 기능**
- 대화 이력을 관리하고, 저장된 대화를 불러와 이어서 대화 가능
- Django의 `StreamingHttpResponse`를 활용하여 실시간 응답을 지원
- LangChain 기반 문서 검색 및 AI 응답 기능 제공

### 3. **PDF 문서 분석 및 검색**
- 사용자가 업로드한 PDF 파일의 텍스트를 추출하여 벡터 DB 저장
- Upstage `solar-embedding-1-large-passage` 모델을 이용한 문서 검색 및 분석 기능 제공
- LangChain을 이용한 질의 응답 시스템 구축

### 4. **관리자 페이지**
- 업로드된 파일 및 대화 기록을 관리할 수 있는 Django Admin 페이지 제공
- 관리자는 사용자의 PDF 파일을 직접 확인 가능

## 폴더 구조
```
24dot75/
├── apps/                # Django 앱 (board, user 포함)
│   ├── board/           # 챗봇 기능을 담당하는 앱
│   ├── user/            # 사용자 인증 관련 앱
├── config/              # Django 프로젝트 설정
├── pdf_processed/       # PDF 처리 및 LangChain 관련 코드
├── static/              # 정적 파일 (CSS, JS, 이미지)
├── templates/           # HTML 템플릿 파일
├── media/               # 업로드된 PDF 파일 저장 경로
├── chroma_langchain_db/ # LangChain 벡터 데이터 저장소
├── db.sqlite3           # SQLite 데이터베이스 파일
├── manage.py            # Django 관리 명령어 실행 파일
├── requirements.txt     # 프로젝트 의존성 패키지 목록
├── .env                 # 환경 변수 설정 파일
├── README.md            # 프로젝트 개요 및 설명 (현재 파일)
```

## 설치 및 실행 방법
### 1. **필요 패키지 설치**
```bash
pip install -r requirements.txt
```

### 2. **환경 변수 설정**
`.env` 파일을 생성하고 다음과 같이 설정합니다:
```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*
```

### 3. **마이그레이션 및 서버 실행**
```bash
python manage.py migrate
python manage.py runserver
```

### 4. **관리자 계정 생성 (옵션)**
```bash
python manage.py createsuperuser
```

## chromadb와 sqlite 버전 오류 해결 방법
1. manage.py파일에 아래 코드 추가
```python
import pysqlite3
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
import sqlite3
print("현재 sqlite3 버전:", sqlite3.sqlite_version)  # 버전 확인용
```
2. 위 방법으로 해결 안될 시 삭제 후 재설치
```bash
pip uninstall pysqlite3
```
pysqlite3 제거를 위해 **y**입력 

```bash
pip install pysqlite3-binary
```

## API 엔드포인트
| HTTP Method | URL 패턴 | 설명 |
|------------|----------|------|
| GET | `/` | 로그인 페이지로 리다이렉트 |
| GET | `/board/chat/` | 챗봇 메인 페이지 |
| POST | `/board/stream_answer/` | 질문을 AI 모델에 전달하고 응답 받기 |
| POST | `/board/upload_file/` | PDF 파일 업로드 |
| GET | `/admin/` | Django Admin 페이지 |

## 기술 스택
- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, Bootstrap
- **AI Model**: LangChain, Upstage Embeddings (`solar-embedding-1-large-passage`)
- **Database**: SQLite, ChromaDB (Vector Storage)

