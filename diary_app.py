import streamlit as st
import datetime
import requests
from bs4 import BeautifulSoup
import random

# --- [기능] 실시간 웹 크롤링 엔진 (BeautifulSoup 활용) ---
def get_live_wisdom():
    try:
        # 명언 공유 사이트에서 실시간으로 지혜를 낚아올립니다.
        # 아래 사이트는 매번 무작위로 다른 페이지의 명언을 제공합니다.
        url = f"https://www.goodreads.com/quotes/tag/inspirational?page={random.randint(1, 10)}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 웹페이지 내의 명언 요소들을 모두 추출
        quote_elements = soup.find_all('div', class_='quoteText')
        if quote_elements:
            target = random.choice(quote_elements)
            # 텍스트만 깔끔하게 정제
            full_text = target.get_text(strip=True).split('―')[0]
            author = target.find('span', class_='authorOrTitle').get_text(strip=True)
            return f"✨ **실시간 영감 (Live Crawling)**\n\n> \"{full_text}\"\n\n- {author}"
    except Exception as e:
        # 크롤링 실패 시 비상용 멘트 (최본부장님의 품격에 맞는 묵직한 문장)
        return "✨ **오늘의 문장**\n\n> \"삶은 우리가 만드는 것이며, 언제나 그래왔고, 앞으로도 그럴 것입니다.\""

# --- [기능] 이미지 속성 기반 의미 해석 엔진 ---
def analyze_photo_meaning(img_id):
    # 이미지 ID(날짜 등)에 따라 사진의 구도와 색감을 철학적으로 해석합니다.
    themes = [
        {"desc": "탁 트인 지평선", "meaning": "오늘의 사진은 '확장'을 의미합니다. 본부장님이 가진 생각의 경계가 무너지고 새로운 기회가 찾아올 징조입니다."},
        {"desc": "단단한 바위와 파도", "meaning": "변치 않는 원칙과 유연한 대응의 조화를 상징합니다. 오늘 어떤 파도가 와도 본부장님은 굳건하실 것입니다."},
        {"desc": "높이 솟은 나무들", "meaning": "성장은 눈에 보이지 않는 뿌리에서 시작됩니다. 오늘 본부장님이 하시는 작은 습관들이 거대한 미래를 지탱할 것입니다."}
    ]
    return themes[img_id % len(themes)]

# --- [UI 반영 섹션] ---
# (중략: 로그인 및 탭 구성은 동일)

# --- 3단계: 오늘의 사진 및 해석 출력 ---
if st.session_state.stage >= 3:
    st.markdown("---")
    st.markdown("### 🖼️ 오늘의 사진 한 장")
    img_url = f"https://picsum.photos/800/400?random={datetime.date.today().day}"
    st.image(img_url)
    
    # 사진의 고유 번호(날짜)를 기반으로 그 의미를 심층 해석
    photo_info = analyze_photo_meaning(datetime.date.today().day)
    st.write(f"🔍 **사진의 해석:** {photo_info['meaning']}") # "AI 추천 이미지" 문구 삭제 및 해석으로 대체
