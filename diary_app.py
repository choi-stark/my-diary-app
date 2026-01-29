import streamlit as st
import datetime
import sqlite3
import random

# --- [설정] 데이터베이스 ---
conn = sqlite3.connect('journal.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS diary (date TEXT PRIMARY KEY, gratitude TEXT, affirmation TEXT, image_url TEXT, img_desc TEXT)')
conn.commit()

# --- [기능] 정성스러운 아침 코멘트 및 사진 해석 엔진 ---
def get_morning_wisdom(type):
    # 아침의 시작에 어울리는 깊이 있는 명언들
    gratitude_pool = [
        "어둠이 걷히고 빛이 들어오는 이 순간, 당신의 감사는 오늘 하루라는 백지 위에 그리는 첫 번째 선입니다.",
        "감사는 단순히 과거의 답례가 아니라, 오늘 하루를 당신의 의지대로 끌고 가겠다는 강력한 선언입니다.",
        "진정한 풍요는 소유에 있지 않고, 오늘 당신 앞에 놓인 사소한 것들의 가치를 발견하는 시선에 있습니다."
    ]
    affirmation_pool = [
        "뿌린 대로 거두는 것이 자연의 이치라면, 오늘 당신이 뱉은 확언은 거대한 숲을 이루는 씨앗이 될 것입니다.",
        "자신을 믿는다는 것은 결과가 좋을 것임을 믿는 것이 아니라, 결과가 어떠하든 다시 일어설 나를 믿는 것입니다.",
        "당신의 생각은 당신의 인생을 만드는 유일한 도구입니다. 이 확언이 오늘 당신의 등대가 되어줄 것입니다."
    ]
    
    selected = random.choice(gratitude_pool if type == 'g' else affirmation_pool)
    return f"✨ **오늘의 문장**\n\n> \"{selected}\""

def get_photo_meaning(day_index):
    # 사진의 테마에 따른 심오한 해석
    meanings = [
        "**[여명]** 어둠을 뚫고 나오는 빛은 본부장님의 잠재력이 현실이 되는 과정을 상징합니다. 오늘이 바로 그 전환점입니다.",
        "**[고요한 호수]** 잔잔한 수면은 깊은 내면의 힘을 의미합니다. 외부의 흔들림에도 평온을 유지하는 본부장님의 하루를 응원합니다.",
        "**[나무의 뿌리]** 보이지 않는 곳에서 단단히 내린 뿌리가 거대한 나무를 지탱하듯, 오늘 본부장님의 성실함이 큰 성공의 밑거름이 될 것입니다.",
        "**[길]** 끝없이 펼쳐진 길은 본부장님이 가진 무한한 가능성을 의미합니다. 한 걸음의 가치를 믿고 나아가시길 바랍니다."
    ]
    return meanings[day_index % len(meanings)]

# --- [보안] 로그인 ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.title("🔒 GEVIS 개인 보안 영역")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("접속"):
        if password == "1234":
            st.session_state["password_correct"] = True
            st.rerun()
else:
    tab1, tab2 = st.tabs(["📝 오늘의 리포트", "📅 지난 기록 보기"])

    with tab1:
        if 'stage' not in st.session_state: st.session_state.stage = 1
        st.title("☀️ GEVIS 데일리 리포트")
        now = datetime.date.today()
        st.subheader(f"오늘은 {now.year}년 {now.month}월 {now.day}일입니다.")

        # --- 1단계: 감사일기 ---
        st.markdown("### 🙏 오늘의 감사일기")
        g1 = st.text_input("첫 번째 감사", key="g1")
        g2 = st.text_input("두 번째 감사", key="g2")
        g3 = st.text_input("세 번째 감사", key="g3")

        if st.session_state.stage == 1:
            if st.button("작성완료", key="btn_g"):
                if g1 and g2 and g3:
                    st.session_state.g_comment = get_morning_wisdom('g')
                    st.session_state.stage = 2
                    st.rerun()

        # --- 2단계: 확언일기 ---
        if st.session_state.stage >= 2:
            st.success(st.session_state.g_comment) # 불필요한 사족 제거
            st.markdown("---")
            st.markdown("### 💪 오늘의 확언일기")
            a1 = st.text_input("첫 번째 확언", key="a1")
            a2 = st.text_input("두 번째 확언", key="a2")
            a3 = st.text_input("세 번째 확언", key="a3")

            if st.session_state.stage == 2:
                if st.button("작성완료", key="btn_a"):
                    if a1 and a2 and a3:
                        st.session_state.a_comment = get_morning_wisdom('a')
                        st.session_state.stage = 3
                        st.rerun()

        # --- 3단계: 사진 및 최종 저장 ---
        if st.session_state.stage >= 3:
            st.info(st.session_state.a_comment)
            st.markdown("---")
            st.markdown("### 🖼️ 오늘의 사진 한 장") # 문구 수정
            img_url = f"https://picsum.photos/800/400?random={now.day}"
            st.image(img_url)
            
            photo_desc = get_photo_meaning(now.day) # 사진 의미 해석
            st.write(f"🔍 **이 사진의 의미:** {photo_desc}") # 캡션 수정

            if st.button("오늘의 기록 최종 저장"):
                gratitude_all = f"{g1} / {g2} / {g3}"
                affirmation_all = f"{a1} / {a2} / {a3}"
                c.execute('INSERT OR REPLACE INTO diary VALUES (?, ?, ?, ?, ?)', 
                          (str(now), gratitude_all, affirmation_all, img_url, photo_desc))
                conn.commit()
                
                # 매일 다른 이모션
                effect = random.choice(["balloons", "snow", "toast"])
                if effect == "balloons": st.balloons()
                elif effect == "snow": st.snow()
                else: st.toast("🎊 기록이 완료되었습니다.")
                
                st.success("데이터베이스에 소중히 보관되었습니다.")
                st.session_state.stage = 1

    with tab2:
        st.title("📂 히스토리")
        search_date = st.date_input("날짜 선택", now)
        if st.button("조회"):
            c.execute('SELECT * FROM diary WHERE date=?', (str(search_date),))
            row = c.fetchone()
            if row:
                st.write(f"### 📅 {row[0]}의 기록")
                st.info(f"**감사:** {row[1]}\n\n**확언:** {row[2]}")
                st.image(row[3])
                st.write(f"🔍 **사진의 의미:** {row[4]}")
            else: st.warning("기록이 없습니다.")
