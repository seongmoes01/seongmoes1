import streamlit as st
import requests
import random

# ----------------------------
# 1. 페이지 설정
# ----------------------------
st.set_page_config(
    page_title="대전성모초 운동장 요정",
    page_icon="🧚",
    layout="centered"
)

# ----------------------------
# 2. 감성 스타일 CSS
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Gaegu', cursive !important;
    font-size: 1.2rem;
}

.main { background-color: #f0f7ff; }

/* 제목 */
.title-text {
    color: #004a99;
    text-align: center;
    font-size: 3rem !important;
    font-weight: bold;
}

/* 파란 요정 메시지 박스 */
.message-box {
    background-color: #d9ecff;
    padding: 20px;
    border-radius: 40px;
    border: 4px dashed #1f77d0;
    text-align: center;
    font-size: 1.6rem;
    margin: 20px 0;
}

/* 점수판 */
.score-container {
    background: linear-gradient(135deg, #ffffff 0%, #e6f2ff 100%);
    padding: 30px;
    border-radius: 30px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    text-align: center;
    border: 4px dashed #004a99;
    margin: 20px 0;
}

.score-number {
    font-size: 80px !important;
    font-weight: 900;
    color: #ff4b4b;
}

/* 풍선 작게 */
.stBalloon { transform: scale(0.4) !important; }

/* expander 화살표 제거 */
details summary {
    list-style: none;
}
details summary::-webkit-details-marker {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 3. API 설정
# ----------------------------
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

# ----------------------------
# 4. 헤더
# ----------------------------
st.markdown("<p class='title-text'>🧚 운동장 요정의 속삭임</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.5rem;'>성모 어린이들 모여라! 오늘 운동장은 어떤 기분일까? ✨</p>", unsafe_allow_html=True)

w_data, a_data = get_weather_data()

if w_data and w_data.get("main") and a_data:

    temp = w_data["main"]["temp"]
    hum = w_data["main"]["humidity"]
    weather_desc = w_data["weather"][0]["description"]
    pm10 = a_data['list'][0]['components']['pm10']

    # ----------------------------
    # 5. 점수 계산
    # ----------------------------
    score = 100
    if temp > 30 or temp < 0: score -= 30
    if hum > 80: score -= 20
    if pm10 > 80: score -= 40

    is_raining = "비" in weather_desc
    is_snowing = "눈" in weather_desc
    if is_raining or is_snowing:
        score = 0

    dust_status = "꿀공기🍯" if pm10 <= 30 else "괜찮아👍" if pm10 <= 80 else "나쁨😷"

    # ----------------------------
    # 6. 🔵 파란 요정 메시지 박스
    # ----------------------------
    if score >= 85:
        fairy_msg = "🌞 햇살이 운동장을 반짝반짝! 오늘은 달리기 왕이 탄생하는 날!"
    elif score >= 50:
        fairy_msg = "🌤 조금 애매하지만 괜찮아요! 안전하게 뛰어놀 준비됐나요?"
    else:
        fairy_msg = "🏫 오늘은 실내 놀이 챔피언 도전! 교실에서도 즐거움은 계속!"

    st.markdown(f"<div class='message-box'>{fairy_msg}</div>", unsafe_allow_html=True)

    # ----------------------------
    # 7. 점수판
    # ----------------------------
    st.markdown("<div class='score-container'>", unsafe_allow_html=True)
    st.markdown("<h3>👑 오늘의 운동장 놀이 점수</h3>", unsafe_allow_html=True)
    st.markdown(f"<p class='score-number'>{score}점</p>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡️ 기온", f"{temp}°C")
    c2.metric("💧 습도", f"{hum}%")
    c3.metric("😷 먼지", dust_status)
    c4.metric("☁️ 날씨", weather_desc)

    st.markdown("</div>", unsafe_allow_html=True)

    # 풍선 효과
    if score >= 85:
        st.balloons()

    # ----------------------------
    # 8. 🎁 오늘의 성모 약속
    # ----------------------------
    st.markdown("### 👇 오늘의 보물을 열어보세요!")

    commitments = [
        "😊 친구에게 먼저 인사하는 멋진 어린이가 되겠습니다!",
        "🏫 복도를 조용히 걸으며 안전 지킴이가 되겠습니다!",
        "💡 모르는 건 용기 내어 질문하겠습니다!",
        "🧹 내가 사용한 자리는 깨끗하게 정리하겠습니다!"
    ]

    with st.expander("🎁 오늘의 성모 약속"):
        st.markdown(f"## 🌟 {random.choice(commitments)}")

else:
    st.error("요정이 데이터를 가져오지 못했어요! 새로고침 해주세요.")

# ----------------------------
# 9. 푸터
# ----------------------------
st.markdown("---")
st.markdown("<p style='text-align:center;color:#888;'>제작: 박순용 선생님<br>© 2026 대전성모초등학교 창의융합 교실</p>", unsafe_allow_html=True)
