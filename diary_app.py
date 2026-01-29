import streamlit as st
import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3
import random

# --- [설정] 데이터베이스 연결 ---
conn = sqlite3.connect('journal.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS diary (date TEXT PRIMARY KEY, gratitude TEXT, affirmation TEXT, image_url TEXT, img_desc TEXT)')
conn.commit()

# --- [기능 1] 실시간 웹 크롤링 엔진 (Goodreads 활용) ---
def get_live_wisdom():
    try:
        # 실시간 명언 사이트에서 지혜를 수집합니다.
        url = f"https://www.goodreads.com/quotes/tag/inspirational?page={random.randint(1, 5)}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quoteText')
        if quotes:
            target = random.choice(quotes)
            text = target.get_text(strip=True).split('―')[0]
            author = target.find('span', class_='authorOrTitle').get_text(strip=True)
            return f"✨ **오늘의 실시간 영감**\n\n> \"{text}\"\n\n- {author}"
    except:
        return "✨ **오늘의 문장**\n\n> \"당신이 걷는 모든 길은 결국 당신의 빛이 될 것입니다.\""

# --- [기능 2] 사진 해석 엔진 ---
def analyze_photo_meaning(day_val):
    meanings = [
        "**[빛의 산란]** 흩어지는 빛줄기는 본부장님의 영향력이 곳곳으로 뻗어나감을 의미합니다.",
        "**[깊은 숲]** 울창한 숲은 단단한 내면을 상징합니다. 오늘 어떤 바람에도 본부장님은 흔들리지 않을 것입니다.",
        "**[잔잔한 바다]** 수평선은 무한한 가능성입니다. 오늘 본부장님의 선택이 거대한 물결을 일으킬 것입니다."
    ]
    return meanings[day_val % len(meanings)]

# --- [보안] 로그인 기능 (비밀번호: 1234) ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    
    if st.session_state["password_correct"]:
        return True

    st.title("🔒 GEVIS 개인 보안 영역")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("접속"):
        if password == "1234":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("비밀번호가 일치하지 않습니다.")
    return False

# --- [메인 로직] ---
if check_password():
    # 1. 초기화 (오류 방지 핵심!)
    if 'stage' not in st.session_state: st.session_state.stage = 1
    if 'g_comment' not in st.session_state: st.session_state.g_comment = ""
    if 'a_comment' not in st.session_state: st.session_state.a_comment = ""

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
                    st.session_state.g_comment = get_live_wisdom() # 실시간 크롤링
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
                        st.session_state.a_comment = get_live_wisdom() # 한 번 더 크롤링
                        st.session_state.stage = 3
                        st.rerun()
                    else: st.warning("내용을 모두 작성해 주세요.")

        # 3단계: 사진 및 최종 저장
        if st.session_state.stage >= 3:
            st.info(st.session_state.a_comment)
            st.markdown("---")
            st.markdown("### 🖼️ 오늘의 사진 한 장")
            img_url = f"https://picsum.photos/800/400?random={now.day}"
            st.image(img_url)
            
            photo_desc = analyze_photo_meaning(now.day)
            st.write(f"🔍 **사진의 해석:** {photo_desc}")

            if st.button("오늘의 기록 최종 저장"):
                gratitude_all = f"{g1} / {g2} / {g3}"
                affirmation_all = f"{a1} / {a2} / {a3}"
                c.execute('INSERT OR REPLACE INTO diary VALUES (?, ?, ?, ?, ?)', 
                          (str(now), gratitude_all, affirmation_all, img_url, photo_desc))
                conn.commit()
                
                effect = random.choice(["balloons", "snow", "toast"])
                if effect == "balloons": st.balloons()
                elif effect == "snow": st.snow()
                else: st.toast("🎊 오늘의 기록을 마쳤습니다.")
                
                st.success("데이터베이스에 소중히 보관되었습니다.")
                st.session_state.stage = 1 # 초기화

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
                st.write(f"🔍 **사진의 해석:** {row[4]}")
            else: st.warning("기록이 없습니다.")
