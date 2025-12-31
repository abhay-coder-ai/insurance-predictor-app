<<<<<<< HEAD
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

# --- CUSTOM STYLING (NEW THEME) ---
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background: linear-gradient(to bottom right, #001f3f, #000000);
        color: #FFFFFF;
    }

    /* Main titles and headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    /* Markdown text color */
    .stMarkdown {
        color: #E0E0E0;
    }

    /* Styling for containers/cards */
    div[data-testid="stVerticalBlock"], div[data-testid="stHorizontalBlock"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    
    /* Remove padding from main block container to make cards seamless */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Customize Streamlit widgets */
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
    }
    
    .st-emotion-cache-16txtl3 {
        padding: 1rem;
    }

</style>
""", unsafe_allow_html=True)


st.title("📊 Insurance Data Analysis Dashboard")

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

    # Function to create styled matplotlib figures
    def create_styled_figure():
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0)  # Transparent figure background
        ax.patch.set_alpha(0)   # Transparent axes background
        ax.tick_params(colors='white', which='both')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        return fig, ax

    with col1:
        # Chart 1: Charges by Smoker Status
        st.subheader("Charges: Smokers vs. Non-Smokers")
        fig1, ax1 = create_styled_figure()
        sns.boxplot(data=df, x='smoker', y='charges', ax=ax1, palette="viridis")
        ax1.spines['bottom'].set_color('white')
        ax1.spines['left'].set_color('white')
        st.pyplot(fig1)

        # Chart 3: Charges by Region
        st.subheader("Average Charges by Region")
        avg_charge_by_region = df.groupby('region')['charges'].mean().sort_values()
        st.bar_chart(avg_charge_by_region) # Using Streamlit's native chart which adapts well

    with col2:
        # Chart 2: Distribution of Age
        st.subheader("Distribution of Patient Age")
        fig3, ax3 = create_styled_figure()
        sns.histplot(df['age'], kde=True, ax=ax3, color="#87CEEB")
        ax3.spines['bottom'].set_color('white')
        ax3.spines['left'].set_color('white')
        st.pyplot(fig3)
        
        # Chart 4: Distribution of BMI
        st.subheader("Distribution of Patient BMI")
        fig4, ax4 = create_styled_figure()
        sns.histplot(df['bmi'], kde=True, ax=ax4, color="#FFA07A")
        ax4.spines['bottom'].set_color('white')
        ax4.spines['left'].set_color('white')
        st.pyplot(fig4)

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
        color_discrete_map={'no': '#00BFFF', 'yes': '#FF6347'},
        template='plotly_dark' # Use Plotly's dark theme
    )
    fig_interactive.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_interactive, use_container_width=True)
    
    # --- SECTION 3: FEATURE IMPORTANCE ---
    st.header("Model Insights")
    st.subheader("Feature Importance")
    st.markdown("This chart shows which factors have the biggest impact on the insurance cost prediction.")

    try:
        model = pickle.load(open('model.pkl', 'rb'))
        
        # Updated feature names to match the 10 features in the new model
        feature_names = [
            'Is Male', 'Smoker', 'NW Region', 'SE Region', 'SW Region', 
            'Age', 'BMI', 'Children', 'Age * Smoker', 'BMI * Smoker'
        ]
        
        # Check if the model has coefficients and the length matches
        if hasattr(model, 'coef_') and len(model.coef_) == len(feature_names):
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': model.coef_
            }).sort_values('importance', ascending=False)
            
            fig_importance, ax_importance = create_styled_figure()
            sns.barplot(x='importance', y='feature', data=importance_df, palette='coolwarm_r', ax=ax_importance)
            ax_importance.set_title("Impact of Each Feature on Insurance Cost", color='white')
            ax_importance.spines['bottom'].set_color('white')
            ax_importance.spines['left'].set_color('white')
            st.pyplot(fig_importance)
        else:
            st.warning("The loaded model's features do not match the expected feature names.")

    except FileNotFoundError:
        st.warning("Could not load 'model.pkl' to show feature importance. Ensure it's in the main directory.")
    except Exception as e:
        st.error(f"An error occurred while displaying feature importance: {e}")

    st.markdown("---")
    st.header("Raw Data")
    st.dataframe(df)

=======
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
>>>>>>> c275d0c969fa16a1272939281de0be20067e80d3
