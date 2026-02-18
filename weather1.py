import streamlit as st
import requests
import random

# 1. 페이지 설정
st.set_page_config(
    page_title="대전성모초 운동장 요정",
    page_icon="🏫",
    layout="centered"
)

# 2. 인터랙티브 스타일링 (버튼 강조 및 풍선 크기 조절)
st.markdown("""
    <style>
    .main { background-color: #f8faff; }
    h1 { color: #004a99; text-align: center; margin-bottom: 0px; }
    
    /* 성모 약속 버튼 강조 효과 */
    .stExpander {
        border: 2px solid #004a99 !important;
        border-radius: 15px !important;
        background-color: #eef5ff !important;
    }
    
    /* 클릭 유도 애니메이션 */
    @keyframes blinking {
        0% { background-color: #eef5ff; }
        50% { background-color: #d0e3ff; }
        100% { background-color: #eef5ff; }
    }
    .stExpanderSummary {
        font-weight: bold !important;
        color: #004a99 !important;
        animation: blinking 2s infinite; /* 버튼이 살짝 깜빡이며 클릭 유도 */
    }

    /* 풍선 및 효과 가독성 조절 */
    .stBalloon { transform: scale(0.6); } /* 풍선 크기를 60%로 축소 */

    .status-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        border-top: 5px solid #004a99;
        margin-top: 20px;
    }
    .score-text {
        font-size: 35px;
        font-weight: bold;
        color: #ff4b4b;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 기상 및 공기질 설정 ---
API_KEY = "fe1f2ac314b701d511deba080e04e3d5" # 박순용 선생님의 API 키를 입력하세요!
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

# 3. 헤더 섹션
st.title("🏫 대전성모초 운동장 요정")
st.markdown("<p style='text-align: center; color: #666;'>성모 어린이들을 위한 박순용 선생님의 기상 안내소</p>", unsafe_allow_html=True)

w_data, a_data = get_weather_data()

if w_data and w_data.get("main") and a_data:
    temp, hum = w_data["main"]["temp"], w_data["main"]["humidity"]
    weather_desc = w_data["weather"][0]["description"]
    pm10 = a_data['list'][0]['components']['pm10']
    
    # 4. 활동 점수 및 미세먼지 판정
    dust_status = "좋음" if pm10 <= 30 else "보통" if pm10 <= 80 else "나쁨" if pm10 <= 150 else "매우나쁨"
    score = 100
    if temp > 30 or temp < 0: score -= 30
    if hum > 80: score -= 20
    if pm10 > 80: score -= 40
    
    is_raining = "비" in weather_desc or "소나기" in weather_desc
    is_snowing = "눈" in weather_desc
    if is_raining or is_snowing: score = 0

    # 5. 메인 대시보드
    st.markdown("<div class='status-box'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡️ 기온", f"{temp}°C")
    c2.metric("💧 습도", f"{hum}%")
    c3.metric("😷 먼지", dust_status)
    c4.metric("☁️ 날씨", weather_desc)
    
    st.divider()
    st.markdown(f"<p style='text-align: center; font-size: 1.1rem; color: #444;'>오늘의 운동장 활동 점수</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='score-text'>{score}점</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 6. 요정의 메시지 및 시각 효과 (풍선 크기 조절됨)
    if is_raining:
        st.info(f"☔ **요정의 메시지**: 현재 습도가 {hum}%예요! 비가 내려 운동장이 미끄러우니 실내에서 안전하게 놀아요.")
    elif is_snowing:
        st.snow()
        st.warning(f"❄️ **요정의 메시지**: 눈이 내려요! 습도는 {hum}%이고 길이 미끄러우니 성모 어린이들 모두 조심하세요.")
    elif score >= 80:
        st.balloons() # 작아진 풍선 효과
        st.success(f"✅ **요정의 메시지 ({score}점)**: 날씨도 공기도 최고! 운동장에서 신나게 뛰어놀아요!")
    else:
        st.info("💡 **요정의 메시지**: 오늘 날씨에 맞춰 선생님과 함께 즐거운 시간을 보내봐요!")

    # 7. 클릭을 유도하는 '성모 약속' 장치
    st.write("")
    st.markdown("#### 👇 여기를 눌러 오늘의 약속을 확인하세요!")
    with st.expander("✨ 오늘의 성모 약속 확인하기 (Click!)"):
        commitments = [
            "친구의 장점을 먼저 찾아 칭찬하는 어린이가 되겠습니다.",
            "선생님의 가르침을 소중히 여기고 바른 자세로 공부하겠습니다.",
            "학교의 공공물건을 내 물건처럼 아껴서 사용하겠습니다.",
            "누가 보지 않아도 정직하게 행동하는 성모인이 되겠습니다."
        ]
        st.write(f"🌟 **{random.choice(commitments)}**")

else:
    st.error("데이터를 불러오는 중입니다. 잠시만 기다려주세요!")

# 8. 푸터
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>© 2026 대전성모초등학교 창의융합 수업 도구<br><b>제작: 박순용 선생님</b></p>", unsafe_allow_html=True)
