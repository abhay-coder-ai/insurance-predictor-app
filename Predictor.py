import streamlit as st
import pickle
import numpy as np
import base64
import time

# =============================
# Page Configuration
# =============================
st.set_page_config(
    page_title="Insurance Quote Estimator",
    page_icon="💡",
    layout="wide"
)

# =============================
# Logo (SVG)
# =============================
logo_svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 24 24"
fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
</svg>
"""
b64_logo = base64.b64encode(logo_svg.encode()).decode()

# =============================
# Global CSS (Clean & Stable)
# =============================
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: #e5e7eb;
}

.card {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 2rem;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 10px 40px rgba(0,0,0,0.45);
    margin-bottom: 2rem;
}

h1, h2, h3 {
    color: #ffffff;
}

.subtext {
    color: #9ca3af;
}

button {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    border-radius: 12px !important;
    height: 3.2em;
    font-weight: 600 !important;
}

.result {
    font-size: 2.6rem;
    font-weight: 700;
    color: #ffffff;
}

</style>
""", unsafe_allow_html=True)

# =============================
# Load Model
# =============================
@st.cache_resource
def load_model():
    model = pickle.load(open("model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    return model, scaler

model, scaler = load_model()

# =============================
# Header Section
# =============================
c1, c2 = st.columns([1, 6])

with c1:
    st.image(f"data:image/svg+xml;base64,{b64_logo}", width=120)

with c2:
    st.markdown("## 💡 Insurance Quote Estimator")
    st.markdown(
        "<span class='subtext'>AI-powered medical insurance cost prediction using Machine Learning</span>",
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# =============================
# Info Cards
# =============================
i1, i2, i3 = st.columns(3)

with i1:
    st.markdown("""
    <div class="card">
        <h3>🧠 ML Model</h3>
        <p class="subtext">Multiple Linear Regression trained on real insurance data</p>
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown("""
    <div class="card">
        <h3>📊 Inputs Used</h3>
        <p class="subtext">Age, BMI, Smoking habits, Region & Family size</p>
    </div>
    """, unsafe_allow_html=True)

with i3:
    st.markdown("""
    <div class="card">
        <h3>⚡ Deployment</h3>
        <p class="subtext">End-to-end ML app built using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

# =============================
# Input Form (NO EXTRA BAR)
# =============================
st.markdown("### 📝 Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("🎂 Age", 18, 100, 30)
    bmi = st.number_input("⚖️ BMI", 10.0, 60.0, 25.0)
    children = st.slider("👶 Number of Children", 0, 5, 0)

with col2:
    sex = st.selectbox("🧍 Sex", ["male", "female"])
    smoker = st.selectbox("🚬 Smoker", ["no", "yes"])
    region = st.selectbox("📍 Region", ["northeast", "northwest", "southeast", "southwest"])

st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("🔍 Estimate Insurance Cost")

st.markdown("</div>", unsafe_allow_html=True)

# =============================
# Prediction Section
# =============================
if predict_btn:
    with st.spinner("Analyzing risk profile..."):
        time.sleep(1.3)

        sex_male = 1 if sex == "male" else 0
        smoker_yes = 1 if smoker == "yes" else 0
        region_nw = 1 if region == "northwest" else 0
        region_se = 1 if region == "southeast" else 0
        region_sw = 1 if region == "southwest" else 0

        age_smoker = age * smoker_yes
        bmi_smoker = bmi * smoker_yes

        features = np.array([[
            sex_male, smoker_yes, region_nw, region_se, region_sw,
            age, bmi, children, age_smoker, bmi_smoker
        ]])

        scaled_features = scaler.transform(features)
        prediction = model.predict(scaled_features)[0]

    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <p class="subtext">Estimated Annual Insurance Premium</p>
        <p class="result">${prediction:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

# =============================
# Footer
# =============================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<center class='subtext'>© 2025 | Developed by <b>Abhay Nag</b> | ML Deployment Project</center>",
    unsafe_allow_html=True
)
