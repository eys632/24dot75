# User권한에서 가능한 기능을 함수에 구현
import sqlite3
import os

DB_PATH = os.path.join("data", "users.db")

def ask_chatbot(question):
    """
    유저가 챗봇에게 질문을 할 수 있는 기능
    """
    print(f"챗봇 응답: {question}에 대한 답변을 준비 중입니다...")

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
