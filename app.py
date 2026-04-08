import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from sklearn.linear_model import LogisticRegression

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Diabetes Dashboard", layout="wide")

# CUSTOM CSS
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: #00FFAA;
}
.stButton>button {
    background-color: #00FFAA;
    color: black;
}
.big-title {
    font-size:40px;
    font-weight:bold;
    color:#00FFAA;
}
</style>
""", unsafe_allow_html=True)

# LOGIN SYSTEM
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login Page")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.login = True
        else:
            st.error("Invalid Login")

    st.stop()

# TITLE
st.title("🩺 Diabetes Risk Prediction Dashboard")
st.markdown('<p class="big-title">🩺 Smart Diabetes Dashboard</p>', unsafe_allow_html=True)

# SIDEBAR INPUT
st.sidebar.subheader("👤 Patient Info")

name = st.sidebar.text_input("Patient Name")
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

age = st.sidebar.slider("Age", 10, 80)
bmi = st.sidebar.slider("BMI", 10.0, 40.0)
glucose = st.sidebar.slider("Glucose", 70, 200)
activity = st.sidebar.selectbox("Activity", ["Low", "Medium", "High"])

activity_map = {"Low":0, "Medium":1, "High":2}

# DUMMY DATA
data = pd.DataFrame({
    "age":[25,45,50,35],
    "bmi":[22,30,28,26],
    "glucose":[90,150,160,120],
    "activity":[2,0,1,1],
    "risk":[0,1,1,0]
})

X = data[["age","bmi","glucose","activity"]]
y = data["risk"]

model = LogisticRegression()
model.fit(X,y)

# DISPLAY USER INFO
st.write(f"### 👤 Patient: {name}")
st.write(f"Gender: {gender}")

# PREDICTION
input_data = pd.DataFrame([[age,bmi,glucose,activity_map[activity]]],
columns=["age","bmi","glucose","activity"])

prediction = model.predict(input_data)[0]

# HEALTH SCORE
score = 100

if glucose > 140:
    score -= 30
if bmi > 30:
    score -= 30
if activity == "Low":
    score -= 20

st.write(f"💚 Health Score: {score}/100")
st.progress(score)

# RESULT
if prediction == 1:
    st.error("⚠️ High Risk")

    if glucose > 140:
        st.write("🔴 High glucose level detected")
    if bmi > 30:
        st.write("🔴 High BMI (Obesity)")
    if activity == "Low":
        st.write("🔴 Low physical activity")

else:
    st.success("✅ Low Risk")

# FILE UPLOAD
st.subheader("📁 Upload Patient Data")
file = st.file_uploader("Upload CSV")

if file:
    df = pd.read_csv(file)
    st.write(df.head())

# GAUGE CHART
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    title={'text': "Risk Level"},
    gauge={'axis': {'range': [0,100]}}
))

st.plotly_chart(fig)

# LINE CHART
chart_data = pd.DataFrame({
    "Time": pd.date_range(start="now", periods=10, freq="min"),
    "Glucose": [glucose + i for i in range(10)]
})

st.line_chart(chart_data.set_index("Time"))

# SUGGESTIONS
st.subheader("🧑‍⚕️ Suggestions")

if prediction == 1:
    st.write("✔️ Exercise daily")
    st.write("✔️ Reduce sugar intake")
    st.write("✔️ Consult doctor")
else:
    st.write("✔️ Maintain healthy lifestyle")

# REPORT DOWNLOAD
report = f"""
Patient: {name}
Age: {age}
BMI: {bmi}
Glucose: {glucose}
Result: {"High Risk" if prediction==1 else "Low Risk"}
"""

st.download_button("📥 Download Report", report)

# SIMULATION
st.write("🔄 Updating data...")
time.sleep(1)