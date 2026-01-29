import streamlit as st
import datetime
import sqlite3
import random

# --- [설정] 데이터베이스 연결 ---
conn = sqlite3.connect('journal.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS diary (date TEXT PRIMARY KEY, gratitude TEXT, affirmation TEXT, image_url TEXT)')
conn.commit()

# --- [기능] 정성스러운 코멘트 엔진 ---
def get_custom_comment(type, user_text=""):
    gratitude_quotes = [
        "행복은 이미 우리 곁에 있습니다. 그것을 발견하는 눈이 바로 '감사'입니다.",
        "작은 감사함이 모여 본부장님의 삶을 더 풍요롭게 만들 것입니다. 오늘 하루도 고생 많으셨습니다.",
        "감사는 과거에 의미를 부여하고, 오늘에 평화를 가져다주며, 내일을 위한 비전을 제시합니다."
    ]
    affirmation_quotes = [
        "본부장님의 확언은 단순한 문장이 아니라, 미래를 그리는 설계도입니다.",
        "생각하는 대로 살지 않으면, 사는 대로 생각하게 됩니다. 오늘의 확언이 본부장님의 길을 밝힐 것입니다.",
        "당신이 할 수 있다고 믿는다면, 이미 절반은 성공한 것입니다. 본부장님의 열정을 응원합니다!"
    ]
    
    quote = random.choice(gratitude_quotes if type == 'g' else affirmation_quotes)
    return f"✨ **GEVIS의 특별 코멘트**\n\n> \"{quote}\"\n\n오늘 남겨주신 '{user_text[:10]}...' 기록은 본부장님의 자산이 될 것입니다."

# --- [보안] 로그인 ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.title("🔒 GEVIS 개인 보안 영역")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("접속"):
        if password == "3496":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("비밀번호가 일치하지 않습니다.")
else:
    # 탭 구성: 일기 작성 / 히스토리
    tab1, tab2 = st.tabs(["📝 오늘의 리포트", "📅 지난 기록 보기"])

    with tab1:
        if 'stage' not in st.session_state: st.session_state.stage = 1
        if 'g_comment' not in st.session_state: st.session_state.g_comment = ""
        if 'a_comment' not in st.session_state: st.session_state.a_comment = ""

        st.title("☀️ GEVIS 데일리 리포트")
        now = datetime.date.today()
        st.subheader(f"오늘은 {now.year}년 {now.month}월 {now.day}일입니다.")

        # --- 1단계: 감사일기 ---
        st.markdown("---")
        st.markdown("### 🙏 오늘의 감사일기")
        g1 = st.text_input("첫 번째 감사를 적어주세요", key="g1")
        g2 = st.text_input("두 번째 감사를 적어주세요", key="g2")
        g3 = st.text_input("세 번째 감사를 적어주세요", key="g3")

        if st.session_state.stage == 1:
            if st.button("작성완료", key="btn_g"):
                if g1 and g2 and g3:
                    st.session_state.g_comment = get_custom_comment('g', g1)
                    st.session_state.stage = 2
                    st.rerun()
                else: st.warning("내용을 모두 작성해 주세요.")

        # --- 2단계: 확언일기 ---
        if st.session_state.stage >= 2:
            st.success(st.session_state.g_comment)
            st.markdown("---")
            st.markdown("### 💪 오늘의 확언일기")
            a1 = st.text_input("첫 번째 확언을 적어주세요", key="a1")
            a2 = st.text_input("두 번째 확언을 적어주세요", key="a2")
            a3 = st.text_input("세 번째 확언을 적어주세요", key="a3")

            if st.session_state.stage == 2:
                if st.button("작성완료", key="btn_a"):
                    if a1 and a2 and a3:
                        st.session_state.a_comment = get_custom_comment('a', a1)
                        st.session_state.stage = 3
                        st.rerun()
                    else: st.warning("내용을 모두 작성해 주세요.")

        # --- 3단계: 최종 코멘트 및 이미지 ---
        if st.session_state.stage >= 3:
            st.info(st.session_state.a_comment) # 확언 코멘트 출력
            st.markdown("---")
            st.markdown("### 🎨 오늘 하루의 무드")
            # 안정적인 랜덤 이미지 서비스로 교체
            img_url = f"https://picsum.photos/800/400?random={now.day}"
            st.image(img_url, caption="본부장님의 오늘을 담은 AI 추천 이미지입니다.")
            
            if st.button("오늘의 기록 최종 저장"):
                gratitude_all = f"{g1} / {g2} / {g3}"
                affirmation_all = f"{a1} / {a2} / {a3}"
                c.execute('INSERT OR REPLACE INTO diary VALUES (?, ?, ?, ?)', (str(now), gratitude_all, affirmation_all, img_url))
                conn.commit()

                # 매일 다른 효과
                effect = random.choice(["balloons", "snow", "toast"])
                if effect == "balloons": st.balloons()
                elif effect == "snow": st.snow()
                else: st.toast("🎊 저장 완료! 멋진 하루였습니다.")
                
                st.success("데이터베이스에 소중히 보관되었습니다.")
                st.session_state.stage = 1 # 완료 후 초기화

    with tab2:
        st.title("📂 히스토리")
        search_date = st.date_input("조회할 날짜를 선택하세요", datetime.date.today())
        if st.button("조회하기"):
            c.execute('SELECT * FROM diary WHERE date=?', (str(search_date),))
            row = c.fetchone()
            if row:
                st.write(f"### 📅 {row[0]}의 기록")
                st.info(f"**🙏 감사일기:** {row[1]}")
                st.info(f"**💪 확언일기:** {row[2]}")
                st.image(row[3])
            else: st.warning("해당 날짜의 기록이 없습니다.")

