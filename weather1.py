import streamlit as st
import requests
import random

# 1. 페이지 설정 (아이콘과 제목 설정)
st.set_page_config(
    page_title="대전성모초 운동장 요정",
    page_icon="🧚",
    layout="centered"
)

# 2. 스타일링 (가독성 극대화 및 불필요한 요소 제거)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&display=swap');

    /* 전체 글꼴 설정 */
    html, body, [class*="st-"] {
        font-family: 'Gaegu', cursive !important;
    }

    .main { background-color: #f0f7ff; }
    
    /* 제목 스타일 */
    .title-text {
        color: #004a99;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: bold;
        margin-bottom: 5px;
    }

    /* 활동 점수판 디자인 */
    .score-container {
        background: white;
        padding: 30px;
        border-radius: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
        border: 5px solid #004a99;
        margin-bottom: 20px;
    }
    .score-number {
        font-size: 100px !important;
        font-weight: 900;
        color: #ff4b4b;
        margin: 0px;
        line-height: 1.2;
    }

    /* 영어 라벨 숨기기 및 숫자 크기 조절 */
    [data-testid="stMetricLabel"] { display: none; }
    [data-testid="stMetricValue"] { font-size: 2rem !important; color: #004a99 !important; }

    /* 풍선 크기 아주 작게 */
    .stBalloon { transform: scale(0.3) !important; }

    /* 성모 약속 상자 스타일 */
    .stExpander {
        border: 3px solid #ffcc00 !important;
        border-radius: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 기상 및 공기질 설정 (박순용 선생님 API 키 적용) ---
API_KEY = "fe1f2ac314b701d511deba080e04e3d5" 
CITY = "Daejeon"
LAT, LON = 36.325, 127.420 # 대전성모초 정밀 좌표

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
st.markdown("<p style='text-align: center; font-size: 1.8rem;'>성모 어린이들 모여라! 오늘 운동장은 어떤 기분일까? ✨</p>", unsafe_allow_html=True)

w_data, a_data = get_weather_data()

if w_data and w_data.get("main") and a_data:
    temp, hum = w_data["main"]["temp"], w_data["main"]["humidity"]
    weather_desc = w_data["weather"][0]["description"]
    pm10 = a_data['list'][0]['components']['pm10']
    
    # 4. 점수 계산 및 한글 상태 판정
    dust_status = "꿀공기🍯" if pm10 <= 30 else "보통👍" if pm10 <= 80 else "안돼요😷"
    score = 100
    if temp > 30 or temp < 0: score -= 30
    if hum > 80: score -= 20
    if pm10 > 80: score -= 40
    
    is_raining = "비" in weather_desc or "소나기" in weather_desc
    is_snowing = "눈" in weather_desc
    if is_raining or is_snowing: score = 0

    # 5. 메인 점수판 (영어 없이 숫자와 단위만 표시)
    st.markdown("<div class='score-container'>", unsafe_allow_html=True)
    st.markdown(f"<h2>👑 오늘의 운동장 점수</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='score-number'>{score}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 1.5rem; color: #666;'>100점 만점에 {score}점이에요!</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("", f"🌡️ {temp}°C")
    col2.metric("", f"💧 {hum}%")
    col3.metric("", f"😷 {dust_status}")
    st.markdown("</div>", unsafe_allow_html=True)

    # 6. 상황별 요정의 재밌는 멘트
    if is_raining:
        st.info(f"☔ **촉촉 요정**: 지금 비가 내려서 운동장이 세수하고 있어요! 습도는 {hum}%! 교실에서 뽀송하게 놀아요!")
    elif is_snowing:
        st.snow()
        st.warning(f"❄️ **꽁꽁 요정**: 와아! 하얀 가루가 내려요! 습도 {hum}%! 길이 미끄러우니 펭귄처럼 조심조심!")
    elif score >= 85:
        st.balloons()
        st.success(f"🥳 **신난 요정 ({score}점)**: 대박! 공기도 {dust_status}이고 날씨가 끝내줘요! 지금 안 나가면 손해!")
    elif pm10 > 80:
        st.error(f"⚠️ **먼지 요정 ({score}점)**: 켁켁! 공기 속에 나쁜 먼지가 숨어있어요! 오늘은 교실 보드게임 왕이 되어볼까?")
    else:
        st.info(f"🤔 **고민 요정 ({score}점)**: 날씨가 조금 애매해요! 나갈 거라면 선생님 말씀 잘 듣고 조심히 놀기!")

    # 7. 성모 약속 (클릭 유도)
    st.write("")
    st.markdown("### 👇 아래 노란 상자를 눌러 '오늘의 보물'을 찾으세요!")
    with st.expander("🎁 오늘의 성모 약속 (두근두근 클릭!)"):
        commitments = [
            "😊 친구의 장점을 먼저 찾아 예쁘게 웃어주는 친절 대장이 될게요!",
            "🏫 우리 학교 복도를 사뿐사뿐, 구름 위를 걷듯 조용히 다닐게요!",
            "💡 궁금한 게 생기면 눈을 반짝이며 질문하는 멋진 성모인이 될게요!",
            "🧹 내가 머문 자리는 요정이 다녀간 듯 깨끗하게 정리하겠습니다!"
        ]
        st.write(f"### 🌟 **{random.choice(commitments)}**")

else:
    st.error("요정이 하늘에서 데이터를 가져오는 중이에요. 잠시 후 새로고침 해주세요!")

# 8. 푸터 (제작자만 깔끔하게 표시)
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888; font-size: 1rem;'><b>제작: 박순용 선생님</b><br>© 2026 대전성모초등학교 창의융합 교실</p>", unsafe_allow_html=True)
