import sqlite3
import os

# 데이터베이스 경로 설정
DB_PATH = os.path.join("data", "users.db")

def initialize_database():
    """
    SQLite 데이터베이스(data/users.db)를 생성하고,
    users 테이블을 생성하는 함수.
    """
    # data 폴더가 존재하지 않으면 생성
    if not os.path.exists("data"):
        os.makedirs("data")

    conn = sqlite3.connect(DB_PATH)  # data 폴더에 DB 저장
    cursor = conn.cursor()

    # users 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('user', 'admin')) NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print(f"SQLite 데이터베이스가 '{DB_PATH}' 에 생성되었습니다.")

if __name__ == "__main__":
    initialize_database()
