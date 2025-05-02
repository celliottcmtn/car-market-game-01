import streamlit as st

def check_achievements(result, design):
    achievements_earned = []
    
    # First profitable car
    if not st.session_state.achievements["first_profit"] and result["Profit"] > 0:
        st.session_state.achievements["first_profit"] = True
        achievements_earned.append({
            "name": "First Profit!", 
            "description": "Created your first profitable car",
            "icon": "💰"
        })
    
    # Big seller (over 1000 units)
    if not st.session_state.achievements["big_seller"] and result["Estimated Sales"] > 1000:
        st.session_state.achievements["big_seller"] = True
        achievements_earned.append({
            "name": "Big Seller!", 
            "description": "Sold over 1,000 cars",
            "icon": "🚗"
        })
    
    # Luxury Master (profit in luxury segment)
    if not st.session_state.achievements["luxury_master"] and result["Best Market Segment"] == "Luxury" and result["Profit"] > 100000:
        st.session_state.achievements["luxury_master"] = True
        achievements_earned.append({
            "name": "Luxury Master!", 
            "description": "Created a highly profitable luxury car",
            "icon": "👑"
        })
    
    # Eco Genius (profit in eco-friendly segment)
    if not st.session_state.achievements["eco_genius"] and result["Best Market Segment"] == "Eco-Friendly" and result["Profit"] > 100000:
        st.session_state.achievements["eco_genius"] = True
        achievements_earned.append({
            "name": "Eco Genius!", 
            "description": "Created a highly profitable eco-friendly car",
            "icon": "🌱"
        })
    
    # Sports King (profit in sports segment)
    if not st.session_state.achievements["sports_king"] and result["Best Market Segment"] == "Sports" and result["Profit"] > 100000:
        st.session_
