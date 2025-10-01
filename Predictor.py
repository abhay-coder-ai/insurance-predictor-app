import streamlit as st
import pickle
import numpy as np
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Insurance Cost Predictor",
    page_icon="🏥",
    layout="wide",
)

# --- DARK THEME STYLING ---
st.markdown(f"""
<style>
    /* Main app background */
    .stApp {{
        background-image: url("https://images.unsplash.com/photo-1579684385127-1ef15d508118?q=80&w=2080&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-position: center;
    }}
    
    /* --- THIS IS THE FIX --- */
    /* All headers (h1, h2, h3) to a darker, light-slate-gray */
    h1, h2, h3 {{
        color: #778899 !important; 
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: #1b263b;
    }}
    
    /* Text inside the sidebar */
    [data-testid="stSidebar"] div {{
        color: #FFFFFF !important;
    }}

    /* Button styling */
    .stButton>button {{
        background-color: #007BFF;
        color: white;
    }}
</style>
""", unsafe_allow_html=True)


# --- LOAD MODEL AND SCALER ---
try:
    model = pickle.load(open('model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model/scaler files not found. Ensure they are in the root directory.")
    st.stop()

# --- SIDEBAR FOR USER INPUT ---
with st.sidebar:
    st.header("📋 Enter Your Details")
    age = st.number_input("Age", 18, 100, 30)
    sex = st.selectbox("Sex", ("male", "female"))
    bmi = st.number_input("BMI", 10.0, 60.0, 25.0, format="%.2f")
    children = st.slider("Children", 0, 5, 0)
    smoker = st.radio("Smoker", ("yes", "no"), horizontal=True)
    region = st.selectbox("Region", ("southwest", "southeast", "northwest", "northeast"))
    
    predict_button = st.button("Predict Cost")

# --- MAIN PAGE LAYOUT ---
st.title("👨‍⚕️ Medical Insurance Cost Predictor")
st.markdown('<p style="color:#B0C4DE;">Get an instant estimate of your annual insurance premium.</p>', unsafe_allow_html=True)

if predict_button:
    # --- PREDICTION LOGIC ---
    features = np.array([[
        1 if sex == 'male' else 0, 
        1 if smoker == 'yes' else 0,
        1 if region == 'northwest' else 0,
        1 if region == 'southeast' else 0,
        1 if region == 'southwest' else 0,
        age, bmi, children
    ]])
    
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features)
    
    # --- DISPLAY RESULT ---
    st.markdown("---")
    st.subheader("Your Estimated Annual Charge:")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="background-color:#023047; border: 1px solid #00B4D8; padding: 20px; border-radius: 10px; text-align: center;">
            <h1 style="color:#90E0EF;">${prediction[0]:,.2f}</h1>
        </div>
        """, unsafe_allow_html=True)
    st.balloons()
else:
    # --- DEFAULT VIEW ---
    st.info("Enter your details in the sidebar to see your estimated cost.")