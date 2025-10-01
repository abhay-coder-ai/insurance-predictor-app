import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pickle

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Insurance Data Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Analysis Dashboard")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("insurance.csv")
        return df
    except FileNotFoundError:
        st.error("The 'insurance.csv' file was not found. Please make sure it's in the main app directory.")
        return None

df = load_data()

if df is not None:
    # --- SECTION 1: STATIC GRAPHS ---
    st.header("Exploratory Data Analysis")
    col1, col2 = st.columns(2)

    with col1:
        # Chart 1: Charges by Smoker Status
        st.subheader("Charges: Smokers vs. Non-Smokers")
        fig1, ax1 = plt.subplots()
        sns.boxplot(data=df, x='smoker', y='charges', ax=ax1, palette="Set2")
        st.pyplot(fig1)

        # Chart 3: Charges by Region
        st.subheader("Average Charges by Region")
        avg_charge_by_region = df.groupby('region')['charges'].mean().sort_values()
        st.bar_chart(avg_charge_by_region, color="#007BFF")

    with col2:
        # Chart 2: Distribution of Age
        st.subheader("Distribution of Patient Age")
        fig3, ax3 = plt.subplots()
        sns.histplot(df['age'], kde=True, ax=ax3, color="skyblue")
        st.pyplot(fig3)
        
        # Chart 4: Distribution of BMI
        st.subheader("Distribution of Patient BMI")
        fig4, ax4 = plt.subplots()
        sns.histplot(df['bmi'], kde=True, ax=ax4, color="salmon")
        st.pyplot(fig4)

    st.markdown("---")

    # --- SECTION 2: INTERACTIVE PLOTLY CHART ---
    st.header("Interactive Analysis")
    st.subheader("Charges vs. BMI (Colored by Smoker)")
    
    fig_interactive = px.scatter(
        df, 
        x='bmi', 
        y='charges', 
        color='smoker',
        title="Hover over points to see details",
        labels={'bmi': 'Body Mass Index (BMI)', 'charges': 'Insurance Charges ($)'},
        color_discrete_map={'no': '#007BFF', 'yes': '#FF4B4B'}
    )
    st.plotly_chart(fig_interactive, use_container_width=True)
    
    st.markdown("---")
    
    # --- SECTION 3: FEATURE IMPORTANCE ---
    st.header("Model Insights")
    st.subheader("Feature Importance")
    st.markdown("This chart shows which factors have the biggest impact on the insurance cost prediction.")

    try:
        model = pickle.load(open('model.pkl', 'rb'))
        
        feature_names = [
            'Smoker', 'Is Male', 'NW Region', 'SE Region', 'SW Region', 
            'Age', 'BMI', 'Children'
        ]
        
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': model.coef_
        }).sort_values('importance', ascending=False)
        
        fig_importance, ax_importance = plt.subplots(figsize=(10, 6))
        sns.barplot(x='importance', y='feature', data=importance_df, palette='coolwarm', ax=ax_importance)
        ax_importance.set_title("Impact of Each Feature on Insurance Cost")
        st.pyplot(fig_importance)

    except FileNotFoundError:
        st.warning("Could not load 'model.pkl' to show feature importance. Ensure it's in the main directory.")

    st.markdown("---")
    st.header("Raw Data")
    st.dataframe(df)