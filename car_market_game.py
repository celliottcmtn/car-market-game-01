import streamlit as st
from styling import load_styles
from ui_components import (
    display_header, display_achievement_notifications, 
    display_instructions, display_achievements_sidebar,
    display_car_design_controls, display_results_panel,
    display_summary
)
from game_logic import reset_game, initialize_session_state, simulate_market
from car_naming import generate_model_name, generate_tagline

# Initialize session state
initialize_session_state()

# Load CSS
load_styles()

# Display header
display_header()

# Show achievement notifications
display_achievement_notifications(st.session_state.new_achievements)
# Clear the notifications after displaying
st.session_state.new_achievements = []

# Instructions screen
if st.session_state.game_state == "instructions":
    display_instructions()
    
    # Start game button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div style="width: 120px; margin: 0 auto;">', unsafe_allow_html=True)
        start_button = st.button("Start Game", key="start_game_button", help="Click to start the game", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
    if start_button:
        st.session_state.game_state = "playing"
        st.session_state.attempts_used = 0
        st.session_state.attempts_results = []
        st.session_state.car_designs = []
        st.session_state.car_names = []
        st.session_state.car_taglines = []
        st.rerun()

    # Show achievements panel if user has earned any
    if st.session_state.total_achievements_earned > 0:
        with st.expander("📊 Your Achievements", expanded=False):
            display_achievements_sidebar(st.session_state.achievements)

# Playing the game or game over state
elif st.session_state.game_state == "playing" or st.session_state.game_state == "game_over":
    # Use a two-column layout for the main game interface
    main_col1, main_col2 = st.columns([1, 2])
    
    # Left column for car design controls
    with main_col1:
        # Rest of the game UI components and logic
        # ...
        
    # Right column for results display
    with main_col2:
        # Results panel
        # ...

if __name__ == "__main__":
    # This ensures the app runs correctly when executed directly
    pass
