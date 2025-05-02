# ui_components.py
import streamlit as st

def display_header():
    """Display the game header and title."""
    st.title("🚗 Car Market Simulator")
    st.subheader("Design, build, and sell cars to dominate the market!")

def display_achievement_notifications(new_achievements):
    """Display notifications for newly earned achievements."""
    for achievement in new_achievements:
        st.toast(f"🏆 Achievement Unlocked: {achievement['name']}")

def display_instructions():
    """Display game instructions to the player."""
    st.markdown("""
    ## How to Play
    
    Welcome to the Car Market Simulator! In this game, you'll design and launch cars to the market.
    
    ### Game Rules:
    1. You have 5 attempts to design and launch cars
    2. For each car, adjust the performance, efficiency, comfort, style, and price
    3. Launch your car to see how the market responds
    4. Try to maximize your profits and market share
    5. Earn achievements by reaching certain milestones
    
    ### Tips:
    - Different market segments value different attributes
    - Price your car appropriately for its features
    - Pay attention to market feedback to improve your next design
    - Try different strategies to see what works best
    
    Good luck, and may your automotive empire thrive!
    """)

def display_achievements_sidebar(achievements):
    """Display the achievements panel in the sidebar."""
    earned_achievements = [a for a in achievements if a['earned']]
    locked_achievements = [a for a in achievements if not a['earned']]
    
    # Show earned achievements
    if earned_achievements:
        st.markdown("### 🏆 Earned")
        for achievement in earned_achievements:
            st.markdown(f"**{achievement['name']}** - {achievement['description']}")
    
    # Show locked achievements with requirements
    if locked_achievements:
        st.markdown("### 🔒 Locked")
        for achievement in locked_achievements:
            st.markdown(f"**{achievement['name']}** - {achievement['description']}")
            st.markdown(f"*Requirement: {achievement['requirement']}*")
