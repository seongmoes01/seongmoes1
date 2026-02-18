import streamlit as st
import requests
import random

# 1. 페이지 설정
st.set_page_config(
    page_title="대전성모초 운동장 요정",
    page_icon="🏫",
    layout="centered"
)

# 2. 스타일링 (점수판 디자인 추가)
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
        font-size: 30px;
        font-weight: bold;
        color: #ff4b4b;
        text-align: center;
    }
    .stMetric { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 기상청 설정 ---
API_KEY = "fe1f2ac314b701d511deba080e04e3d5" # 여기에 선생님의 API 키를 꼭 넣어주세요!
CITY = "Daejeon"

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"
    try:
        res = requests.get(url).json()
        return res
    except:
        return None

# 3. 상단 헤더
st.title("🏫 대전성모초 운동장 요정")
st.markdown("<p style='text-align: center; color: #666;'> 오늘의 활동 가능한 운동장 판정 점수 !</p>", unsafe_allow_html=True)

data = get_weather()

if data and data.get("main"):
    temp = data["main"]["temp"]
    hum = data["main"]["humidity"]
    weather_desc = data["weather"][0]["description"]
    
    # 4. 운동장 활동 가능 점수 계산 로직 (과학적 근거 가미)
    score = 100
    if temp > 30 or temp < 0: score -= 40  # 너무 덥거나 추우면 대폭 감점
    elif temp > 25 or temp < 10: score -= 15 # 약간 덥거나 추우면 조금 감점
    if hum > 70: score -= 20 # 습도가 높으면 끈적여서 감점
    if "비" in weather_desc or "눈" in weather_desc: score = 0 # 눈이나 비가 오면 활동 불가

    # 5. 날씨 데이터 및 점수 표시
    st.markdown("<div class='status-box'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("🌡️ 기온", f"{temp}°C")
    c2.metric("💧 습도", f"{hum}%")
    c3.metric("☁️ 날씨", weather_desc)
    
    st.divider()
    st.markdown(f"<p style='text-align: center; font-size: 1.2rem; color: #444;'>✨ 오늘의 운동장 활동 가능 점수 ✨</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='score-text'>{score}점 / 100점</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # 6. 점수별 요정의 메시지 및 효과
    if score >= 80:
        st.balloons()
        st.success(f"✅ **요정의 메시지 ({score}점)**: 와아! 최고예요! 운동장에서 마음껏 뛰어놀기 정말 좋은 날씨예요. 친구들과 축구 한 판 어때요?")
    elif score >= 50:
        st.info(f"💡 **요정의 메시지 ({score}점)**: 적당히 놀기 좋은 날이에요! 너무 무리하지 말고 그늘에서 쉬어가며 놀기로 해요.")
    elif score > 0:
        st.warning(f"⚠️ **요정의 메시지 ({score}점)**: 주의하세요! 날씨가 조금 힘들 수 있어요. 짧게 놀고 교실로 일찍 들어오는 게 좋겠어요.")
    else:
        if temp < 5: st.snow()
        st.error(f"🚫 **요정의 메시지 ({score}점)**: 오늘은 운동장 활동이 어려워요. 교실에서 친구들과 도란도란 즐거운 시간을 보내봐요!")

    # 7. 수업용 약속 (박순용 선생님 커스텀)
    st.divider()
    with st.expander("📚 행복한 '오늘의 성모 약속'"):
        commitments = [
            "친구에게 따뜻한 미소로 먼저 인사하겠습니다.",
            "내가 쓴 자리는 스스로 정리하는 멋진 성모인이 되겠습니다.",
            "선생님 말씀에 귀 기울이며 눈을 반짝이는 수업 시간을 만들겠습니다.",
            "급식을 감사히 먹고 건강한 몸과 마음을 키우겠습니다."
        ]
        st.write(f"🌟 **{random.choice(commitments)}**")

else:
    st.error("요정이 날씨를 확인하러 갔어요. 잠시 후에 다시 새로고침 해주세요!")

# 8. 하단 푸터
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>© 2026 대전성모초등학교 창의융합 수업 도구<br><b>제작: 박순용 선생님</b></p>", unsafe_allow_html=True)

