import streamlit as st
import requests
import random

# 1. 페이지 설정 (모바일 및 웹 최적화)
st.set_page_config(
    page_title="대전성모초 운동장 요정",
    page_icon="🏫",
    layout="centered"
)

# 2. 대전성모초 전용 스타일 입히기 (가독성 중심)
st.markdown("""
    <style>
    .main { background-color: #f8faff; }
    h1 { color: #004a99; text-align: center; font-family: 'Nanum Gothic', sans-serif; margin-bottom: 0px; }
    .status-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        border-top: 5px solid #004a99;
        margin-top: 20px;
    }
    .stMetric { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 기상청 설정 ---
API_KEY = "fe1f2ac314b701d511deba080e04e3d5"  
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
st.markdown("<p style='text-align: center; color: #666;'>성모 어린이들의 즐겁고 안전한 바깥 놀이를 판정해드려요!</p>", unsafe_allow_html=True)

data = get_weather()

if data and data.get("main"):
    temp = data["main"]["temp"]
    hum = data["main"]["humidity"]
    weather_desc = data["weather"][0]["description"]
    
    # 4. 날씨 데이터 카드 (가독성 확보)
    st.markdown("<div class='status-box'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("🌡️ 기온", f"{temp}°C")
    c2.metric("💧 습도", f"{hum}%")
    c3.metric("☁️ 날씨", weather_desc)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # 5. 날씨별 다이나믹 효과 및 요정의 메시지
    # 가독성을 위해 눈 효과는 추울 때만 '잠깐' 실행됩니다.
    if "비" in weather_desc or "소나기" in weather_desc:
        st.info("☔ **요정의 메시지**: 지금은 비가 내려요. 복도에서 뛰지 말고 교실에서 친구들과 행복한 시간 보내세요!")
    elif temp < 5:
        st.snow() # 눈 효과 실행
        st.warning("❄️ **요정의 메시지**: 밖이 많이 추워요! 두꺼운 외투를 입고 감기에 걸리지 않도록 조심해요.")
    elif temp > 28:
        st.error("☀️ **요정의 메시지**: 햇볕이 무척 뜨겁네요! 운동장에서 놀기보다는 시원한 그늘이나 실내에서 쉬기로 해요.")
    else:
        st.balloons() # 날씨 좋을 땐 기분 좋게 풍선 효과!
        st.success("✅ **요정의 메시지**: 와아! 지금은 운동장에서 마음껏 뛰어놀기 정말 좋은 날씨예요!")

    # 6. 수업용 교육 요소 (오늘의 마음가짐)
    st.divider()
    with st.expander("📚 박순용 선생님과 함께하는 '오늘의 성모 약속'"):
        commitments = [
            "친구에게 먼저 따뜻한 미소로 인사하는 어린이가 되겠습니다.",
            "내가 사용한 물건은 스스로 정리정돈하는 멋진 성모인이 되겠습니다.",
            "수업 시간에 눈을 반짝이며 선생님 말씀에 귀를 기울이겠습니다.",
            "급식을 골고루 맛있게 먹고 튼튼한 몸을 만들겠습니다."
        ]
        st.write(f"🌟 **{random.choice(commitments)}**")

else:
    st.error("요정이 잠시 날씨 데이터를 확인하러 갔어요. 잠시 후 다시 확인해주세요!")

# 7. 하단 푸터 (제작자 수정 완료)
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>© 2026 대전성모초등학교 운동장 요정 <br><b>제작: 박순용 선생님</b></p>", unsafe_allow_html=True)
