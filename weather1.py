import streamlit as st
import requests
import random

# 1. 페이지 설정
st.set_page_config(
    page_title="대전성모초 운동장 요정",
    page_icon="🧚",
    layout="centered"
)

# 2. 아이들 취향 저격 스타일링 (글씨체, 점수 크기, 풍선 조절)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&display=swap');

    /* 전체 글씨체를 부드러운 느낌의 Gaegu 폰트로 설정 */
    html, body, [class*="st-"] {
        font-family: 'Gaegu', cursive !important;
        font-size: 1.2rem;
    }

    .main { background-color: #f0f7ff; }
    
    /* 제목 스타일 */
    .title-text {
        color: #004a99;
        text-align: center;
        font-size: 3rem !important;
        font-weight: bold;
        margin-bottom: 0px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* 활동 점수 왕창 크게! */
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
        margin: 10px 0;
    }

    /* 풍선 크기를 아주 작고 귀엽게 (기존보다 더 축소) */
    .stBalloon { transform: scale(0.4) !important; }

    /* 클릭 유도 버튼 효과 */
    .stExpander {
        border: 3px solid #ffcc00 !important;
        border-radius: 20px !important;
    }
    .stExpanderSummary {
        background-color: #fff9e6 !important;
        font-size: 1.5rem !important;
        color: #d4a017 !important;
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

# 3. 헤더 섹션
st.markdown("<p class='title-text'>🧚 운동장 요정의 속삭임</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.5rem;'>성모 어린이들 모여라! 오늘 운동장은 어떤 기분일까? ✨</p>", unsafe_allow_html=True)

w_data, a_data = get_weather_data()

if w_data and w_data.get("main") and a_data:
    temp, hum = w_data["main"]["temp"], w_data["main"]["humidity"]
    weather_desc = w_data["weather"][0]["description"]
    pm10 = a_data['list'][0]['components']['pm10']
    
    # 4. 활동 점수 및 미세먼지 판정
    dust_status = "꿀공기🍯" if pm10 <= 30 else "괜찮아👍" if pm10 <= 80 else "안돼요😷" if pm10 <= 150 else "위험해🚨"
    score = 100
    if temp > 30 or temp < 0: score -= 30
    if hum > 80: score -= 20
    if pm10 > 80: score -= 40
    
    is_raining = "비" in weather_desc or "소나기" in weather_desc
    is_snowing = "눈" in weather_desc
    if is_raining or is_snowing: score = 0

    # 5. 메인 점수판 (왕관 디자인 추가)
    st.markdown("<div class='score-container'>", unsafe_allow_html=True)
    st.markdown(f"<h3>👑 오늘의 운동장 놀이 점수</h3>", unsafe_allow_html=True)
    st.markdown(f"<p class='score-number'>{score}점</p>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡️ 기온", f"{temp}°C")
    c2.metric("💧 습도", f"{hum}%")
    c3.metric("😷 먼지", dust_status)
    c4.metric("☁️ 날씨", "맑음☀️" if "맑음" in weather_desc else "구름☁️")
    st.markdown("</div>", unsafe_allow_html=True)

    # 6. 상황별 요정의 재치 있는 멘트
    if is_raining:
        st.info(f"☔ **촉촉한 요정**: 지금 하늘에서 비가 내려서 운동장이 세수 중이에요! 습도가 {hum}%라 끈적하니 교실에서 뽀송하게 놀아요!")
    elif is_snowing:
        st.snow()
        st.warning(f"❄️ **꽁꽁 요정**: 와! 하얀 가루가 내려요! 습도는 {hum}%! 길이 미끄러우니 펭귄처럼 조심조심 걷기 약속!")
    elif score >= 85:
        st.balloons() # 더 작고 귀여워진 풍선
        st.success(f"🥳 **신난 요정 ({score}점)**: 대박! 공기도 {dust_status}이고 날씨가 끝내줘요! 지금 안 나가면 손해라구!")
    elif pm10 > 80:
        st.error(f"⚠️ **먼지 요정 ({score}점)**: 켁켁! 공기 속에 나쁜 먼지가 숨어있어요! 오늘은 교실에서 보드게임 왕이 되어볼까요?")
    else:
        st.info(f"🤔 **고민 중인 요정 ({score}점)**: 기온이 {temp}°C라 조금 애매해요! 나갈 거라면 선생님 말씀 잘 듣고 조심히 놀기!")

    # 7. 클릭 유도 '성모 약속' (애니메이션 강조)
    st.write("")
    st.markdown("### 👇 아래 노란 상자를 눌러 '오늘의 보물'을 찾으세요!")
    with st.expander("🎁 오늘의 성모 약속 (두근두근 클릭!)"):
        commitments = [
            "😊 친구의 눈을 보며 예쁘게 웃어주는 친절 대장이 되겠습니다!",
            "🏫 우리 학교 복도를 사뿐사뿐, 구름 위를 걷듯 조용히 다닐게요!",
            "💡 궁금한 게 생기면 참지 말고 눈을 반짝이며 질문하겠습니다!",
            "🧹 내가 머문 자리는 요정이 다녀간 듯 깨끗하게 정리하겠습니다!"
        ]
        st.write(f"### 🌟 **{random.choice(commitments)}**")

else:
    st.error("요정이 하늘에서 데이터를 가져오다가 잠시 길을 잃었나 봐요! 다시 새로고침 해주세요.")

# 8. 푸터 (제작자만 깔끔하게 표시)
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888; font-size: 1rem;'><b>제작: 박순용 선생님</b><br>© 2026 대전성모초등학교 창의융합 교실</p>", unsafe_allow_html=True)
