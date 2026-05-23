import streamlit as st
import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="AI Predictive Maintenance",
    page_icon="🏭",
    layout="wide"
)

# -------------------------------
# CUSTOM CSS
# -------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: #00FFAA;
}

div[data-testid="stMetric"] {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white !important;
    box-shadow: 2px 2px 12px rgba(0,0,0,0.3);
}

div[data-testid="stMetricLabel"] {
    color: white !important;
}

div[data-testid="stMetricValue"] {
    color: #00FFAA !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# FAKE DATASET
# -------------------------------

data = {
    "Temperature": [40, 45, 50, 55, 60, 70, 80, 90],
    "Vibration": [0.2, 0.3, 0.4, 0.5, 0.7, 0.8, 1.0, 1.2],
    "RPM": [1000, 1200, 1300, 1400, 1500, 1700, 1900, 2100],
    "Current": [2, 3, 4, 5, 6, 7, 8, 10],
    "Status": [0, 0, 0, 0, 1, 1, 1, 1]
}

df = pd.DataFrame(data)

X = df[["Temperature", "Vibration", "RPM", "Current"]]
y = df["Status"]

# -------------------------------
# TRAIN AI MODEL
# -------------------------------

model = RandomForestClassifier()
model.fit(X, y)

# -------------------------------
# GENERATE LIVE SENSOR VALUES
# -------------------------------

temperature = random.randint(30, 100)
vibration = round(random.uniform(0.1, 1.5), 2)
rpm = random.randint(800, 3000)
current = random.randint(1, 15)

# -------------------------------
# PREDICTION INPUT
# -------------------------------

input_data = pd.DataFrame({
    "Temperature": [temperature],
    "Vibration": [vibration],
    "RPM": [rpm],
    "Current": [current]
})

prediction = model.predict(input_data)

# -------------------------------
# HEALTH CALCULATION
# -------------------------------

health = 100 - (
    (temperature / 100) * 30 +
    (vibration / 1.5) * 30 +
    (current / 15) * 20 +
    (rpm / 3000) * 20
)

health = max(0, int(health))

# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("⚙️ Smart Maintenance System")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Machine Analytics", "Reports"]
)

st.sidebar.success("🟢 System Active")

st.sidebar.info("""
AI-powered predictive maintenance system
for industrial machine monitoring.
""")

st.sidebar.write("### 🧠 AI Model")
st.sidebar.success("Random Forest Classifier")

# -------------------------------
# AUTO REFRESH
# -------------------------------

st_autorefresh(interval=5000, key="datarefresh")

# -------------------------------
# DASHBOARD PAGE
# -------------------------------

if menu == "Dashboard":

    st.title("🏭 AI Predictive Maintenance Dashboard")

    st.write("### 📡 Real-Time Machine Monitoring")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🌡 Temperature", f"{temperature} °C")
    col2.metric("📳 Vibration", vibration)
    col3.metric("⚙ RPM", rpm)
    col4.metric("⚡ Current", f"{current} A")

    # -------------------------------
    # AI PREDICTION
    # -------------------------------

    st.subheader("🤖 AI Prediction Result")

    if prediction[0] == 0:
        st.success("🟢 MACHINE RUNNING NORMALLY")
    else:
        st.error("🔴 MACHINE FAULT DETECTED")

    # -------------------------------
    # AI ANALYSIS
    # -------------------------------

    st.subheader("🧠 AI Analysis")

    issues = []

    if temperature > 75:
        issues.append("High temperature detected")

    if vibration > 1.0:
        issues.append("Abnormal vibration levels")

    if rpm > 2500:
        issues.append("High RPM causing stress")

    if current > 10:
        issues.append("Excess current consumption")

    if len(issues) == 0:

        st.success("""
        ✅ Machine is operating under safe conditions.

        ✔ Temperature is stable  
        ✔ Vibration levels are normal  
        ✔ RPM is within safe limits  
        ✔ Current consumption is healthy
        """)

    else:

        st.error("⚠ Possible Fault Reasons Detected:")

        for issue in issues:
            st.write(f"🔴 {issue}")

    # -------------------------------
    # MACHINE HEALTH
    # -------------------------------

    st.subheader("💚 Machine Health Status")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health,
        title={'text': "Health Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "lightgreen"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    if health > 80:
        st.success("🟢 Machine Condition Excellent")

    elif health > 60:
        st.warning("🟡 Maintenance Recommended")

    else:
        st.error("🔴 Critical Machine Condition")

    # -------------------------------
    # SENSOR GRAPH
    # -------------------------------

    st.subheader("📊 Live Sensor Monitoring")

    fig2, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(
        ["Temperature", "Vibration", "RPM", "Current"],
        [temperature, vibration, rpm, current]
    )

    ax.bar_label(bars)

    ax.set_ylabel("Sensor Values")
    ax.set_title("Real-Time Sensor Data")

    st.pyplot(fig2)

# -------------------------------
# ANALYTICS PAGE
# -------------------------------

elif menu == "Machine Analytics":

    st.title("📈 Machine Analytics")

    st.write("""
    This section analyzes machine performance
    using AI-powered sensor monitoring.
    """)

    analytics = pd.DataFrame({
        "Parameter": ["Temperature", "Vibration", "RPM", "Current"],
        "Value": [temperature, vibration, rpm, current]
    })

    st.table(analytics)

    st.info("""
    AI continuously monitors sensor patterns
    to identify abnormal machine behavior.
    """)

# -------------------------------
# REPORTS PAGE
# -------------------------------

elif menu == "Reports":

    st.title("📑 Maintenance Report")

    if prediction[0] == 0:

        st.success("""
        ✔ Machine operating normally

        ✔ No immediate maintenance required

        ✔ System performance stable
        """)

    else:

        st.error("""
        ⚠ Fault prediction detected

        ⚠ Maintenance inspection required

        ⚠ Check vibration and temperature levels
        """)

    report = pd.DataFrame({
        "Temperature": [temperature],
        "Vibration": [vibration],
        "RPM": [rpm],
        "Current": [current],
        "Health": [f"{health}%"],
        "Status": ["NORMAL" if prediction[0] == 0 else "FAULT"]
    })

    st.table(report)

# -------------------------------
# FOOTER
# -------------------------------

st.caption("Developed for Industrial Predictive Maintenance Review")
