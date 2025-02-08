from sign_in import login_user
from admin_features import create_user, delete_user, approve_admin_request, manage_database, get_admin_request_list
from user_features import ask_chatbot, request_admin_access
import sqlite3
import os

DB_PATH = os.path.join("data", "users.db")

def user_dashboard(username):
    """
    일반 사용자(user) 전용 기능
    """
    print(f"\n[유저 기능] {username}님, 사용할 기능을 선택하세요:")
    print("1. 챗봇에게 질문하기")
    print("2. 관리자 권한 요청")
    
    choice = input("선택: ")
    if choice == "1":
        question = input("챗봇에게 질문: ")
        ask_chatbot(question)
    elif choice == "2":
        request_admin_access(username)

def admin_dashboard(username):
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

def super_admin_dashboard(username):
    """
    슈퍼 관리자(super_admin) 전용 기능 (admin과 동일한 권한)
    """
    print(f"\n[슈퍼 관리자 기능] {username}님, 사용할 기능을 선택하세요:")
    admin_dashboard(username)  # 슈퍼 관리자는 관리자 기능을 모두 수행 가능

def access_control(username, password):
    """
    로그인 후, 유저 권한에 따라 적절한 기능을 실행하는 함수
    """
    role = login_user(username, password)

    if role == "super_admin":
        print(f"\n환영합니다, {username}님. 슈퍼 관리자 권한이 확인되었습니다.")
        super_admin_dashboard(username)
    elif role == "admin":
        print(f"\n환영합니다, {username}님. 관리자 권한이 확인되었습니다.")
        admin_dashboard(username)
    elif role == "user":
        print(f"\n환영합니다, {username}님. 일반 사용자 권한이 확인되었습니다.")
        user_dashboard(username)
    else:
        print("로그인 실패. 접근 권한이 없습니다.")

if __name__ == "__main__":
    username = input("아이디 입력: ")
    password = input("비밀번호 입력: ")
    access_control(username, password)
