#!/bin/bash

# PDF 대량 업로드 스크립트
# 사용법: ./bulk_upload.sh [소스_폴더] [사용자명]

SOURCE_FOLDER="$1"
USERNAME="${2:-eys632}"
UPLOAD_DIR="/home/ubuntu/media/uploads"

if [ -z "$SOURCE_FOLDER" ]; then
    echo "사용법: $0 <소스_폴더> [사용자명]"
    echo "예시: $0 /path/to/pdf/folder eys632"
    exit 1
fi

if [ ! -d "$SOURCE_FOLDER" ]; then
    echo "오류: 소스 폴더가 존재하지 않습니다: $SOURCE_FOLDER"
    exit 1
fi

echo "PDF 파일들을 $SOURCE_FOLDER 에서 $UPLOAD_DIR 로 복사합니다..."
echo "사용자: $USERNAME"
echo ""

# uploads 디렉토리가 없으면 생성
mkdir -p "$UPLOAD_DIR"

count=0
for file in "$SOURCE_FOLDER"/*.{pdf,PDF,txt,TXT,doc,DOC,docx,DOCX}; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        target="$UPLOAD_DIR/$filename"
        
        # 파일이 이미 존재하면 건너뛰기
        if [ -f "$target" ]; then
            echo "건너뜀: $filename (이미 존재)"
        else
            cp "$file" "$target"
            echo "복사됨: $filename"
            ((count++))
        fi
    fi
done

echo ""
echo "총 $count 개 파일이 복사되었습니다."
echo ""
echo "이제 Django 관리 명령어를 실행하여 벡터 데이터베이스에 추가합니다..."

# Django 관리 명령어 실행
cd /home/ubuntu
source myenv/bin/activate
python manage.py bulk_upload "$UPLOAD_DIR" --user "$USERNAME"

echo "완료!"
