import streamlit as st
import requests
import random

# 1. 페이지 설정
st.set_page_config(page_title="대전성모초 운동장 요정", page_icon="🧚", layout="centered")

# 2. 스타일링 (빈칸 제거 및 고가독성 디자인)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Gaegu', cursive !important; }
    .main { background-color: #f0f7ff; }
    
    .title-text { color: #004a99; text-align: center; font-size: 3.5rem !important; font-weight: bold; margin-bottom: 5px; }
    
    /* 점선 박스 제거 및 새로운 대시보드 스타일 */
    .dashboard-card {
        background: white;
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        border: 4px solid #004a99;
        text-align: center;
        margin-top: -10px; /* 제목과의 간격을 좁혀 빈칸 느낌 제거 */
    }
    .score-number { font-size: 110px !important; font-weight: 900; color: #ff4b4b; line-height: 1; margin: 10px 0; }
    
    [data-testid="stMetricLabel"] { display: none !important; }
    .stBalloon { transform: scale(0.2) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 설정 (박순용 선생님 API 키 반영) ---
API_KEY = "fe1f2ac314b701d511deba080e04e3d5" 
CITY = "Daejeon"
LAT, LON = 36.325, 127.420

def get_weather_data():
    w_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"
    a_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"
    try:
        return requests.get(w_url).json(), requests.get(a_url).json()
    except: return None, None

# 3. 상단 헤더
st.markdown("<p class='title-text'>🧚 운동장 요정의 속삭임</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.8rem;'>성모 어린이들 모여라! 오늘 운동장은 어떤 기분일까? ✨</p>", unsafe_allow_html=True)

w_data, a_data = get_weather_data()

if w_data and a_data:
    temp, hum = w_data["main"]["temp"], w_data["main"]["humidity"]
    weather_desc = w_data["weather"][0]["description"]
    pm10 = a_data['list'][0]['components']['pm10']
    
    # 4. 점수 및 상태 판정
    dust_status = "꿀공기🍯" if pm10 <= 30 else "보통👍" if pm10 <= 80 else "안돼요😷"
    score = 100
    if temp > 30 or temp < 0: score -= 30
    if hum > 80: score -= 20
    if pm10 > 80: score -= 40
    if "비" in weather_desc or "눈" in weather_desc: score = 0

    # 5. 메인 대시보드 (기존의 빈 점선 칸을 대신함)
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 1.6rem; color: #004a99;'>👑 오늘의 운동장 놀이 점수</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='score-number'>{score}</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("", f"🌡️ {temp}°C")
    col2.metric("", f"💧 {hum}%")
    col3.metric("", f"😷 {dust_status}")
    st.markdown("</div>", unsafe_allow_html=True)

    # 6. 재밌는 상황별 멘트
    if "비" in weather_desc:
        st.info(f"☔ **촉촉 요정**: 운동장이 세수 중! 오늘은 교실에서 보드게임 왕이 되어볼까요?")
    elif score >= 85:
        st.balloons()
        st.success(f"🥳 **신난 요정 ({score}점)**: 날씨 대박! 지금 운동장으로 안 나가면 손해라구!")
    else:
        st.info(f"🤔 **고민 요정**: {temp}°C라 조금 애매해요! 나간다면 선생님 말씀 잘 듣기!")

    # 7. 성모 약속
    st.write("")
    with st.expander("🎁 오늘의 성모 약속 (두근두근 클릭!)"):
        st.write(f"### 🌟 **{random.choice(['친구에게 예쁜 미소 짓기!', '복도에서 사뿐사뿐 걷기!', '정리정돈 스스로 하기!'])}**")

# 8. 푸터
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'><b>제작: 박순용 선생님</b><br>© 2026 대전성모초등학교 창의융합 교실</p>", unsafe_allow_html=True)
