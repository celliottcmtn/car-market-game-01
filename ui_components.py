import streamlit as st

def display_header():
    """Display the game header with logo"""
    st.markdown('<div style="max-width: 900px; margin: 0 auto; padding: 10px;">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 5])
    with col1:
        try:
            st.image("logo.png", width=100)
        except:
            pass  # Skip if logo doesn't load
    with col2:
        st.markdown("<h1 style='margin-top: 25px;'>Business Administration Car Market Simulation Game</h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def display_achievement_notifications(new_achievements):
    """Display notifications for newly earned achievements"""
    if new_achievements:
        # Display the newest achievement notification
        achievement = new_achievements[0]
        st.markdown(f"""
        <div class="achievement-notification">
            <span style="font-size: 28px; margin-right: 10px;">{achievement['icon']}</span>
            <div>
                <div style="font-size: 18px;">Achievement Unlocked!</div>
                <div>{achievement['name']} {achievement['description']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_instructions():
    """Display the instructions screen"""
    st.markdown("""
    <div class="instructions-container">
        <h2 style="color: #3498db; text-align: center;">Welcome to the Car Market Simulator!</h2>
        <hr>
        <h3>Game Instructions:</h3>
        <ol>
            <li><strong>Objective:</strong> Design a profitable car by adjusting its features and price.</li>
            <li><strong>You have 3 attempts</strong> to create a profitable car design.</li>
            <li>Customize your car's specifications using the sliders.</li>
            <li><strong style="color: #3F51B5;">See your car's name</strong> and marketing tagline based on its features!</li>
            <li>Click "Simulate Market" to see how your car performs.</li>
            <li>Learn from each attempt and adjust your strategy.</li>
            <li><strong style="color: #9C27B0;">Watch for Random Market Events!</strong> These happen frequently and can affect your profits.</li>
            <li><strong style="color: #FFD700;">Earn Achievements</strong> by reaching specific milestones.</li>
            <li>After your third attempt, you'll see an AI-generated image of your final car design.</li>
            <li>The "Impose Trump Tariff" button lets you see how a 25% tariff would affect your profits.</li>
        </ol>
        <p style="text-align: center; font-weight: bold;">Good luck with your car design!</p>
    </div>
    """, unsafe_allow_html=True)

def display_achievements_sidebar(achievements):
    """Display achievements in the sidebar during gameplay"""
    if sum(1 for value in achievements.values() if value) > 0:
        st.markdown("### 🏆 Your Achievements")
        
        # Build the HTML with individual achievement badges
        badges_html = ""
        
        achievement_data = [
            ("first_profit", "💰", "First Profit!"),
            ("big_seller", "🚗", "Big Seller!"),
            ("luxury_master", "👑", "Luxury Master!"),
            ("eco_genius", "🌱", "Eco Genius!"), 
            ("sports_king", "🏎️", "Speed Demon!"),
            ("budget_master", "📊", "Budget Master!"),
            ("family_favorite", "👨‍👩‍👧‍👦", "Family Favorite!"),
            ("mega_profit", "💎", "Mega Profit!")
        ]
        
        for key, icon, name in achievement_data:
            if achievements[key]:
                badges_html += f"""
                <div class="achievement-badge" style="margin-bottom: 5px;">
                    <span class="achievement-icon">{icon}</span>
                    <span class="achievement-name">{name}</span>
                </div>
                """
        
        # Wrap all badges in a flex container
        complete_html = f'<div style="display: flex; flex-wrap: wrap;">{badges_html}</div>'
        st.markdown(complete_html, unsafe_allow_html=True)
        
        # Show achievement count
        earned = sum(1 for value in achievements.values() if value)
        st.markdown(f"""
        <p style="margin-top: 10px;">
            You've earned {earned} out of 8 possible achievements!
        </p>
        """, unsafe_allow_html=True)

def display_car_design_controls(game_state, attempts_used, attempts_results, car_designs, car_name=""):
    """Display car design sliders and controls"""
    st.markdown(f"""
    <div class="attempt-counter">
        Attempt {attempts_used + 1} of 3
    </div>
    """, unsafe_allow_html=True)
    
    # More UI components (sliders, etc.)
    # ...

def display_results_panel(result, game_state, car_image_url, car_names, car_taglines, attempts_results, car_designs, tariff_applied):
    """Display the results of market simulation"""
    # Results panel implementation
    # ...

def display_summary(attempts_results, car_designs, car_names, car_taglines, achievements):
    """Display game summary at the end"""
    # Summary implementation
    # ...
