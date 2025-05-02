# styling.py
import streamlit as st

def load_styles():
    """Load and apply custom CSS styles to the Streamlit app."""
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #ff4b4b;
        --secondary-color: #4b4bff;
        --background-color: #f0f2f6;
        --text-color: #262730;
        --highlight-color: #ffd166;
    }
    
    /* Header styling */
    .css-10trblm {
        color: var(--primary-color);
        font-weight: 800;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 20px;
        font-weight: 600;
    }
    
    .stButton > button[data-baseweb="button"] {
        background-color: var(--primary-color);
        transition: all 0.3s ease;
    }
    
    .stButton > button[data-baseweb="button"]:hover {
        background-color: #ff2e2e;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background-color: var(--secondary-color);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--text-color);
    }
    
    /* Achievement notification styling */
    .stToast {
        background-color: var(--highlight-color);
        color: var(--text-color);
        border-radius: 10px;
        font-weight: 600;
        padding: 10px;
    }
    
    /* Car model name styling */
    h2 {
        color: var(--secondary-color);
        margin-bottom: 0;
    }
    
    /* Tagline styling */
    h2 + p {
        font-style: italic;
        margin-top: 0;
        color: #666;
    }
    
    /* Game summary styling */
    .stMetric {
        background-color: rgba(75, 75, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    
    /* Mobile responsiveness */
    @media screen and (max-width: 768px) {
        .stButton > button {
            width: 100%;
        }
    }
    </style>
    """, unsafe_allow_html=True)
