import streamlit as st
import datetime
import requests
import sqlite3

# [보안] 로그인 기능
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True
    st.title("🔒 GEVIS 개인 보안 영역")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("접속"):
        if password == "1234": # 비밀번호
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("비밀번호가 일치하지 않습니다.")
    return False

if check_password():
    # 단계별 진행 상태 관리
    if 'stage' not in st.session_state:
        st.session_state.stage = 1

    now = datetime.datetime.now()
    st.title("☀️ GEVIS 데일리 리포트")
    st.subheader(f"오늘은 {now.year}년 {now.month}월 {now.day}일입니다.")

    # --- 1단계: 감사일기 섹션 ---
    st.markdown("---")
    st.markdown("### 🙏 오늘의 감사일기") # (3가지) 삭제 완료
    g1 = st.text_input("1. 감사한 일", key="g1", placeholder="첫 번째 감사를 적어주세요")
    g2 = st.text_input("2. 감사한 일", key="g2", placeholder="두 번째 감사를 적어주세요")
    g3 = st.text_input("3. 감사한 일", key="g3", placeholder="세 번째 감사를 적어주세요")

    if st.session_state.stage == 1:
        if st.button("작성완료", key="btn_g"): # 버튼명 변경
            if g1 and g2 and g3:
                st.session_state.stage = 2
                st.rerun()
            else:
                st.warning("내용을 모두 작성해 주세요.")

    # --- 2단계: 감사 코멘트 및 확언일기 섹션 ---
    if st.session_state.stage >= 2:
        st.success("✨ **오늘의 감사 코멘트**\n\n작은 감사가 본부장님의 하루를 바꿉니다. 정말 잘하고 계세요!")
        
        st.markdown("---")
        st.markdown("### 💪 오늘의 확언일기") # (3가지) 삭제 완료
        a1 = st.text_input("1. 오늘의 확언", key="a1", placeholder="첫 번째 확언을 적어주세요")
        a2 = st.text_input("2. 오늘의 확언", key="a2", placeholder="두 번째 확언을 적어주세요")
        a3 = st.text_input("3. 오늘의 확언", key="a3", placeholder="세 번째 확언을 적어주세요")

        if st.session_state.stage == 2:
            if st.button("작성완료", key="btn_a"):
                if a1 and a2 and a3:
                    st.session_state.stage = 3
                    st.rerun()
                else:
                    st.warning("내용을 모두 작성해 주세요.")

    # --- 3단계: 확언 코멘트 및 최종 완료 ---
    if st.session_state.stage >= 3:
        st.info(f"🔥 **동기부여 메시지**\n\n'{a1}'라는 확언은 반드시 현실이 됩니다. 본부장님을 믿습니다!")
        st.markdown("---")
        if st.button("오늘의 기록 최종 저장"):
            st.balloons()
            st.success("모든 기록이 완료되었습니다. 멋진 하루 되세요!")
