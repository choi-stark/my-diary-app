import streamlit as st
import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3
import random

# --- [1. 보안] 로그인 기능 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]: return True

    st.title("🔒 GEVIS 개인 보안 영역")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("접속"):
        # 본부장님이 설정하신 비밀번호 3496 유지
        if password == "3496":
            st.session_state["password_correct"] = True
            st.rerun()
        else: st.error("비밀번호가 일치하지 않습니다.")
    return False

if check_password():
    # --- [2. 설정] 데이터베이스 (v4 유지) ---
    conn = sqlite3.connect('journal_v4.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS diary (date TEXT PRIMARY KEY, gratitude TEXT, affirmation TEXT, image_url TEXT, img_desc TEXT)')
    conn.commit()

    # --- [3. 초기화] 세션 상태 ---
    if 'stage' not in st.session_state: st.session_state.stage = 1
    if 'g_comment' not in st.session_state: st.session_state.g_comment = ""
    if 'a_comment' not in st.session_state: st.session_state.a_comment = ""

    # --- [4. 기능] 맞춤형 실시간 크롤링 및 멘토 엔진 ---
    def get_mentor_remark():
        # 부드러운 격려(Soft)와 냉철한 쓴소리(Bitter) 혼합
        remarks = [
            "🌸 **[응원]** 본부장님, 오늘도 충분히 잘 해내셨습니다. 스스로를 믿으세요.",
            "🌸 **[공감]** 가끔은 쉬어가도 괜찮습니다. 지치지 않는 것이 가장 중요하니까요.",
            "⚡ **[자극]** 지금 이 정도로 만족하실 건가요? 본부장님의 잠재력은 훨씬 큽니다.",
            "⚡ **[경고]** 어제와 똑같이 살면서 다른 내일을 꿈꾸는 것은 욕심입니다. 지금 움직이세요."
        ]
        return random.choice(remarks)

    def get_custom_wisdom(keyword):
        try:
            url = f"https://search.naver.com/search.naver?where=nexearch&query={keyword}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.select('.item_list li')
            
            if items:
                target = random.choice(items)
                text = target.select_one('.text_area .text').get_text(strip=True)
                author = target.select_one('.text_area .author').get_text(strip=True)
                
                # 감사일기(명언)와 확언일기(동기부여) 구분
                icon = "🙏" if "동기부여" not in keyword else "🔥"
                title = "오늘의 지혜" if "동기부여" not in keyword else "오늘의 열정"
                
                # 확언일기일 때만 '멘토의 쓴소리/응원' 추가
                mentor_msg = f"\n\n---\n{get_mentor_remark()}" if "동기부여" in keyword else ""
                
                return f"{icon} **{title}**\n\n> \"{text}\"\n\n- {author}{mentor_msg}"
        except: pass
        return "✨ **오늘의 문장**\n\n> \"당신이 걷는 모든 길은 결국 당신만의 고유한 빛이 될 것입니다.\""

    # --- [5. 기능] 사진 의미 해석 ---
    def get_photo_meaning(day_val):
        meanings = [
            "**[여명]** 어둠을 뚫고 나오는 빛은 본부장님의 잠재력이 현실이 되는 과정을 상징합니다.",
            "**[고요한 호수]** 잔잔한 수면은 깊은 내면의 힘을 의미합니다. 외부의 흔들림에도 평온을 유지하세요.",
            "**[단단한 나무]** 오늘 본부장님의 성실함이 거대한 성공의 밑거름이 될 것임을 나무의 뿌리가 말해줍니다."
        ]
        return meanings[day_val % len(meanings)]

    # --- [6. UI] 메인 화면 ---
    tab1, tab2 = st.tabs(["📝 오늘의 리포트", "📅 지난 기록 보기"])

    with tab1:
        st.title("☀️ GEVIS 데일리 리포트")
        now = datetime.date.today()
        st.subheader(f"오늘은 {now.year}년 {now.month}월 {now.day}일입니다.")

        # 1단계: 감사일기
        st.markdown("### 🙏 오늘의 감사일기")
        g1 = st.text_input("첫 번째 감사", key="g1")
        g2 = st.text_input("두 번째 감사", key="g2")
        g3 = st.text_input("세 번째 감사", key="g3")

        if st.session_state.stage == 1:
            if st.button("작성완료", key="btn_g"):
                if g1 and g2 and g3:
                    st.session_state.g_comment = get_custom_wisdom("인생+명언")
                    st.session_state.stage = 2
                    st.rerun()
                else: st.warning("내용을 모두 작성해 주세요.")

        # 2단계: 확언일기
        if st.session_state.stage >= 2:
            st.success(st.session_state.g_comment)
            st.markdown("---")
            st.markdown("### 💪 오늘의 확언일기")
            a1 = st.text_input("첫 번째 확언", key="a1")
            a2 = st.text_input("두 번째 확언", key="a2")
            a3 = st.text_input("세 번째 확언", key="a3")

            if st.session_state.stage == 2:
                if st.button("작성완료", key="btn_a"):
                    if a1 and a2 and a3:
                        st.session_state.a_comment = get_custom_wisdom("성공+동기부여+명언")
                        st.session_state.stage = 3
                        st.rerun()
                    else: st.warning("내용을 모두 작성해 주세요.")

        # 3단계: 사진 및 최종 저장
        if st.session_state.stage >= 3:
            st.info(st.session_state.a_comment)
            st.markdown("---")
            st.markdown("### 🖼️ 오늘의 사진 한 장")
            img_url = f"https://picsum.photos/seed/{now.day}/800/400"
            st.image(img_url)
            
            photo_desc = get_photo_meaning(now.day)
            st.write(f"🔍 **사진의 해석:** {photo_desc}")

            if st.button("오늘의 기록 최종 저장"):
                gratitude_all = f"1. {g1}\n2. {g2}\n3. {g3}"
                affirmation_all = f"1. {a1}\n2. {a2}\n3. {a3}"
                c.execute('INSERT OR REPLACE INTO diary VALUES (?, ?, ?, ?, ?)', 
                          (str(now), gratitude_all, affirmation_all, img_url, photo_desc))
                conn.commit()
                st.balloons()
                st.success("데이터베이스에 소중히 보관되었습니다.")
                st.session_state.stage = 1

    with tab2:
        st.title("📂 히스토리")
        col_date, col_content = st.columns([1, 3])
        with col_date:
            st.markdown("##### 📅 날짜 선택")
            search_date = st.date_input("이동하고 싶은 날짜", now, label_visibility="collapsed")
        with col_content:
            c.execute('SELECT * FROM diary WHERE date=?', (str(search_date),))
            row = c.fetchone()
            if row:
                st.write(f"### 📅 {row[0]}의 기록")
                st.info(f"**🙏 오늘의 감사**\n\n{row[1]}")
                st.info(f"**💪 오늘의 확언**\n\n{row[2]}")
                st.image(row[3], use_container_width=True)
                st.caption(f"🔍 **사진의 해석:** {row[4]}")
            else: st.warning(f"{search_date}에 작성된 기록이 없습니다.")
