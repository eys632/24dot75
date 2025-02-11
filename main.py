import os
import sqlite3
from access.sign_in import register_user, login_user
from pdf_processed.database_process import select_docs, create_vector_store
from pdf_processed.llm_process import generate_response
from access.user_features import save_chat_log

# 데이터베이스 경로 설정
USER_DB_PATH = "data/users.db"
CHAT_DB_PATH = "data/chat_history.db"
CHROMA_DB_PATH = "pdf_processed/chroma_langchain_db"

# 벡터 저장소 초기화
db = create_vector_store(collection_name="document_embeddings", db_path=CHROMA_DB_PATH)

def main():
    """
    전체 시스템 실행 함수
    """
    print("\n[회원가입 및 로그인]")
    
    # 사용자 회원가입 또는 로그인
    while True:
        action = input("회원가입(r) 또는 로그인(l)을 선택하세요: ").strip().lower()
        if action == "r":
            user_id = input("아이디: ").strip()
            user_pw = input("비밀번호: ").strip()
            register_user(user_id, user_pw, "user")
        elif action == "l":
            user_id = input("아이디: ").strip()
            user_pw = input("비밀번호: ").strip()
            user, role = login_user(user_id, user_pw)
            if user:
                print(f"{user_id}님, 로그인 성공!")
                break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")
    
    # 질문 처리 루프
    while True:
        question = input("질문을 입력하세요 (종료하려면 'exit' 입력): ").strip()
        if question.lower() == "exit":
            print("프로그램을 종료합니다.")
            break
        
        # LLM을 이용해 질문을 재해석하고 적절한 문서를 검색
        retrieved_docs = select_docs(db, question)
        response, _ = generate_response(db, question)
        
        # 결과 저장
        save_chat_log(user_id, question, response)
        
        # 응답 출력
        print("\n[챗봇 응답]")
        print(response)
        print("------------------------------------")

if __name__ == "__main__":
    main()
