import sqlite3
import os
from sign_in import hash_password

DB_PATH = os.path.join("data", "users.db")

def create_user(username, password):
    """
    새로운 user 계정을 생성하는 기능
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hash_password(password), "user"))
        conn.commit()
        print(f"유저 계정이 생성되었습니다. (아이디: {username})")
    except sqlite3.IntegrityError:
        print("이미 존재하는 아이디입니다.")

    conn.close()

def delete_user(username):
    """
    유저 계정을 삭제하는 기능 (슈퍼 어드민은 삭제 불가)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result and result[0] == "super_admin":
        print("[오류] 슈퍼 관리자는 삭제할 수 없습니다.")
        conn.close()
        return

    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    print(f"{username} 계정이 삭제되었습니다.")

    conn.close()

def approve_admin_request(username):
    """
    관리자(admin)가 user의 admin 요청을 승인하는 기능
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 요청한 유저가 실제로 존재하는지 확인
    cursor.execute("SELECT username FROM admin_requests WHERE username = ?", (username,))
    request_exists = cursor.fetchone()

    if not request_exists:
        print(f"{username}님의 관리자 권한 요청이 존재하지 않습니다.")
        conn.close()
        return

    # 유저 권한을 admin으로 변경
    cursor.execute("UPDATE users SET role = 'admin' WHERE username = ?", (username,))
    cursor.execute("DELETE FROM admin_requests WHERE username = ?", (username,))
    conn.commit()
    
    print(f"{username}님이 관리자로 승격되었습니다.")
    conn.close()

def manage_database():
    """
    관리자(admin)가 users.db를 확인할 수 있는 기능
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    print("\n=== 현재 유저 목록 ===")
    for user in users:
        print(user)

    conn.close()
