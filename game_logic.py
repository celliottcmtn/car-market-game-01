# game_logic.py
import streamlit as st
import random

def initialize_session_state():
    """Initialize the session state variables if they don't exist."""
    if 'game_state' not in st.session_state:
        st.session_state.game_state = "instructions"
    
    if 'max_attempts' not in st.session_state:
        st.session_state.max_attempts = 5
    
    if 'attempts_used' not in st.session_state:
        st.session_state.attempts_used = 0
    
    if 'attempts_results' not in st.session_state:
        st.session_state.attempts_results = []
    
    if 'car_designs' not in st.session_state:
        st.session_state.car_designs = []
    
    if 'car_names' not in st.session_state:
        st.session_state.car_names = []
    
    if 'car_taglines' not in st.session_state:
        st.session_state.car_taglines = []
    
    if 'total_achievements_earned' not in st.session_state:
        st.session_state.total_achievements_earned = 0
    
    if 'new_achievements' not in st.session_state:
        st.session_state.new_achievements = []
    
    if 'achievements' not in st.session_state:
        st.session_state.achievements = [
            {
                'name': 'First Launch',
                'description': 'Launch your first car',
                'requirement': 'Launch 1 car',
                'earned': False
            },
            {
                'name': 'Million Dollar Car',
                'description': 'Make $1M+ profit on a single car',
                'requirement': 'Make $1M profit on one car',
                'earned': False
            },
            {
                'name': 'Balanced Design',
                'description': 'Design a car with all attributes at 5+',
                'requirement': 'All design attributes 5 or higher',
                'earned': False
            },
            {
                'name': 'Luxury Expert',
                'description': 'Design a car with 9+ comfort and style',
                'requirement': 'Comfort and Style both 9 or higher',
                'earned': False
            },
            {
                'name': 'Performance Beast',
                'description': 'Design a car with 9+ performance',
                'requirement': 'Performance 9 or higher',
                'earned': False
            }
        ]

def reset_game():
    """Reset the game to start a new round."""
    st.session_state.game_state = "instructions"
    st.session_state.attempts_used = 0
    st.session_state.attempts_results = []
    st.session_state.car_designs = []
    st.session_state.car_names = []
    st.session_state.car_taglines = []
    # Don't reset achievements

def simulate_market(car_design):
    """Simulate market response to a car design."""
    # Extract car attributes
    performance = car_design['performance']
    efficiency = car_design['efficiency']
    comfort = car_design['comfort']
    style = car_design['style']
    price = car_design['price']
    
    # Calculate base appeal (higher is better)
    base_appeal = (performance + efficiency + comfort + style) / 4
    
    # Price adjustment (too expensive reduces appeal, too cheap might too)
    ideal_price = 10000 + (performance + efficiency + comfort + style) * 2500
    price_factor = 1.0 - abs(price - ideal_price) / ideal_price
    price_factor = max(0.5, min(price_factor, 1.5))
    
    # Final appeal calculation
    appeal = base_appeal * price_factor
    
    # Add some randomness to simulate market fluctuations
    market_randomness = random.uniform(0.8, 1.2)
    appeal *= market_randomness
    
    # Calculate sales (higher appeal = more sales)
    base_sales = appeal * 1000
    sales = int(base_sales)
    
    # Calculate revenue
    revenue = sales * price
    
    # Calculate costs (higher attributes = higher costs)
    cost_per_unit = 5000 + (performance * 800) + (efficiency * 600) + (comfort * 700) + (style * 500)
    total_cost = sales * cost_per_unit
    
    # Calculate profit
    profit = revenue - total_cost
    
    # Calculate market share (simplified)
    market_share = appeal * 2
    
    # Generate feedback based on design and results
    feedback = generate_feedback(car_design, appeal, price_factor)
    
    # Check achievements
    check_achievements(car_design, profit)
    
    # Return the results
    return {
        'sales': sales,
        'revenue': revenue,
        'profit': profit,
        'market_share': market_share,
        'feedback': feedback
    }

def generate_feedback(car_design, appeal, price_factor):
    """Generate feedback text based on car design and market appeal."""
    feedback = []
    
    # Appeal feedback
    if appeal >= 8:
        feedback.append("The market absolutely loves your car! Customers are raving about it!")
    elif appeal >= 6:
        feedback.append("Your car is well-received in the market. Good job!")
    elif appeal >= 4:
        feedback.append("Your car is doing okay, but doesn't stand out from the competition.")
    else:
        feedback.append("Customers are showing little interest in your car. It needs improvement.")
    
    # Price feedback
    if price_factor < 0.7:
        feedback.append("The price seems completely disconnected from what the car offers.")
    elif price_factor < 0.9:
        feedback.append("The price doesn't quite match the value proposition.")
    elif price_factor > 1.3:
        feedback.append("You've priced this very competitively, perhaps too low for what it offers.")
    
    # Attribute-specific feedback
    attributes = [
        ('performance', car_design['performance'], "Performance"),
        ('efficiency', car_design['efficiency'], "Efficiency"),
        ('comfort', car_design['comfort'], "Comfort"),
        ('style', car_design['style'], "Style")
    ]
    
    # Find the highest and lowest attributes
    highest = max(attributes, key=lambda x: x[1])
    lowest = min(attributes, key=lambda x: x[1])
    
    if highest[1] >= 8:
        feedback.append(f"Customers particularly love the {highest[2].lower()} of your car.")
    
    if lowest[1] <= 3:
        feedback.append(f"The {lowest[2].lower()} has been criticized by customers and reviewers.")
    
    return " ".join(feedback)

def check_achievements(car_design, profit):
    """Check if any achievements have been unlocked."""
    achievements = st.session_state.achievements
    new_achievements = []
    
    # First Launch achievement
    if len(st.session_state.car_designs) == 0 and not achievements[0]['earned']:
        achievements[0]['earned'] = True
        new_achievements.append(achievements[0])
    
    # Million Dollar Car achievement
    if profit >= 1000000 and not achievements[1]['earned']:
        achievements[1]['earned'] = True
        new_achievements.append(achievements[1])
    
    # Balanced Design achievement
    if (car_design['performance'] >= 5 and
        car_design['efficiency'] >= 5 and
        car_design['comfort'] >= 5 and
        car_design['style'] >= 5 and
        not achievements[2]['earned']):
        achievements[2]['earned'] = True
        new_achievements.append(achievements[2])
    
    # Luxury Expert achievement
    if (car_design['comfort'] >= 9 and
        car_design['style'] >= 9 and
        not achievements[3]['earned']):
        achievements[3]['earned'] = True
        new_achievements.append(achievements[3])
    
    # Performance Beast achievement
    if car_design['performance'] >= 9 and not achievements[4]['earned']:
        achievements[4]['earned'] = True
        new_achievements.append(achievements[4])
    
    # Update total achievements count
    st.session_state.total_achievements_earned = sum(1 for a in achievements if a['earned'])
    
    # Add new achievements to be displayed
    st.session_state.new_achievements.extend(new_achievements)
