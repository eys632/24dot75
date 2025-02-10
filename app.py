import streamlit as st
import sqlite3
import json
from access.sign_in import login_user, register_user
from pdf_processed.database_process import select_docs, create_vector_store
from pdf_processed.llm_process import generate_response
from access.user_features import save_chat_log

# 데이터베이스 설정
CHAT_DB_PATH = "data/chat_history.db"
CHROMA_DB_PATH = "pdf_processed/chroma_langchain_db"

# 벡터 저장소 초기화
db = create_vector_store(collection_name="document_embeddings", db_path=CHROMA_DB_PATH)

# Streamlit UI
st.set_page_config(page_title="AI 챗봇", layout="wide")

st.title("💬 AI 기반 챗봇")

# 로그인 & 회원가입 UI
st.sidebar.header("👤 로그인 / 회원가입")
user_id = st.sidebar.text_input("아이디")
user_pw = st.sidebar.text_input("비밀번호", type="password")
login_btn = st.sidebar.button("로그인")
register_btn = st.sidebar.button("회원가입")

if login_btn:
    user, role = login_user(user_id, user_pw)
    if user:
        st.sidebar.success(f"✅ {user_id}님, 로그인 성공!")
    else:
        st.sidebar.error("❌ 로그인 실패. 아이디 또는 비밀번호를 확인하세요.")

if register_btn:
    register_user(user_id, user_pw, "user")
    st.sidebar.success("✅ 회원가입 완료! 로그인하세요.")

# 질문 입력 UI
st.subheader("🤖 질문을 입력하세요")
question = st.text_input("질문 입력")

if st.button("질문하기"):
    if user_id:
        # ChromaDB에서 문서 검색
        retrieved_docs = select_docs(db, question)

        # LLM을 이용한 응답 생성
        response, _ = generate_response(db, question)

        # 응답 저장
        save_chat_log(user_id, question, response)

        # 응답 출력
        st.subheader("📌 AI 응답")
        try:
            # 응답 데이터 확인 후 JSON 변환 여부 결정
            if isinstance(response, str):
                response_data = json.loads(response)
            else:
                response_data = response

            # 질문 요약 출력
            if "question_summary" in response_data:
                st.markdown(f"**🔎 질문 요약:** {response_data['question_summary']['summary']}")

            # 주요 내용 출력
            if "answer" in response_data and "main_content" in response_data["answer"]:
                st.markdown("### 📌 주요 내용:")
                for idx, content in enumerate(response_data["answer"]["main_content"]):
                    st.markdown(f"**{idx + 1}.** {content}")

            # 결론 출력
            if "conclusion" in response_data:
                st.markdown(f"### 🔍 결론: {response_data['conclusion']['conclusion']}")

        except json.JSONDecodeError:
            st.write("🚨 AI 응답을 처리하는 중 오류가 발생했습니다.")

    else:
        st.warning("❗ 먼저 로그인해주세요.")
