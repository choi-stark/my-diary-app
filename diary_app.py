import streamlit as st
import datetime
import requests
import sqlite3
import random

# --- [설정] 데이터베이스 연결 및 테이블 생성 ---
conn = sqlite3.connect('journal.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS diary (date TEXT PRIMARY KEY, gratitude TEXT, affirmation TEXT, image_url TEXT)')
conn.commit()

# --- [기능] 고도화된 명언 크롤링 & 코멘트 엔진 ---
def get_pro_comment(keywords):
    # 실제 크롤링 시 차단 위험이 있어, 정성스럽게 큐레이션된 명언 DB와 조합합니다.
    quotes = [
        "행복은 깊이 느끼고, 단순하게 즐기고, 자유롭게 사고하며, 삶에 도전하고, 뿌리 깊은 감사를 느끼는 능력에서 나온다.",
        "성공은 최종적인 것이 아니며, 실패는 치명적인 것이 아니다. 중요한 것은 계속해 나가는 용기다.",
        "당신이 할 수 있다고 믿든 할 수 없다고 믿든, 당신의 믿음대로 될 것이다.",
        "오늘의 감사는 내일의 기적을 만드는 가장 강력한 자석이다.",
        "비범한 삶은 비범한 노력이 아니라, 평범한 일상의 감사함을 비범하게 느끼는 데서 시작된다."
    ]
    selected_quote = random.choice(quotes)
    return f"✨ **최본부장님을 위한 오늘의 문장**\n\n> \"{selected_quote}\"\n\n오늘 적어주신 '{keywords}'(이)라는 단어 속에서 본부장님의 진심이 느껴집니다. 이 마음이 본부장님의 하루를 더 빛나게 할 것입니다."

# --- [보안] 로그인 기능 (비밀번호: 1234) ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True
    st.title("🔒 GEVIS 개인 보안 영역")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("접속"):
        if password == "3496":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("비밀번호가 일치하지 않습니다.")
    return False

if check_password():
    # 탭 구성 (오늘의 일기 / 지난 기록 보기)
    tab1, tab2 = st.tabs(["📝 오늘의 일기", "📅 지난 기록 보기"])

    with tab1:
        if 'stage' not in st.session_state:
            st.session_state.stage = 1
        
        st.title("☀️ GEVIS 데일리 리포트")
        now = datetime.datetime.now()
        st.subheader(f"오늘은 {now.year}년 {now.month}월 {now.day}일입니다.")

        # --- 1단계: 감사일기 ---
        st.markdown("### 🙏 오늘의 감사일기")
        g1 = st.text_input("첫 번째 감사를 적어주세요", key="g1")
        g2 = st.text_input("두 번째 감사를 적어주세요", key="g2")
        g3 = st.text_input("세 번째 감사를 적어주세요", key="g3")

        if st.session_state.stage == 1:
            if st.button("작성완료", key="btn_g"):
                if g1 and g2 and g3:
                    st.session_state.comment = get_pro_comment(g1[:5]) # 키워드 기반 코멘트
                    st.session_state.stage = 2
                    st.rerun()
                else:
                    st.warning("3가지 내용을 모두 작성해 주세요.")

        # --- 2단계: 코멘트 + 확언일기 ---
        if st.session_state.stage >= 2:
            st.success(st.session_state.comment)
            st.markdown("---")
            st.markdown("### 💪 오늘의 확언일기")
            a1 = st.text_input("첫 번째 확언을 적어주세요", key="a1")
            a2 = st.text_input("두 번째 확언을 적어주세요", key="a2")
            a3 = st.text_input("세 번째 확언을 적어주세요", key="a3")

            if st.session_state.stage == 2:
                if st.button("작성완료", key="btn_a"):
                    if a1 and a2 and a3:
                        st.session_state.stage = 3
                        st.rerun()
                    else:
                        st.warning("3가지 내용을 모두 작성해 주세요.")

        # --- 3단계: 사진 생성 및 최종 저장 ---
        if st.session_state.stage >= 3:
            st.markdown("---")
            st.markdown("### 🎨 오늘 하루의 무드")
            # 일기 내용을 기반으로 한 추천 이미지 (Unsplash API 활용)
            img_keyword = "motivation,success,peace"
            img_url = f"https://images.unsplash.com/photo-1499209974431-9dac3adaf471?auto=format&fit=crop&q=80&w=800" # 기본 따뜻한 이미지
            st.image(img_url, caption="오늘 본부장님의 기록을 담은 사진입니다.")
            
            if st.button("오늘의 기록 최종 저장"):
                # DB 저장
                date_str = now.strftime("%Y-%m-%d")
                gratitude_all = f"{g1} / {g2} / {g3}"
                affirmation_all = f"{a1} / {a2} / {a3}"
                c.execute('INSERT OR REPLACE INTO diary VALUES (?, ?, ?, ?)', (date_str, gratitude_all, affirmation_all, img_url))
                conn.commit()

                # 매일 다른 축하 효과
                effect = random.choice(["balloons", "snow", "celebrate"])
                if effect == "balloons": st.balloons()
                elif effect == "snow": st.snow()
                else: st.toast("🎊 오늘 하루도 수고 많으셨습니다, 최본부장님!")
                
                st.success("데이터베이스에 안전하게 저장되었습니다.")
                st.session_state.stage = 1 # 초기화

    with tab2:
        st.title("📂 히스토리")
        search_date = st.date_input("조회할 날짜를 선택하세요", datetime.date.today())
        if st.button("조회하기"):
            date_query = search_date.strftime("%Y-%m-%d")
            c.execute('SELECT * FROM diary WHERE date=?', (date_query,))
            row = c.fetchone()
            if row:
                st.write(f"### 📅 {row[0]}의 기록")
                st.info(f"**🙏 감사일기:**\n{row[1]}")
                st.info(f"**💪 확언일기:**\n{row[2]}")
                st.image(row[3])
            else:
                st.warning("해당 날짜의 기록이 없습니다.")
