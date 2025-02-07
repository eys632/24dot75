from sign_in import login_user
import sqlite3
import os

DB_PATH = os.path.join("data", "users.db")

def user_dashboard():
    """
    일반 유저(user) 전용 기능
    """
    print("일반 사용자 기능을 실행합니다.")

def admin_dashboard():
    """
    관리자(admin) 전용 기능
    """
    print("관리자 기능을 실행합니다.")

def super_admin_dashboard():
    """
    슈퍼 관리자(super_admin) 전용 기능
    """
    print("슈퍼 관리자 기능을 실행합니다.")
    print("이 계정은 삭제할 수 없으며, 시스템의 모든 권한을 가집니다.")

def access_control(username, password):
    """
    로그인 후, 유저 권한에 따라 적절한 기능을 실행하는 함수
    :param username: 사용자 아이디
    :param password: 비밀번호
    """
    role = login_user(username, password)

    if role == "super_admin":
        print(f"환영합니다, {username}님. 슈퍼 관리자 권한이 확인되었습니다.")
        super_admin_dashboard()
    elif role == "admin":
        print(f"환영합니다, {username}님. 관리자 권한이 확인되었습니다.")
        admin_dashboard()
    elif role == "user":
        print(f"환영합니다, {username}님. 일반 사용자 권한이 확인되었습니다.")
        user_dashboard()
    else:
        print("로그인 실패. 접근 권한이 없습니다.")

def delete_user(username):
    """
    특정 사용자를 삭제하는 기능 (슈퍼 관리자는 삭제 불가능)
    :param username: 삭제할 사용자 아이디
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 슈퍼 관리자 삭제 방지
    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result and result[0] == "super_admin":
        print("[오류] 슈퍼 관리자는 삭제할 수 없습니다.")
        conn.close()
        return

    # 일반 사용자 삭제
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    print(f"{username} 계정이 삭제되었습니다.")

if __name__ == "__main__":
    # 테스트 실행
    access_control("test_user", "1234")  # 일반 사용자 기능 실행
    access_control("admin_user", "admin1234")  # 관리자 기능 실행
    access_control("superadmin", "super_secure_password")  # 슈퍼 관리자 기능 실행

    # 삭제 테스트
    delete_user("test_user")  # 일반 사용자 삭제
    delete_user("superadmin")  # 슈퍼 관리자 삭제 (불가능)
