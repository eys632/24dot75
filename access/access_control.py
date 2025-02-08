from sign_in import login_user
from admin_features import create_user, delete_user, approve_admin_request, manage_database, get_admin_request_list
from user_features import ask_chatbot, request_admin_access
import sqlite3
import os
import hashlib

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "users.db"))

# 폴더가 없으면 자동 생성
if not os.path.exists(os.path.join(DB_PATH)):
    os.makedirs(os.path.join(DB_PATH, "data"))

def hash_password(password):
    """ 비밀번호를 SHA-256 방식으로 해싱 """
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_database():
    """
    데이터베이스가 존재하지 않을 경우 새로 생성
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # users 테이블이 없으면 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')

    # admin_requests 테이블이 없으면 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_requests (
            username TEXT PRIMARY KEY
        )
    ''')

    conn.commit()
    conn.close()

# 실행 시 데이터베이스 초기화 (테이블 없으면 생성)
initialize_database()

def register_user():
    """
    새 사용자를 데이터베이스에 등록하는 함수
    """
    print("\n[회원가입] 새 사용자 정보를 입력하세요.")
    username = input("아이디 입력: ").strip()
    password = input("비밀번호 입력: ").strip()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hash_password(password), "user"))
        conn.commit()
        print(f"\n[회원가입 완료] {username}님, 회원가입이 완료되었습니다! 자동으로 로그인됩니다.")
        conn.close()
        return username, password  # 회원가입 후 자동 로그인
    except sqlite3.IntegrityError:
        print("이미 존재하는 아이디입니다. 다른 아이디를 사용해주세요.")
        conn.close()
        return None, None  # 회원가입 실패

def user_dashboard(user_id, username):
    """
    일반 사용자(user) 전용 기능
    """
    print(f"\n[유저 기능] {username}님, 사용할 기능을 선택하세요:")
    print("1. 챗봇에게 질문하기")
    print("2. 관리자 권한 요청")
    
    choice = input("선택: ")
    if choice == "1":
        question = input("챗봇에게 질문: ")
        ask_chatbot(user_id, question)
    elif choice == "2":
        request_admin_access(username)

def admin_dashboard(user_id, username):
    """
    관리자(admin) 전용 기능
    """
    print(f"\n[관리자 기능] {username}님, 사용할 기능을 선택하세요:")
    print("1. 유저 계정 생성")
    print("2. 유저 계정 삭제")
    print("3. 관리자 권한 요청 승인")
    print("4. DB 관리")

    choice = input("선택: ")
    if choice == "1":
        new_user = input("새 유저 아이디: ")
        new_pass = input("새 유저 비밀번호: ")
        create_user(new_user, new_pass)
    elif choice == "2":
        user_to_delete = input("삭제할 유저 아이디: ")
        delete_user(user_to_delete)
    elif choice == "3":
        admin_requests = get_admin_request_list()
        
        if not admin_requests:
            print("\n[알림] 현재 관리자 승격 요청을 한 유저가 없습니다.")
            return
        
        print("\n[관리자 승격 요청 목록]")
        for i, user in enumerate(admin_requests, 1):
            print(f"{i}. {user}")

        admin_candidate = input("\n관리자로 승격할 유저 아이디 (취소하려면 Enter 입력): ").strip()
        if admin_candidate:
            approve_admin_request(admin_candidate)
    elif choice == "4":
        manage_database()

def super_admin_dashboard(user_id, username):
    """
    슈퍼 관리자(super_admin) 전용 기능 (admin과 동일한 권한)
    """
    print(f"\n[슈퍼 관리자 기능] {username}님, 사용할 기능을 선택하세요:")
    admin_dashboard(username)  # 슈퍼 관리자는 관리자 기능을 모두 수행 가능

def access_control(username, password):
    """
    로그인 후, 유저 권한에 따라 적절한 기능을 실행하는 함수
    """
    user_id, role = login_user(username, password)

    if role == "super_admin":
        print(f"\n환영합니다, {username}님. 슈퍼 관리자 권한이 확인되었습니다.")
        super_admin_dashboard(user_id, username)
    elif role == "admin":
        print(f"\n환영합니다, {username}님. 관리자 권한이 확인되었습니다.")
        admin_dashboard(user_id, username)
    elif role == "user":
        print(f"\n환영합니다, {username}님. 일반 사용자 권한이 확인되었습니다.")
        user_dashboard(user_id, username)
    else:
        print("로그인 실패. 접근 권한이 없습니다.")

if __name__ == "__main__":
    print("\n[로그인 시스템]")
    print("1. 로그인")
    print("2. 회원가입")

    choice = input("선택: ").strip()
    
    if choice == "1":
        username = input("아이디 입력: ").strip()
        password = input("비밀번호 입력: ").strip()
        access_control(username, password)

    elif choice == "2":
        new_username, new_password = register_user()
        if new_username and new_password:
            access_control(new_username, new_password)  # 회원가입 후 자동 로그인
    else:
        print("[오류] 잘못된 입력입니다. 프로그램을 종료합니다.")
