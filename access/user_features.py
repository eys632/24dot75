# User 권한에서 가능한 기능을 함수에 구현
import sqlite3
import os
from datetime import datetime

# 데이터베이스 경로 설정
DB_PATH = os.path.join("data", "users.db")
CHAT_DB_PATH = os.path.join("data", "chat_history.db")  # 유저 질문/답변 저장 DB

def ask_chatbot(user_id, question):
    """
    유저가 챗봇에게 질문을 하면, 임시 응답을 생성하고 DB에 저장하는 기능.
    """
    # 임시 응답
    response = f"챗봇 응답: '{question}'에 대한 답변을 잘 할 수 있도록 공부하고 있습니다..."
    
    # 질문과 응답을 DB에 저장
    save_chat_log(user_id, question, response)

    # 응답 출력
    print(response)

def save_chat_log(user_id, query, response):
    """
    질문과 답변을 chat_history.db에 저장하는 함수
    """
    conn = sqlite3.connect(CHAT_DB_PATH)
    cursor = conn.cursor()

    # chat_logs 테이블이 없으면 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 데이터 삽입
    cursor.execute("INSERT INTO chat_logs (user_id, query, response) VALUES (?, ?, ?)",
                   (user_id, query, response))

    conn.commit()
    conn.close()

def request_admin_access(username):
    """
    유저가 관리자(admin) 권한을 요청하는 기능
    요청 사항을 DB에 저장하여 admin이 확인 가능하도록 함.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 요청을 따로 저장하는 테이블이 없다면 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL
    )
    """)

    try:
        cursor.execute("INSERT INTO admin_requests (username) VALUES (?)", (username,))
        conn.commit()
        print(f"{username}님이 관리자 권한을 요청했습니다.")
    except sqlite3.IntegrityError:
        print("이미 관리자 권한 요청이 진행 중입니다.")

    conn.close()

if __name__ == "__main__":
    # 테스트 실행
    ask_chatbot("user123", "오늘 날씨 어때?")
    ask_chatbot("user123", "내일 비와?")
