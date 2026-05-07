import streamlit as st
import pickle
import pandas as pd
from pathlib import Path

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="IPL Predictor", layout="centered")

# =========================
# PREMIUM CSS
# =========================
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
.stApp {
    background: linear-gradient(180deg, #0b1120, #0f172a);
    color: #e5e7eb;
}

/* ===== TITLE ===== */
h1 {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: white !important;
}
/* ===== SUBTITLE ===== */
.subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 30px;
}

/* ===== LABELS ===== */
label {
    color: #cbd5e1 !important;
    font-size: 13px;
}

/* ===== INPUTS ===== */
div[data-baseweb="input"] input {
    background-color: #1f2937 !important;
    color: white !important;
    border-radius: 6px !important;
    border: none !important;
    height: 38px;
}

/* ===== SELECT ===== */
div[data-baseweb="select"] {
    background-color: #1f2937 !important;
    border-radius: 6px;
}

/* ===== BUTTON ===== */
div.stButton > button {
    border: 1px solid #4b5563;
    color: white;
    background: transparent;
    border-radius: 6px;
}

/* ===== RESULT ===== */
.result {
    text-align: center;
    font-size: 30px;
    font-weight: 600;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("<h1>🏏 IPL Sports Analytics Predictor</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Real-time match prediction using Machine Learning</div>", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
model = pickle.load(open("model.pkl", "rb"))

# =========================
# DATA
# =========================
teams = [
    'Chennai Super Kings','Mumbai Indians','Royal Challengers Bangalore',
    'Kolkata Knight Riders','Delhi Capitals','Sunrisers Hyderabad',
    'Rajasthan Royals','Punjab Kings'
]

cities = ['Mumbai','Delhi','Bangalore','Chennai','Kolkata','Hyderabad']

# =========================
# LOGOS
# =========================
team_logos = {
    'Chennai Super Kings': "logos/csk.png",
    'Mumbai Indians': "logos/mi.png",
    'Royal Challengers Bangalore': "logos/rcb.png",
    'Kolkata Knight Riders': "logos/kkr.png",
    'Delhi Capitals': "logos/dc.png",
    'Sunrisers Hyderabad': "logos/srh.png",
    'Rajasthan Royals': "logos/rr.png",
    'Punjab Kings': "logos/pbks.png"
}

def get_logo(team):
    path = Path(team_logos[team])
    if path.exists():
        return str(path)
    return None

# =========================
# TEAM SELECTION
# =========================
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Batting Team", teams)
    logo = get_logo(batting_team)
    if logo:
        st.image(logo, width=60)

with col2:
    bowling_team = st.selectbox("Bowling Team", teams)
    logo = get_logo(bowling_team)
    if logo:
        st.image(logo, width=60)

# =========================
# CITY
# =========================
city = st.selectbox("Venue", cities)

# =========================
# MATCH INPUTS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    runs_left = st.number_input("Runs Left", min_value=0)

with col2:
    balls_left = st.number_input("Balls Left", min_value=0)

with col3:
    wickets_left = st.number_input("Wickets Left", min_value=0, max_value=10)

crr = st.number_input("Current Run Rate", min_value=0.0)
rrr = st.number_input("Required Run Rate", min_value=0.0)

# =========================
# VALIDATION
# =========================
if batting_team == bowling_team:
    st.warning("⚠️ Teams must be different")

# =========================
# ENCODING
# =========================
team_map = {team: i for i, team in enumerate(teams)}
city_map = {city: i for i, city in enumerate(cities)}

# =========================
# PREDICT
# =========================
if st.button("Predict"):

    input_df = pd.DataFrame([[
        team_map[batting_team],
        team_map[bowling_team],
        city_map[city],
        runs_left, balls_left, wickets_left, crr, rrr
    ]], columns=[
        'batting_team','bowling_team','city',
        'runs_left','balls_left','wickets_left','crr','rrr'
    ])

    prob = model.predict_proba(input_df)[0][1]
    win_prob = round(prob * 100, 2)

    st.markdown(f"<div class='result'>Win Probability: {win_prob}%</div>", unsafe_allow_html=True)

    st.progress(int(win_prob))

    if win_prob > 50:
        st.success("Batting team likely to win")
    else:
        st.error("Bowling team likely to win")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("<p style='text-align:center;'>IPL Sports Analytics | Internship Project Dashboard</p>", unsafe_allow_html=True)