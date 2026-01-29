import streamlit as st
import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3
import random

# --- [설정] 데이터베이스 연결 및 테이블 보정 ---
conn = sqlite3.connect('journal.db', check_same_thread=False)
c = conn.cursor()
# 오류 방지를 위해 테이블을 초기화하거나 칸(img_desc)을 명시적으로 확인합니다.
c.execute('CREATE TABLE IF NOT EXISTS diary (date TEXT PRIMARY KEY, gratitude TEXT, affirmation TEXT, image_url TEXT, img_desc TEXT)')
conn.commit()

# --- [기능 1] 한국 명언 사이트 실시간 크롤링 엔진 ---
def get_korean_wisdom():
    try:
        # 한국 명언 사이트(예시: 명언 가이드 등)에서 실시간으로 지혜를 수집합니다.
        url = "https://search.naver.com/search.naver?where=nexearch&query=명언"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 네이버 명언 검색 결과에서 텍스트 추출
        quotes = soup.select('.item_list li .text_area')
        if quotes:
            target = random.choice(quotes)
            text = target.select_one('.text').get_text(strip=True)
            author = target.select_one('.author').get_text(strip=True)
            return f"🇰🇷 **오늘의 한국어 영감**\n\n> \"{text}\"\n\n- {author}"
    except:
        # 네트워크 오류 시 본부장님을 위한 묵직한 예비 문구
        fallbacks = [
            "오늘이라는 선물은 당신이 어떻게 쓰느냐에 따라 기적이 됩니다.",
            "진정한 성공은 어제보다 나은 나를 발견하는 과정에 있습니다.",
            "당신의 생각이 당신의 세상을 만듭니다. 오늘을 긍정으로 채우십시오."
        ]
        return f"✨ **오늘의 문장**\n\n> \"{random.choice(fallbacks)}\""

# --- [기능 2] 사진 해석 엔진 ---
def analyze_photo_meaning(day_val):
    meanings = [
        "**[여명]** 어둠을 뚫고 나오는 빛은 본부장님의 잠재력이 현실이 되는 과정을 상징합니다.",
        "**[고요한 호수]** 잔잔한 수면은 깊은 내면의 힘을 의미합니다. 외부의 흔들림에도 평온을 유지하세요.",
        "**[단단한 나무]** 오늘 본부장님의 성실함이 거대한 성공의 밑거름이 될 것임을 나무의 뿌리가 말해줍니다."
    ]
    return meanings[day_val % len(meanings)]

# --- [보안] 로그인 (비밀번호: 1234) ---
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
    # 초기화 및 탭 구성
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
                    st.session_state.g_comment = get_korean_wisdom()
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
                        st.session_state.a_comment = get_korean_wisdom()
                        st.session_state.stage = 3
                        st.rerun()
                    else: st.warning("내용을 모두 작성해 주세요.")

        # 3단계: 사진 및 최종 저장
        if st.session_state.stage >= 3:
            st.info(st.session_state.a_comment)
            st.markdown("---")
            st.markdown("### 🖼️ 오늘의 사진 한 장")
            # 사진이 깨지지 않도록 주소 끝에 확장자(.jpg)를 명시합니다.
            img_url = f"https://picsum.photos/seed/{now.day}/800/400.jpg"
            st.image(img_url)
            
            photo_desc = analyze_photo_meaning(now.day)
            st.write(f"🔍 **사진의 해석:** {photo_desc}")

            if st.button("오늘의 기록 최종 저장"):
                gratitude_all = f"{g1} / {g2} / {g3}"
                affirmation_all = f"{a1} / {a2} / {a3}"
                # 5개의 값을 순서대로 저장하여 에러 방지
                c.execute('INSERT OR REPLACE INTO diary VALUES (?, ?, ?, ?, ?)', 
                          (str(now), gratitude_all, affirmation_all, img_url, photo_desc))
                conn.commit()
                
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
                st.write(f"🔍 **사진의 해석:** {row[4]}")
            else: st.warning("기록이 없습니다.")

