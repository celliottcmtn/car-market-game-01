import streamlit as st
from market_simulation import simulate_market_performance
from car_naming import generate_model_name, generate_tagline, generate_version_name
from achievements import check_achievements
from image_generation import generate_car_image

def reset_game():
    """Reset game state"""
    st.session_state.game_state = "instructions"
    st.session_state.result = None
    st.session_state.car_image_url = None
    st.session_state.tariff_applied = False
    st.session_state.attempts_used = 0
    st.session_state.attempts_results = []
    st.session_state.car_designs = []
    st.session_state.new_achievements = []
    st.session_state.car_name = ""
    st.session_state.car_tagline = ""
    st.session_state.car_names = []
    st.session_state.car_taglines = []

def initialize_session_state():
    """Initialize all session state variables"""
    if 'game_state' not in st.session_state:
        st.session_state.game_state = "instructions"
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'car_image_url' not in st.session_state:
        st.session_state.car_image_url = None
    if 'tariff_applied' not in st.session_state:
        st.session_state.tariff_applied = False
    if 'attempts_used' not in st.session_state:
        st.session_state.attempts_used = 0
    if 'attempts_results' not in st.session_state:
        st.session_state.attempts_results = []
    if 'car_designs' not in st.session_state:
        st.session_state.car_designs = []
    if 'achievements' not in st.session_state:
        st.session_state.achievements = {
            "first_profit": False,
            "big_seller": False,
            "luxury_master": False,
            "eco_genius": False, 
            "sports_king": False,
            "budget_master": False,
            "family_favorite": False,
            "mega_profit": False
        }
    if 'new_achievements' not in st.session_state:
        st.session_state.new_achievements = []
    if 'total_achievements_earned' not in st.session_state:
        st.session_state.total_achievements_earned = 0
    if 'show_achievements' not in st.session_state:
        st.session_state.show_achievements = False
    if 'car_name' not in st.session_state:
        st.session_state.car_name = ""
    if 'car_tagline' not in st.session_state:
        st.session_state.car_tagline = ""
    if 'car_names' not in st.session_state:
        st.session_state.car_names = []
    if 'car_taglines' not in st.session_state:
        st.session_state.car_taglines = []

def simulate_market(speed, aesthetics, reliability, efficiency, tech, price):
    """Handle market simulation and update game state"""
    # Reset tariff state when simulating new market
    st.session_state.tariff_applied = False
    
    # Generate version name for this attempt
    versioned_name = generate_version_name(st.session_state.car_name, st.session_state.attempts_used + 1)
    
    # Generate tagline
    tagline = generate_tagline(speed, aesthetics, reliability, efficiency, tech)
    
    # Store design for future reference
    st.session_state.car_designs.append({
        "Speed": speed,
        "Aesthetics": aesthetics, 
        "Reliability": reliability,
        "Efficiency": efficiency,
        "Tech": tech,
        "Price": price
    })
    
    # Store car name and tagline
    st.session_state.car_names.append(versioned_name)
    st.session_state.car_taglines.append(tagline)
    
    # Simulate market
    st.session_state.result = simulate_market_performance(speed, aesthetics, reliability, efficiency, tech, price)
    st.session_state.attempts_results.append(st.session_state.result)
    st.session_state.attempts_used += 1
    
    # Check for achievements
    new_achievements = check_achievements(st.session_state.result, st.session_state.car_designs[-1])
    if new_achievements:
        st.session_state.new_achievements = new_achievements
        st.session_state.total_achievements_earned += len(new_achievements)
    
    # Clear car name for next attempt
    st.session_state.car_name = ""
    
    # Generate AI image only on final attempt
    if st.session_state.attempts_used >= 3:
        st.session_state.car_image_url = generate_car_image(speed, aesthetics, reliability, efficiency, tech, price)
        st.session_state.game_state = "game_over"
