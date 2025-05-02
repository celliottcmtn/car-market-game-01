import streamlit as st

def load_styles():
    """Load all CSS styles for the application"""
    st.markdown("""
    <style>        
    .custom-container, .custom-container-tariff, .instructions-container, .achievement-container, .market-event-container, .car-name-container {
            padding: 10px;
        }
        .stButton button {
            width: 100%;
        }
        .small-button {
            max-width: 100%;
        }
    }
    @media (min-width: 992px) {
        .sidebar-placeholder {
            display: block;
            width: 100%;
            height: 1px;
        }
        .results-container {
            padding-left: 20px;
        }
    }

    /* Animation for market events */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }

    /* Achievement badges */
    .achievement-badge {
        display: inline-block;
        margin: 5px;
        padding: 8px 12px;
        background-color: #f8f9fa;
        border: 2px solid #FFD700;
        border-radius: 8px;
        text-align: center;
    }
    
    .achievement-icon {
        display: block;
        font-size: 24px;
        margin-bottom: 5px;
    }
    
    .achievement-name {
        display: block;
        font-weight:bold;
        font-size: 14px;
    }
    
    /* Market event styling */
    .market-event-positive {
        color: #4CAF50;
        font-weight: bold;
    }
    
    .market-event-negative {
        color: #F44336;
        font-weight: bold;
    }
    
    /* Car name styling */
    .car-name-header {
        text-align: center;
        color: #3F51B5;
        margin: 5px 0;
    }
    
    .car-tagline {
        text-align: center;
        font-style: italic;
        color: #607D8B;
        margin: 5px 0 15px 0;
    }
    
    /* Header styling */
    .header-green {
        color: #4CAF50;
    }
    
    .header-orange {
        color: #FF9800;
    }
    
    .header-purple {
        color: #9C27B0;
    }
    
    .header-gold {
        color: #FFD700;
    }
    
    /* Section dividers */
    .section-divider {
        margin: 15px 0;
        padding-top: 10px;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Attempt counter */
    .attempt-counter {
        background-color: #f5f5f5;
        padding: 8px 12px;
        border-radius: 4px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 15px;
        border: 1px solid #e0e0e0;
    }
    
    /* Achievement notification */
    .achievement-notification {
        display: flex;
        align-items: center;
        background-color: #FFF9C4;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        border: 2px solid #FFD700;
        animation: pulse 1.5s infinite;
    }
    </style>
    """, unsafe_allow_html=True)
