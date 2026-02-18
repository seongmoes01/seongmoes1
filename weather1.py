import streamlit as st
import requests
import random

# 1. 페이지 설정
st.set_page_config(
    page_title="대전성모초 운동장 요정",
    page_icon="🏫",
    layout="centered"
)

# 2. 스타일링
st.markdown("""
    <style>
    .main { background-color: #f8faff; }
    h1 { color: #004a99; text-align: center; margin-bottom: 0px; }
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
    .stMetric { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 기상청 및 미세먼지 설정 ---
API_KEY = "fe1f2ac314b701d511deba080e04e3d5" # 여기에 선생님의 API 키를 꼭 넣어주세요!
CITY = "Daejeon"
# 대전성모초 좌표 (정밀 미세먼지용)
LAT = 36.325
LON = 127.420

def get_weather_data():
    # 날씨 데이터
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"
    # 미세먼지 데이터
    air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"
    
    try:
        w_res = requests.get(weather_url).json()
        a_res = requests.get(air_url).json()
        return w_res, a_res
    except:
        return None, None

# 3. 상단 헤더
st.title("🏫 대전성모초 운동장 요정")
st.markdown("<p style='text-align: center; color: #666;'>성모초 오늘의 운동장 날씨와 공기 질!</p>", unsafe_allow_html=True)

w_data, a_data = get_weather_data()

if w_data and w_data.get("main") and a_data:
    temp = w_data["main"]["temp"]
    hum = w_data["main"]["humidity"]
    weather_desc = w_data["weather"][0]["description"]
    # 미세먼지 수치 (PM10 기준)
    pm10 = a_data['list'][0]['components']['pm10']
    
    # 미세먼지 등급 판정
    dust_status = "좋음"
    if pm10 > 150: dust_status = "매우나쁨"
    elif pm10 > 80: dust_status = "나쁨"
    elif pm10 > 30: dust_status = "보통"

    # 4. 운동장 활동 점수 계산 로직
    score = 100
    if temp > 30 or temp < 0: score -= 30
    if hum > 80: score -= 20
    if pm10 > 80: score -= 40 # 미세먼지 나쁨 이상이면 대폭 감점
    elif pm10 > 30: score -= 10
    
    # 눈/비 올 경우 점수 0점 처리
    is_raining = "비" in weather_desc or "소나기" in weather_desc
    is_snowing = "눈" in weather_desc
    if is_raining or is_snowing: score = 0

    # 5. 데이터 카드 표시
    st.markdown("<div class='status-box'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡️ 기온", f"{temp}°C")
    c2.metric("💧 습도", f"{hum}%")
    c3.metric("😷 먼지", dust_status)
    c4.metric("☁️ 날씨", weather_desc)
    
    st.divider()
    st.markdown(f"<p style='text-align: center; font-size: 1.2rem; color: #444;'>✨ 오늘의 운동장 활동 가능 점수 ✨</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='score-text'>{score}점 / 100점</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # 6. 상황별 요정의 상세 메시지
    if is_raining:
        st.info(f"☔ **요정의 메시지**: 현재 습도가 {hum}%로 매우 높고 비가 내리고 있어요! 운동장이 젖어 미끄러우니 오늘은 교실에서 안전하게 놀아요.")
    elif is_snowing:
        st.snow()
        st.warning(f"❄️ **요정의 메시지**: 하얀 눈이 내리고 있어요! 습도는 {hum}%이고 날씨가 추우니 복도나 계단에서 넘어지지 않도록 조심하세요.")
    elif score >= 80:
        st.balloons()
        st.success(f"✅ **요정의 메시지 ({score}점)**: 공기도 깨끗하고 날씨도 최고예요! 운동장에서 마음껏 뛰어놀아도 좋은 날입니다!")
    elif pm10 > 80:
        st.error(f"😷 **요정의 메시지 ({score}점)**: 미세먼지 농도가 높아요! 기관지 건강을 위해 오늘은 야외활동을 자제하고 마스크를 꼭 써주세요.")
    elif score >= 50:
        st.info(f"💡 **요정의 메시지 ({score}점)**: 놀기에 적당한 날씨예요. 중간중간 시원한 물을 마시며 휴식 시간을 가져보세요.")
    else:
        st.warning(f"⚠️ **요정의 메시지 ({score}점)**: 기온이나 공기 상태가 조금 불안정해요. 짧고 굵게 놀고 일찍 들어오기로 약속!")

    # 7. 수업용 약속 섹션
    st.divider()
    with st.expander("📚 감사할 줄 아는 성모초 어린이의 '오늘의 성모 약속'"):
        commitments = [
            "친구의 마음을 다치게 하지 않는 고운 말을 사용하겠습니다.",
            "급식실에서 차례차례 줄을 잘 서는 질서 있는 어린이가 되겠습니다.",
            "선생님과 눈을 맞추며 즐겁게 공부하는 성모 어린이가 되겠습니다.",
            "주변의 쓰레기를 먼저 줍는 깨끗한 마음을 실천하겠습니다."
        ]
        st.write(f"🌟 **{random.choice(commitments)}**")

else:
    st.error("요정이 기상청 서버에서 데이터를 가져오는 중이에요. 잠시 후 새로고침(F5) 해주세요!")

# 8. 푸터
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>© 2026 대전성모초등학교 창의융합 수업 도구<br><b>제작: 박순용 선생님</b></p>", unsafe_allow_html=True)
