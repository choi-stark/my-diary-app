import streamlit as st
import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3

# [설정] 데이터베이스 연결
conn = sqlite3.connect('journal.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS diary (date TEXT, gratitude TEXT, affirmation TEXT, image_url TEXT)')

# [기능] 명언 크롤링 함수 (예시: 특정 사이트 혹은 API 활용)
def get_daily_quote():
    # 실제 구현 시 특정 명언 사이트를 크롤링하거나 무료 API를 사용합니다.
    # 여기서는 예시로 샘플 리스트를 활용하는 로직을 제안합니다.
    url = "https://api.quotable.io/random" # 무료 명언 API
    try:
        response = requests.get(url)
        data = response.json()
        return f"\"{data['content']}\" - {data['author']}"
    except:
        return "오늘도 당신은 충분히 잘해내고 있습니다. (네트워크 오류로 자체 명언 출력)"

# [UI] 상단 헤더 및 시간 체크
now = datetime.datetime.now()
st.title("☀️ GEVIS 데일리 리포트")

if now.hour >= 6:
    st.subheader(f"오늘은 {now.month}월 {now.day}일입니다. 오늘의 감사일기를 작성해주세요.")

# [UI] 1. 감사일기 섹션
st.divider()
st.markdown("### 🙏 감사일기 (3가지)")
g1 = st.text_input("첫 번째 감사", key="g1")
g2 = st.text_input("두 번째 감사", key="g2")
g3 = st.text_input("세 번째 감사", key="g3")

if st.button("감사 코멘트 받기"):
    quote = get_daily_quote()
    st.info(f"✨ **최본부장님을 위한 감사 코멘트**\n\n작은 감사들이 모여 큰 행복을 만듭니다. {g1}, {g2}, {g3}라는 소중한 마음을 간직하세요.\n\n> {quote}")

# [UI] 2. 확언일기 섹션
st.divider()
st.markdown("### 💪 확언일기 (3가지)")
a1 = st.text_input("첫 번째 확언", key="a1")
a2 = st.text_input("두 번째 확언", key="a2")
a3 = st.text_input("세 번째 확언", key="a3")

if st.button("동기부여 메시지 받기"):
    st.success(f"🔥 **할 수 있다는 믿음**\n\n'{a1}'와 같은 확언이 최본부장님의 오늘을 바꿀 것입니다. 당신의 능력을 믿으세요!")

# [UI] 3. 오늘의 이미지 & 저장
st.divider()
if st.button("오늘의 일기 저장 및 이미지 생성"):
    # 이미지 생성 API 호출 로직 (예: Unsplash Source)
    img_url = "https://source.unsplash.com/featured/?nature,peace"
    st.image(img_url, caption="오늘의 무드")
    
    # DB 저장
    date_str = now.strftime("%Y-%m-%d")
    gratitude_full = f"{g1} / {g2} / {g3}"
    affirmation_full = f"{a1} / {a2} / {a3}"
    c.execute('INSERT INTO diary VALUES (?,?,?,?)', (date_str, gratitude_full, affirmation_full, img_url))
    conn.commit()
    st.balloons()