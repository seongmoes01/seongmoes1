import streamlit as st
import requests

# 1. 페이지 설정 (대전성모초 테마색 반영)
st.set_page_config(page_title="대전성모초 운동장 요정", page_icon="🏫", layout="centered")

# CSS를 이용한 성모초 스타일링 (파란색 포인트)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stAlert { border-radius: 15px; }
    h1 { color: #004a99; border-bottom: 2px solid #004a99; padding-bottom: 10px; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 설정 (선생님의 API 키를 넣어주세요) ---
API_KEY = "fe1f2ac314b701d511deba080e04e3d5"
CITY = "Daejeon"

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"
    try:
        res = requests.get(url).json()
        return res
    except:
        return None

# 2. 상단 헤더 (학교 캐릭터/로고 배치 구역)
col_img, col_txt = st.columns([1, 3])
with col_img:
    # 성모초 캐릭터 이미지가 있다면 여기에 URL을 넣으세요. 현재는 이모지로 대체합니다.
    st.title("🧚") 
with col_txt:
    st.title("대전성모초 운동장 요정")
    st.write("성모 어린이 여러분, 오늘 운동장 상태를 확인해볼까요?")

# 3. 데이터 가져오기 및 화면 표시
data = get_weather()

if data and data.get("main"):
    temp = data["main"]["temp"]
    hum = data["main"]["humidity"]
    weather_desc = data["weather"][0]["description"]
    
    # 날씨 카드 레이아웃
    c1, c2, c3 = st.columns(3)
    c1.metric("현재 기온", f"{temp} °C")
    c2.metric("현재 습도", f"{hum} %")
    c3.metric("날씨 상황", weather_desc)

    st.divider()

    # 4. 성모초 어린이를 위한 요정의 판정
    if "비" in weather_desc or "소나기" in weather_desc:
        st.info("☔ **요정의 속삭임**: 지금은 비가 내려요! 친구들과 교실에서 도란도란 이야기를 나눠보는 건 어떨까요?")
    elif temp > 30:
        st.warning("☀️ **요정의 속삭임**: 햇볕이 너무 뜨거워요! 운동장에서 놀 때는 꼭 모자를 쓰고 물을 자주 마셔요.")
    elif temp < 5:
        st.snow("❄️ **요정의 속삭임**: 날씨가 많이 추워요. 외투를 든든히 입고 감기 조심하세요!")
    else:
        st.success("✅ **요정의 속삭임**: 와아! 운동장에서 마음껏 뛰어놀기 정말 좋은 날씨예요. 친구들과 축구 한 판 어때요?")

    # 5. 수업용 다이내믹 요소 (랜덤 칭찬 퀴즈)
    st.write("")
    with st.expander("📚 오늘은 어떤 마음으로 지내볼까요? (클릭!)"):
        tips = [
            "친구에게 먼저 '안녕'이라고 인사하는 성모 어린이가 되어요!",
            "선생님 말씀에 귀 기울이는 멋진 수업 시간을 만들어봐요.",
            "교실에 떨어진 쓰레기를 먼저 줍는 예쁜 마음을 가져봐요.",
            "오늘 배운 과학 원리를 집에 가서 가족들에게 설명해줄까요?"
        ]
        import random
        st.info(random.choice(tips))

else:
    st.error("요정이 데이터를 불러오는 중이에요. API 키가 활성화되었는지 확인해주세요!")

st.caption("© 2026 대전성모초등학교 - 선생님과 함께하는 즐거운 과학 교실")