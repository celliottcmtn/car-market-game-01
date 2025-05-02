# car_market_game.py
import streamlit as st
from styling import load_styles
from ui_components import (
    display_header, display_achievement_notifications, 
    display_instructions, display_achievements_sidebar
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
        # Car design controls
        st.subheader("Design Your Car")
        
        # Performance slider
        performance = st.slider(
            "Performance", 
            min_value=1, 
            max_value=10, 
            value=5,
            help="How fast and powerful your car is"
        )
        
        # Efficiency slider
        efficiency = st.slider(
            "Efficiency", 
            min_value=1, 
            max_value=10, 
            value=5,
            help="How fuel-efficient your car is"
        )
        
        # Comfort slider
        comfort = st.slider(
            "Comfort", 
            min_value=1, 
            max_value=10, 
            value=5,
            help="How comfortable and luxurious your car is"
        )
        
        # Style slider
        style = st.slider(
            "Style", 
            min_value=1, 
            max_value=10, 
            value=5,
            help="How stylish and visually appealing your car is"
        )
        
        # Price slider
        price = st.slider(
            "Price", 
            min_value=10000, 
            max_value=100000, 
            value=50000,
            step=5000,
            format="$%d",
            help="How much your car costs"
        )
        
        # Generate car name
        car_name = generate_model_name(performance, efficiency, comfort, style)
        
        # Generate tagline
        tagline = generate_tagline(performance, efficiency, comfort, style)
        
        # Display car name and tagline
        st.markdown(f"## {car_name}")
        st.markdown(f"*{tagline}*")
        
        # Submit design button
        submitted = st.button("Launch to Market", type="primary")
        
        if submitted and st.session_state.attempts_used < st.session_state.max_attempts:
            # Save the car design
            car_design = {
                "performance": performance,
                "efficiency": efficiency,
                "comfort": comfort,
                "style": style,
                "price": price
            }
            
            # Simulate market response
            market_response = simulate_market(car_design)
            
            # Update session state
            st.session_state.attempts_used += 1
            st.session_state.car_designs.append(car_design)
            st.session_state.car_names.append(car_name)
            st.session_state.car_taglines.append(tagline)
            st.session_state.attempts_results.append(market_response)
            
            # Check if game over
            if st.session_state.attempts_used >= st.session_state.max_attempts:
                st.session_state.game_state = "game_over"
            
            st.rerun()
        
        # Reset game button (only shown in game over state)
        if st.session_state.game_state == "game_over":
            if st.button("Play Again"):
                reset_game()
                st.rerun()
    
    # Right column for results display
    with main_col2:
        st.subheader("Market Results")
        
        if len(st.session_state.attempts_results) > 0:
            # Display results for each attempt
            for i, (design, name, tagline, result) in enumerate(zip(
                st.session_state.car_designs,
                st.session_state.car_names,
                st.session_state.car_taglines,
                st.session_state.attempts_results
            )):
                with st.expander(f"Launch {i+1}: {name}", expanded=(i == len(st.session_state.attempts_results) - 1)):
                    st.markdown(f"### {name}")
                    st.markdown(f"*{tagline}*")
                    
                    # Car specs
                    st.markdown("#### Specifications")
                    specs_col1, specs_col2 = st.columns(2)
                    with specs_col1:
                        st.markdown(f"**Performance:** {design['performance']}/10")
                        st.markdown(f"**Efficiency:** {design['efficiency']}/10")
                        st.markdown(f"**Comfort:** {design['comfort']}/10")
                    with specs_col2:
                        st.markdown(f"**Style:** {design['style']}/10")
                        st.markdown(f"**Price:** ${design['price']:,}")
                    
                    # Market results
                    st.markdown("#### Market Performance")
                    st.markdown(f"**Sales:** {result['sales']:,} units")
                    st.markdown(f"**Revenue:** ${result['revenue']:,}")
                    st.markdown(f"**Profit:** ${result['profit']:,}")
                    st.markdown(f"**Market Share:** {result['market_share']:.1f}%")
                    
                    # Feedback
                    st.markdown("#### Market Feedback")
                    st.markdown(result['feedback'])
        else:
            st.info("Design and launch your first car to see results here!")

# Game over summary (displayed below the main interface)
if st.session_state.game_state == "game_over":
    st.markdown("---")
    st.header("Game Summary")
    
    # Calculate total profit
    total_profit = sum(result['profit'] for result in st.session_state.attempts_results)
    
    # Calculate total sales
    total_sales = sum(result['sales'] for result in st.session_state.attempts_results)
    
    # Determine best seller
    best_seller_index = max(range(len(st.session_state.attempts_results)), 
                          key=lambda i: st.session_state.attempts_results[i]['sales'])
    best_seller = st.session_state.car_names[best_seller_index]
    
    # Display summary stats
    st.subheader("Your Automobile Empire")
    sum_col1, sum_col2, sum_col3 = st.columns(3)
    
    with sum_col1:
        st.metric("Total Profit", f"${total_profit:,}")
    with sum_col2:
        st.metric("Total Sales", f"{total_sales:,} units")
    with sum_col3:
        st.metric("Best Seller", best_seller)
    
    # Congratulatory message
    if total_profit > 1000000:
        st.success("Congratulations! You've built a successful car company!")
    elif total_profit > 0:
        st.info("You've made a profit! With more experience, you could become a major player.")
    else:
        st.error("Your company lost money. Better luck next time!")

if __name__ == "__main__":
    # This ensures the app runs correctly when executed directly
    pass
