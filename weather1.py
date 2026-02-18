import streamlit as st
import requests
import random

# 1. 페이지 설정
st.set_page_config(
    page_title="대전성모초 운동장 요정",
    page_icon="🧚",
    layout="centered"
)

# 2. 스타일링 (빈칸 제거 및 점수판 통합)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Gaegu', cursive !important;
    }

    .main { background-color: #f0f7ff; }
    
    .title-text {
        color: #004a99;
        text-align: center;
        font-size: 3rem !important;
        font-weight: bold;
        margin-bottom: 0px;
    }

    /* 활동 점수판 디자인 - 빈칸 없이 바로 연결됨 */
    .score-container {
        background: white;
        padding: 40px 20px;
        border-radius: 30px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        text-align: center;
        border: 5px solid #004a99;
        margin-top: 10px; /* 제목과 바로 붙여 빈칸 느낌 제거 */
    }
    .score-number {
        font-size: 110px !important;
        font-weight: 900;
        color: #ff4b4b;
        margin: 0px;
        line-height: 1;
    }

    [data-testid="stMetricLabel"] { display: none !important; }
    .stBalloon { transform: scale(0.2) !important; }

    .stExpander {
        border: 3px solid #ffcc00 !important;
        border-radius: 20px !important;
        background-color: #fff9e6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 기상 및 공기질 설정 ---
API_KEY = "fe1f2ac314b701d511deba080e04e3d5" 
CITY = "Daejeon"
LAT, LON = 36.325, 127.420

def get_weather_data():
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"
    air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"
    try:
        w_res = requests.get(weather_url).json()
        a_res = requests.get(air_url).json()
        return w_res, a_res
    except:
        return None, None

# 3. 상단 헤더
st.markdown("<p class='title-text'>🧚 운동장 요정의 속삭임</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.8rem; margin-top: -10px;'>성모 어린이들 모여라! 오늘 운동장은 어떤 기분일까? ✨</p>", unsafe_allow_html=True)

w_data, a_data = get_weather_data()

if w_data and w_data.get("main") and a_data:
    temp, hum = w_data["main"]["temp"], w_data["main"]["humidity"]
    weather_desc = w_data["weather"][0]["description"]
    pm10 = a_data['list'][0]['components']['pm10']
    
    dust_status = "꿀공기🍯" if pm10 <= 30 else "보통👍" if pm10 <= 80 else "안돼요😷"
    score = 100
    if temp > 30 or temp < 0: score -= 30
    if hum > 80: score -= 20
    if pm10 > 80: score -= 40
    
    is_raining = "비" in weather_desc or "소나기" in weather_desc
    is_snowing = "눈" in weather_desc
    if is_raining or is_snowing: score = 0

    # 5. 메인 점수판 (선생님이 싫어하셨던 빈칸을 점수판으로 대체)
    st.markdown("<div class='score-container'>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 1.6rem; color: #004a99; margin-bottom: 5px;'>👑 오늘의 운동장 점수</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='score-number'>{score}</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("", f"🌡️ {temp}°C")
    c2.metric("", f"💧 {hum}%")
    c3.metric("", f"😷 {dust_status}")
    st.markdown("</div>", unsafe_allow_html=True)

    # 6. 상황별 멘트
    if is_raining:
        st.info(f"☔ **촉촉 요정**: 운동장이 세수 중이에요! 교실에서 뽀송하게 놀아요!")
    elif is_snowing:
        st.snow()
        st.warning(f"❄️ **꽁꽁 요정**: 눈이 내려요! 펭귄처럼 조심조심 걷기 약속!")
    elif score >= 85:
        st.balloons()
        st.success(f"🥳 **신난 요정 ({score}점)**: 날씨 대박! 지금 운동장으로 안 나가면 손해!")
    else:
        st.info(f"🤔 **고민 요정**: {temp}°C라 조금 애매해요! 나간다면 선생님 말씀 잘 듣기!")

    # 7. 성모 약속
    st.write("")
    with st.expander("🎁 오늘의 성모 약속 (두근두근 클릭!)"):
        commitments = ["😊 친구에게 먼저 인사하기!", "🏫 복도에서 조용히 걷기!", "💡 선생님과 눈 맞추며 공부하기!", "🧹 내 자리는 내가 정리하기!"]
        st.write(f"### 🌟 **{random.choice(commitments)}**")

else:
    st.error("데이터를 불러오는 중이에요!")

# 8. 푸터
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888; font-size: 1rem;'><b>제작: 박순용 선생님</b><br>© 2026 대전성모초등학교 창의융합 교실</p>", unsafe_allow_html=True)
