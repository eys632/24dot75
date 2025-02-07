import sqlite3
import hashlib
import os

DB_PATH = os.path.join("data", "users.db")

def hash_password(password):
    """
    입력된 비밀번호를 SHA-256 방식으로 해싱하여 반환
    """
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, role="user"):
    """
    새 사용자를 데이터베이스에 등록하는 함수
    :param username: 사용자 아이디
    :param password: 비밀번호 (해싱하여 저장)
    :param role: 사용자 권한 (기본값: user, 관리자는 admin)
    """
    if role == "super_admin":
        print("[오류] 슈퍼 관리자는 생성할 수 없습니다.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hash_password(password), role))
        conn.commit()
        print(f"계정이 생성되었습니다. (아이디: {username}, 권한: {role})")
    except sqlite3.IntegrityError:
        print("아이디가 이미 존재합니다.")

    conn.close()

def login_user(username, password):
    """
    사용자가 입력한 아이디와 비밀번호를 확인하여 로그인 처리
    :param username: 사용자 아이디
    :param password: 입력한 비밀번호 (DB의 해싱된 값과 비교)
    :return: 로그인 성공 여부 및 유저 권한 반환
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

# username이 존재하는지 확인
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        stored_password, role = result
        if stored_password == hash_password(password):
            print(f"로그인 성공. 아이디: {username}, 권한: {role}")
            return role  # user 또는 admin 반환
        else:
            print("비밀번호가 틀렸습니다.")
    else:
        print("존재하지 않는 아이디입니다.")

    return None  # 로그인 실패 시 None 반환

if __name__ == "__main__":
    # 테스트용 유저 추가
    print("\n[회원가입 테스트]")
    register_user("test_user", "1234", "user")  # 일반 사용자 생성
    register_user("admin_user", "admin1234", "admin")  # 관리자 계정 생성
    register_user("super_test", "password", "super_admin")  # 슈퍼 관리자 생성 방지 확인

    # 로그인 테스트
    print("\n[로그인 테스트]")
    login_user("test_user", "1234")  # 일반 유저 로그인
    login_user("admin_user", "admin1234")  # 관리자 로그인
    login_user("superadmin", "supersuper")  # 슈퍼 어드민 로그인
    login_user("test_user", "wrongpass")  # 비밀번호 틀림
    login_user("unknown_user", "1234")  # 존재하지 않는 유저

    # 슈퍼 관리자가 생성되었는지 확인
    print("\n[슈퍼 관리자 존재 여부 확인]")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'super_admin'")
    super_admin_exists = cursor.fetchone()[0]
    conn.close()

    if super_admin_exists > 0:
        print("슈퍼 관리자 계정이 존재합니다.")
    else:
        print("슈퍼 관리자 계정이 존재하지 않습니다. (오류 발생 가능)")
