import streamlit as st
import requests
import random

# 1. 페이지 설정
st.set_page_config(
    page_title="대전성모초 운동장 요정",
    page_icon="🧚",
    layout="centered"
)

# 2. 아이들 취향 저격 스타일링 (영어 제거 및 빈칸 최적화)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&display=swap');

    /* 전체 글씨체 설정 */
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
        margin-bottom: 0px;
    }

    /* 활동 점수판 디자인 - 빈칸 없이 바로 연결 */
    .score-container {
        background: white;
        padding: 30px;
        border-radius: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
        border: 5px solid #004a99;
        margin-top: 10px; /* 제목과의 간격을 좁혀 빈칸 느낌 제거 */
    }
    .score-number {
        font-size: 110px !important;
        font-weight: 900;
        color: #ff4b4b;
        margin: 0px;
        line-height: 1;
    }

    /* 영어 라벨 및 화살표 아이콘 완전 숨기기 (핵심!) */
    [data-testid="stMetricLabel"] { display: none !important; }
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; color: #004a99 !important; }
    
    /* 성모 약속 박스의 영어(_arrow_down_ 등) 숨기기 */
    .stExpander svg { display: none !important; } 
    .stExpanderSummary p { font-size: 1.6rem !important; color: #d4a017 !important; }
    .stExpanderSummary {
        background-color: #fff9e6 !important;
        border-radius: 15px !important;
        padding: 10px !important;
    }

    /* 풍선 크기 아주 작게 조절 */
    .stBalloon { transform: scale(0.2) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 기상 및 공기질 설정 (박순용 선생님 API 키 적용) ---
API_KEY = "fe1f2ac314b701d511deba080e04e3d5" 
CITY = "Daejeon"
LAT, LON = 36.325, 127.420

def get_weather_data():
    w_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"
    a_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"
    try:
        return requests.get(w_url).json(), requests.get(a_res_url).json()
    except:
        # 에러 방지를 위한 기본값 처리
        return None, None

# 3. 상단 헤더 (빈칸 없이 타이트하게 배치)
st.markdown("<p class='title-text'>🧚 운동장 요정의 속삭임</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.8rem; margin-top: -10px;'>성모 어린이들 모여라! 오늘 운동장은 어떤 기분일까? ✨</p>", unsafe_allow_html=True)

w_data, a_data = get_weather_data()

# 데이터가 없을 때를 대비한 샘플 데이터 (배포 시 API가 작동하면 자동으로 바뀝니다)
temp, hum, pm10, weather_desc = 15.0, 50, 25.0, "맑음"
if w_data and a_data:
    temp = w_data["main"]["temp"]
    hum = w_data["main"]["humidity"]
    weather_desc = w_data["weather"][0]["description"]
    pm10 = a_data['list'][0]['components']['pm10']

# 4. 점수 계산 및 상태 판정
dust_status = "꿀공기🍯" if pm10 <= 30 else "보통👍" if pm10 <= 80 else "안돼요😷"
score = 100
if temp > 30 or temp < 0: score -= 30
if hum > 80: score -= 20
if pm10 > 80: score -= 40
if "비" in weather_desc or "눈" in weather_desc: score = 0

# 5. 메인 점수판 (선생님이 말씀하신 빈칸을 이 내용으로 채웠습니다)
st.markdown("<div class='score-container'>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size: 1.6rem; color: #004a99; margin-bottom: 0;'>👑 오늘의 운동장 점수</p>", unsafe_allow_html=True)
st.markdown(f"<p class='score-number'>{score}</p>", unsafe_allow_html=True)
st.markdown(f"수치 확인: {temp}°C | {hum}% | {dust_status}", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 6. 상황별 재치 있는 멘트
if "비" in weather_desc:
    st.info(f"☔ **촉촉 요정**: 지금 비가 내려서 운동장이 세수하고 있어요! 오늘은 교실에서 뽀송하게 놀아요!")
elif score >= 85:
    st.balloons()
    st.success(f"🥳 **신난 요정 ({score}점)**: 대박! 날씨가 끝내줘요! 지금 안 나가면 손해라구!")
else:
    st.info(f"🤔 **고민 요정**: 날씨가 조금 애매해요! 나갈 거라면 선생님 말씀 잘 듣기!")

# 7. 성모 약속 (영어가 보이지 않게 수정)
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

# 8. 푸터 (제작자: 박순용 선생님)
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888; font-size: 1rem;'><b>제작: 박순용 선생님</b><br>© 2026 대전성모초등학교 창의융합 교실</p>", unsafe_allow_html=True)
