import sqlite3
import os
import sys

# 현재 파일(UserDB_Create.py)의 상위 폴더를 기준으로 "access" 폴더를 import 경로에 추가
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 24dot75 폴더 경로
ACCESS_DIR = os.path.join(BASE_DIR, "access")  # access 폴더 경로
sys.path.append(ACCESS_DIR)  # Python import 경로에 추가

from sign_in import hash_password  # import 가능

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

    # users 테이블 생성 (슈퍼 관리자 계정 추가)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('user', 'admin', 'super_admin')) NOT NULL
    )
    """)

    # 슈퍼 관리자 존재 여부 확인
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'super_admin'")
    super_admin_exists = cursor.fetchone()[0]

    # 슈퍼 관리자가 존재하지 않으면 생성
    if super_admin_exists == 0:
        cursor.execute("""
        INSERT INTO users (username, password, role) 
        VALUES (?, ?, ?)
        """, ("superadmin", hash_password("super_secure_password"), "super_admin"))
        print("슈퍼 관리자 계정(superadmin)이 생성되었습니다.")

    conn.commit()
    conn.close()
    print(f"SQLite 데이터베이스가 '{DB_PATH}' 에 생성되었습니다.")

if __name__ == "__main__":
    initialize_database()
