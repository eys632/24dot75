# access_control.py
from sign_in import login_user

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

def access_control(username, password):
    """
    로그인 후, 유저 권한에 따라 적절한 기능을 실행하는 함수
    :param username: 사용자 아이디
    :param password: 비밀번호
    """
    role = login_user(username, password)

    if role == "admin":
        print(f"환영합니다, {username}님. 관리자 권한이 확인되었습니다.")
        admin_dashboard()
    elif role == "user":
        print(f"환영합니다, {username}님. 일반 사용자 권한이 확인되었습니다.")
        user_dashboard()
    else:
        print("로그인 실패. 접근 권한이 없습니다.")

if __name__ == "__main__":
    # 로그인 후 기능 실행 테스트
    access_control("test_user", "1234")  # 일반 사용자 기능 실행
    access_control("admin_user", "admin1234")  # 관리자 기능 실행
    access_control("test_user", "wrongpass")  # 비밀번호 오류
    access_control("unknown_user", "1234")  # 존재하지 않는 유저
