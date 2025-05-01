import streamlit as st
import pandas as pd
import requests
import os
import time
import random  # Added for random market events

# Simulated market data
market_data = pd.DataFrame({
    "Segment": ["Budget", "Family", "Luxury", "Sports", "Eco-Friendly"],
    "Avg_Price": [20000, 30000, 60000, 80000, 35000],
    "Preferred_Speed": [4, 5, 7, 10, 5],
    "Preferred_Aesthetics": [5, 6, 9, 8, 7],
    "Preferred_Reliability": [8, 7, 6, 5, 9],
    "Preferred_Efficiency": [7, 6, 4, 3, 10],
    "Preferred_Tech": [6, 7, 10, 9, 8],
    "Market_Size": [50000, 40000, 15000, 10000, 25000]
})

# Achievement system functions
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
        st.session_state.achievements["sports_king"] = True
        achievements_earned.append({
            "name": "Speed Demon!", 
            "description": "Created a highly profitable sports car",
            "icon": "🏎️"
        })
    
    # Budget Master (profit with low price)
    if not st.session_state.achievements["budget_master"] and result["Best Market Segment"] == "Budget" and result["Profit"] > 50000:
        st.session_state.achievements["budget_master"] = True
        achievements_earned.append({
            "name": "Budget Master!", 
            "description": "Created a profitable budget car",
            "icon": "📊"
        })
    
    # Family Favorite (profit in family segment)
    if not st.session_state.achievements["family_favorite"] and result["Best Market Segment"] == "Family" and result["Profit"] > 50000:
        st.session_state.achievements["family_favorite"] = True
        achievements_earned.append({
            "name": "Family Favorite!", 
            "description": "Created a profitable family car",
            "icon": "👨‍👩‍👧‍👦"
        })
    
    # Mega Profit (profit over 1M)
    if not st.session_state.achievements["mega_profit"] and result["Profit"] > 1000000:
        st.session_state.achievements["mega_profit"] = True
        achievements_earned.append({
            "name": "Mega Profit!", 
            "description": "Made over $1,000,000 profit with a single car",
            "icon": "💎"
        })
    
    return achievements_earned

# Improved market simulation function with random events
def simulate_market_performance(speed, aesthetics, reliability, efficiency, tech, price):
    # Prioritize speed and aesthetics for sports car determination
    is_sports_car = speed >= 8 and aesthetics >= 7
    
    # Calculate scores with adjusted weights to make success easier
    market_data["Score"] = (
        0.8 * abs(market_data["Preferred_Speed"] - speed) +
        0.8 * abs(market_data["Preferred_Aesthetics"] - aesthetics) +
        0.8 * abs(market_data["Preferred_Reliability"] - reliability) +
        0.8 * abs(market_data["Preferred_Efficiency"] - efficiency) +
        0.8 * abs(market_data["Preferred_Tech"] - tech)
    )
    
    # Override for sports cars - ensure high-speed, high-aesthetic cars match with sports segment
    if is_sports_car:
        # Force sports car match by artificially lowering the sports segment score
        sports_idx = market_data[market_data["Segment"] == "Sports"].index[0]
        market_data.at[sports_idx, "Score"] = market_data["Score"].min() - 1
    
    best_match = market_data.loc[market_data["Score"].idxmin()]
    
    # More forgiving price factor
    price_factor = max(0.2, 1 - abs(price - best_match["Avg_Price"]) / best_match["Avg_Price"])
    
    # More generous estimated sales calculation
    estimated_sales = int(best_match["Market_Size"] * (1 - best_match["Score"] / 60) * price_factor)
    
    # Reduced production costs
    cost = (speed * 1500) + (aesthetics * 1200) + (reliability * 1400) + (efficiency * 1300) + (tech * 2000)
    
    profit = estimated_sales * (price - cost)
    
    # Random market event (25% chance)
    market_event = None
    if random.random() < 0.25:
        events = [
            {
                "name": "Fuel Price Spike", 
                "effect": "Fuel prices are up! Efficient cars are in higher demand.", 
                "modifier": lambda p, s, c, seg: (
                    p * 1.3 if seg == "Eco-Friendly" else 
                    p * 0.9 if seg == "Sports" or seg == "Luxury" else 
                    p
                ),
                "sales_modifier": lambda s, e: int(s * (1 + (e * 0.05)))
            },
            {
                "name": "Economic Boom", 
                "effect": "The economy is booming! Luxury and sports cars are selling well.", 
                "modifier": lambda p, s, c, seg: (
                    p * 1.3 if seg == "Luxury" or seg == "Sports" else 
                    p
                ),
                "sales_modifier": lambda s, e: s
            },
            {
                "name": "Safety Concerns", 
                "effect": "Recent accidents have raised safety concerns. Reliable cars are in demand.", 
                "modifier": lambda p, s, c, seg: p * (1 + (reliability * 0.02)),
                "sales_modifier": lambda s, e: s
            },
            {
                "name": "Tech Revolution", 
                "effect": "New tech is trending! High-tech cars are selling better.", 
                "modifier": lambda p, s, c, seg: p * (1 + (tech * 0.015)),
                "sales_modifier": lambda s, e: s
            },
            {
                "name": "New Competition", 
                "effect": "A new competitor has entered your segment, reducing your sales.", 
                "modifier": lambda p, s, c, seg: p * 0.85,
                "sales_modifier": lambda s, e: int(s * 0.85)
            },
            {
                "name": "Celebrity Endorsement", 
                "effect": "A celebrity was seen driving a car like yours! Sales are up.", 
                "modifier": lambda p, s, c, seg: p * 1.2,
                "sales_modifier": lambda s, e: int(s * 1.25)
            }
        ]
        market_event = random.choice(events)
        
        # Apply event effects
        old_profit = profit
        old_sales = estimated_sales
        
        # Apply sales modifier first (some events change sales)
        estimated_sales = market_event["sales_modifier"](estimated_sales, efficiency)
        
        # Then recalculate profit with new sales and any profit modifiers
        profit = market_event["modifier"](profit, estimated_sales, cost, best_match["Segment"])
        
        # Store the changes for display
        market_event["profit_change"] = profit - old_profit
        market_event["sales_change"] = estimated_sales - old_sales
    
    # Generate feedback based on profit
    feedback = ""
    if estimated_sales == 0:
        feedback = "🚨 No sales! Your price is too high for the options you've chosen. Try lowering your price or better matching your car's features to a market segment."
    elif profit < -5000000:
        feedback = "🚨 Significant Loss! Your car is losing money. Try reducing production costs or increasing the price to better match the market."
    elif profit < -1000000:
        feedback = "⚠️ Loss! Consider adjusting your features or price to better appeal to your target market."
    elif profit < -100000:
        feedback = "🔴 Small Loss! You're close to breaking even. A few tweaks to features or price should get you into profitable territory."
    elif profit < 0:
        feedback = "Almost there! Small adjustments to price or features should make your car profitable."
    elif profit < 20000:
        feedback = "⚠️ Breaking Even! Your car is just covering costs. Minor adjustments could improve profitability."
    elif profit < 100000:
        feedback = "✅ Profitable! Your car is making money. Nice work!"
    elif profit < 500000:
        feedback = "🌟 Very Profitable! Great job balancing features and price for this market segment."
    else:
        feedback = "🏆 Extremely Profitable! Outstanding work creating an ideal car for the market!"
    
    return {
        "Feedback": feedback,
        "Best Market Segment": best_match["Segment"],
        "Estimated Sales": estimated_sales,
        "Profit": profit,
        "Cost": cost,
        "Market_Event": market_event
    }

# Function to generate feedback for a profit amount
def get_feedback_for_profit(profit, sales=None):
    if sales == 0 or sales is not None and sales < 10:
        return "🚨 No sales! Your price is too high for the options you've chosen. Try lowering your price or better matching your car's features to a market segment."
    
    if profit < -5000000:
        return "🚨 Significant Loss! Your car is losing money. Try reducing production costs or increasing the price to better match the market."
    elif profit < -1000000:
        return "⚠️ Loss! Consider adjusting your features or price to better appeal to your target market."
    elif profit < -100000:
        return "🔴 Small Loss! You're close to breaking even. A few tweaks to features or price should get you into profitable territory."
    elif profit < 0:
        return "Almost there! Small adjustments to price or features should make your car profitable."
    elif profit < 20000:
        return "⚠️ Breaking Even! Your car is just covering costs. Minor adjustments could improve profitability."
    elif profit < 100000:
        return "✅ Profitable! Your car is making money. Nice work!"
    elif profit < 500000:
        return "🌟 Very Profitable! Great job balancing features and price for this market segment."
    else:
        return "🏆 Extremely Profitable! Outstanding work creating an ideal car for the market!"

# AI image generation function using OpenAI DALL·E
def generate_car_image(speed, aesthetics, reliability, efficiency, tech, price):
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not openai_api_key:
            return "Error: No API Key found."
        
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }
        
        # Improved car type determination that prioritizes speed for sports cars
        car_type = "sports car"
        if speed >= 8 and aesthetics >= 7:
            car_type = "sports car"  # Force sports car if speed and aesthetics are high
        elif price > 60000:
            car_type = "luxury sedan"
        elif price > 25000 and efficiency < 8:
            car_type = "mid-range SUV"
        elif price > 25000 and efficiency >= 8:
            car_type = "eco-friendly SUV"
        elif price > 20000 and efficiency >= 8:
            car_type = "eco-friendly compact"
        else:
            car_type = "budget hatchback"
            
        aesthetics_desc = "plain and basic" if aesthetics <= 3 else "sleek and stylish" if aesthetics <= 7 else "wild and extravagant"
        
        # Enhanced prompt to strongly prevent text in images
        prompt = f"A {car_type} with a {aesthetics_desc} design and funky color palette. The car should match its market segment: a high-performance sports car for extreme speed, a refined luxury sedan for premium comfort, a mid-range SUV for versatility, an eco-friendly SUV for sustainable family travel, an eco-friendly compact for maximum efficiency, or a budget hatchback for affordability. The car should be driving on a winding mountain road. The image should be comic/photorealistic. VERY IMPORTANT: DO NOT INCLUDE ANY TEXT, LETTERS, NUMBERS, WORDS, LABELS, WATERMARKS, LOGOS, OR SYMBOLS OF ANY KIND IN THE IMAGE."
        
        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": "1024x1024",
            "n": 1
        }
        
        response = requests.post("https://api.openai.com/v1/images/generations", json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()["data"][0]["url"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error generating image: {str(e)}"

# Streamlit UI
try:
    st.set_page_config(page_title="Business Administration Car Market Simulation Game", layout="wide", initial_sidebar_state="expanded")
except Exception as e:
    # This means the page config was already set, which is fine
    pass

# Improved CSS with better responsive layout and smaller start button
st.markdown("""
    <style>
    /* Fix for black background on mobile */
    body {
        background-color: #ffffff !important;
    }
    .main .block-container {
        background-color: #ffffff !important;
    }
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* Fix for text color visibility on mobile */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, div, label {
        color: #333333 !important;
    }
    /* Make sure sliders, inputs and other controls have visible text */
    .stSlider label, .stNumberInput label, .stSelectbox label, .stButton label {
        color: #333333 !important;
    }
    /* Make sure all input text is visible */
    input, select, textarea {
        color: #333333 !important;
    }
    /* Specifically fix the price input field */
    .stNumberInput input, .stNumberInput .css-qrbaxs {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
    /* Fix for any input field background colors */
    .css-qrbaxs, .css-zt5igj, input[type="number"], .stNumberInput div[data-baseweb="input"] {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    /* Fix Trump tariff button color scheme - more aggressive approach */
    button[key="apply_tariff"],
    [data-testid="baseButton-secondary"][aria-label="Impose Trump Tariff +25%"],
    div:has(> button:contains("Impose Trump Tariff")),
    button:contains("Trump Tariff"),
    button:contains("Impose Trump"),
    div:has(> span:contains("Impose Trump Tariff")) button {
        background-color: #FF5733 !important;
        color: white !important;
        border-color: #CC4422 !important;
        opacity: 1 !important;
    }
    /* Override Streamlit button colors */
    .stButton button {
        color: white !important;
    }
    /* Make sure the tariff button text is always visible */
    button:contains("Trump") span,
    button:contains("Tariff") span,
    div:has(> button:contains("Trump")) span {
        color: white !important;
    }
    /* Strong dark text for important elements */
    strong, b {
        color: #111111 !important;
    }
    
    .custom-container {
        border: 2px solid #4CAF50;
        padding: 15px;
        border-radius: 10px;
        background-color: #ffffff;
        color: #000000;
        margin-bottom: 20px;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    .custom-container-tariff {
        border: 2px solid #FF5733;
        padding: 15px;
        border-radius: 10px;
        background-color: #fff3e0;
        color: #000000;
        margin-bottom: 20px;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    /* New styles for achievements and market events */
    .achievement-container {
        border: 2px solid #FFD700;
        padding: 15px;
        border-radius: 10px;
        background-color: #FFFDF0;
        color: #000000;
        margin-bottom: 20px;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        animation: glow 1.5s infinite alternate;
    }
    @keyframes glow {
        from {
            box-shadow: 0 0 5px -5px #FFD700;
        }
        to {
            box-shadow: 0 0 10px 5px #FFD700;
        }
    }
    .market-event-container {
        border: 2px solid #9C27B0;
        padding: 15px;
        border-radius: 10px;
        background-color: #F3E5F5;
        color: #000000;
        margin-bottom: 20px;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    .market-event-positive {
        color: #4CAF50 !important;
        font-weight: bold;
    }
    .market-event-negative {
        color: #F44336 !important;
        font-weight: bold;
    }
    .section-divider {
        border-top: 1px solid #ccc;
        margin-top: 10px;
        padding-top: 10px;
    }
    .header-green {
        color: #4CAF50;
    }
    .header-orange {
        color: #FF5733;
    }
    .header-purple {
        color: #9C27B0;
    }
    .header-gold {
        color: #FFD700;
    }
    .instructions-container {
        border: 2px solid #3498db;
        padding: 20px;
        border-radius: 10px;
        background-color: #e8f4f8;
        color: #000000;
        margin-bottom: 20px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    .attempt-counter {
        font-weight: bold;
        color: #3498db;
        font-size: 18px;
        text-align: center;
        margin: 10px 0;
        padding: 10px;
        background-color: #e8f4f8;
        border-radius: 5px;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    .prev-attempt {
        font-size: 14px;
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .centered-header-container {
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .centered-container {
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    /* Significantly smaller start button on desktop with manual size control */
    .small-button {
        max-width: 120px !important;
        margin: 0 auto !important;
        display: block !important;
    }
    .small-button button {
        width: 120px !important;
        min-width: unset !important;
        max-width: 120px !important;
    }
    /* Override Streamlit default button expansion */
    div[data-testid="stButton"] {
        width: auto !important;
    }
    /* Button colors */
    .stButton button {
        font-weight: bold;
        color: white !important;
    }
    /* Primary buttons should always have white text */
    button[kind="primary"], 
    .stButton button[data-baseweb="button"][kind="primary"],
    [data-testid="baseButton-primary"] {
        color: white !important;
    }
    /* Red warning buttons */
    button[kind="secondary"], 
    .stButton button[data-baseweb="button"][kind="secondary"],
    [data-testid="baseButton-secondary"] {
        background-color: #FF5733 !important;
        border-color: #FF5733 !important;
        color: white !important;
    }
    .red-button button {
        background-color: #FF5733 !important;
        border-color: #FF5733 !important;
        color: white !important;
    }
    /* Responsive design */
    @media (max-width: 768px) {
        .hide-on-mobile {
            display: none !important;
        }
        .custom-container, .custom-container-tariff, .instructions-container, .achievement-container, .market-event-container {
            padding: 10px;
        }
        .stButton button {
            width: 100%;
        }
        .small-button {
            max-width: 100%;
        }
    }
    /* Improve settings and results layout */
    .settings-panel {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .results-panel {
        margin-top: 20px;
    }
    .sidebar-placeholder {
        display: none;
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
    /* Achievement badge styles */
    .achievement-badge {
        display: inline-block;
        margin: 5px;
        padding: 8px 15px;
        background-color: #FFD700;
        border-radius: 30px;
        color: #333 !important;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .achievement-icon {
        font-size: 24px;
        margin-right: 8px;
        vertical-align: middle;
    }
    .achievement-name {
        vertical-align: middle;
    }
    /* Achievements panel styles */
    .achievements-panel {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        border: 1px solid #dee2e6;
    }
    .achievement-tab {
        display: inline-block;
        padding: 8px 15px;
        background-color: #e9ecef;
        border-radius: 5px 5px 0 0;
        margin-right: 5px;
        cursor: pointer;
    }
    .achievement-tab.active {
        background-color: #fff;
        border-bottom: 2px solid #4CAF50;
    }
    /* Animated notification for new achievements */
    @keyframes slideIn {
        0% { transform: translateY(-100%); opacity: 0; }
        10% { transform: translateY(0); opacity: 1; }
        90% { transform: translateY(0); opacity: 1; }
        100% { transform: translateY(-100%); opacity: 0; }
    }
    .achievement-notification {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        background-color: #FFD700;
        color: #333 !important;
        padding: 15px 25px;
        border-radius: 50px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        animation: slideIn 4s ease-in-out;
        animation-fill-mode: forwards;
        text-align: center;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 300px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = "instructions"  # States: instructions, playing, game_over
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
# New session state variables for achievements
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

# Function to reset the game
def reset_game():
    st.session_state.game_state = "instructions"
    st.session_state.result = None
    st.session_state.car_image_url = None
    st.session_state.tariff_applied = False
    st.session_state.attempts_used = 0
    st.session_state.attempts_results = []
    st.session_state.car_designs = []
    st.session_state.new_achievements = []
    # Note: we don't reset achievements when starting a new game

# Logo and header in the same row
logo_path = "logo.png"  # Replace with the actual logo file path

# Create centered container for the header
st.markdown('<div style="max-width: 900px; margin: 0 auto; padding: 10px;">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 5])
with col1:
    try:
        st.image(logo_path, width=100)
    except:
        pass  # Skip if logo doesn't load
with col2:
    st.markdown("<h1 style='margin-top: 25px;'>Business Administration Car Market Simulation Game</h1>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Show any new achievements notifications
if st.session_state.new_achievements:
    # Display the newest achievement notification
    achievement = st.session_state.new_achievements[0]
    st.markdown(f"""
    <div class="achievement-notification">
        <span style="font-size: 28px; margin-right: 10px;">{achievement['icon']}</span>
        <div>
            <div style="font-size: 18px;">Achievement Unlocked!</div>
            <div>{achievement['name']} {achievement['description']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Clear the notifications after displaying
    st.session_state.new_achievements = []

# Instructions screen
if st.session_state.game_state == "instructions":
    st.markdown("""
    <div class="instructions-container">
        <h2 style="color: #3498db; text-align: center;">Welcome to the Car Market Simulator!</h2>
        <hr>
        <h3>Game Instructions:</h3>
        <ol>
            <li><strong>Objective:</strong> Design a profitable car by adjusting its features and price.</li>
            <li><strong>You have 3 attempts</strong> to create a profitable car design.</li>
            <li>Customize your car's specifications using the sliders.</li>
            <li>Click "Simulate Market" to see how your car performs.</li>
            <li>Learn from each attempt and adjust your strategy.</li>
            <li>Watch for <span style="color: #9C27B0; font-weight: bold;">Random Market Events</span> that can affect your profits!</li>
            <li>Earn <span style="color: #FFD700; font-weight: bold;">Achievements</span> by reaching specific milestones.</li>
            <li>After your third attempt, you'll see an AI-generated image of your final car design.</li>
            <li>The "Impose Trump Tariff" button lets you see how a 25% tariff would affect your profits.</li>
        </ol>
        <p style="text-align: center; font-weight: bold;">Good luck with your car design!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Using a more aggressive approach with columns to constrain button width
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
        st.rerun()

    # Show achievements panel if user has earned any
    if st.session_state.total_achievements_earned > 0:
        with st.expander("📊 Your Achievements", expanded=False):
            st.markdown("""
            <h3 style="color: #FFD700; text-align: center;">🏆 Your Achievements 🏆</h3>
            <p style="text-align: center;">Achievements you've earned across all games</p>
            """, unsafe_allow_html=True)
            
            # Display earned achievements
            achievement_html = "<div style='display: flex; flex-wrap: wrap; justify-content: center;'>"
            
            if st.session_state.achievements["first_profit"]:
                achievement_html += """
                <div class="achievement-badge">
                    <span class="achievement-icon">💰</span>
                    <span class="achievement-name">First Profit!</span>
                </div>
                """
            
            if st.session_state.achievements["big_seller"]:
                achievement_html += """
                <div class="achievement-badge">
                    <span class="achievement-icon">🚗</span>
                    <span class="achievement-name">Big Seller!</span>
                </div>
                """
                
            if st.session_state.achievements["luxury_master"]:
                achievement_html += """
                <div class="achievement-badge">
                    <span class="achievement-icon">👑</span>
                    <span class="achievement-name">Luxury Master!</span>
                </div>
                """
                
            if st.session_state.achievements["eco_genius"]:
                achievement_html += """
                <div class="achievement-badge">
                    <span class="achievement-icon">🌱</span>
                    <span class="achievement-name">Eco Genius!</span>
                </div>
                """
                
            if st.session_state.achievements["sports_king"]:
                achievement_html += """
                <div class="achievement-badge">
                    <span class="achievement-icon">🏎️</span>
                    <span class="achievement-name">Speed Demon!</span>
                </div>
                """
                
            if st.session_state.achievements["budget_master"]:
                achievement_html += """
                <div class="achievement-badge">
                    <span class="achievement-icon">📊</span>
                    <span class="achievement-name">Budget Master!</span>
                </div>
                """
                
            if st.session_state.achievements["family_favorite"]:
                achievement_html += """
                <div class="achievement-badge">
                    <span class="achievement-icon">👨‍👩‍👧‍👦</span>
                    <span class="achievement-name">Family Favorite!</span>
                </div>
                """
                
            if st.session_state.achievements["mega_profit"]:
                achievement_html += """
                <div class="achievement-badge">
                    <span class="achievement-icon">💎</span>
                    <span class="achievement-name">Mega Profit!</span>
                </div>
                """
                
            achievement_html += "</div>"
            st.markdown(achievement_html, unsafe_allow_html=True)
            
            # Show achievement count
            st.markdown(f"""
            <p style="text-align: center; margin-top: 15px;">
                You've earned {st.session_state.total_achievements_earned} out of 8 possible achievements!
            </p>
            """, unsafe_allow_html=True)

# Playing the game or game over state
elif st.session_state.game_state == "playing" or st.session_state.game_state == "game_over":
    # Use a two-column layout for the main game interface
    main_col1, main_col2 = st.columns([1, 2])
    
    # Left column for car design controls
    with main_col1:
        st.markdown(f"""
        <div class="attempt-counter">
            Attempt {st.session_state.attempts_used + 1} of 3
        </div>
        """, unsafe_allow_html=True)
        
        # Show previous attempts 
        if len(st.session_state.attempts_results) > 0:
            st.markdown("### Previous Attempts")
            for i, (design, result) in enumerate(zip(st.session_state.car_designs, st.session_state.attempts_results)):
                with st.expander(f"Attempt {i+1}: ${result['Profit']:,}"):
                    st.write(f"**Market:** {result['Best Market Segment']}")
                    st.write(f"**Sales:** {result['Estimated Sales']} units")
                    st.write(f"**Settings:** Speed: {design['Speed']}, Aesthetics: {design['Aesthetics']}, " +
                            f"Reliability: {design['Reliability']}, Efficiency: {design['Efficiency']}, " +
                            f"Tech: {design['Tech']}, Price: ${design['Price']:,}")
                    
                    # Show market event if there was one
                    if result.get('Market_Event'):
                        event = result['Market_Event']
                        st.markdown(f"""
                        <div style="margin-top: 10px; padding: 5px 10px; background-color: #f3e5f5; border-radius: 5px;">
                            <strong style="color: #9C27B0;">📢 Market Event:</strong> {event['name']} - {event['effect']}
                        </div>
                        """, unsafe_allow_html=True)
        
        # Design inputs
        st.markdown("### Customize Your Car")
        
        # If we have previous attempts, use the best one as a starting point
        default_speed = 5
        default_aesthetics = 5
        default_reliability = 5
        default_efficiency = 5
        default_tech = 5
        default_price = 30000
        
        if len(st.session_state.attempts_results) > 0:
            # Find best previous attempt
            profits = [result['Profit'] for result in st.session_state.attempts_results]
            best_idx = profits.index(max(profits))
            best_design = st.session_state.car_designs[best_idx]
            
            default_speed = best_design['Speed']
            default_aesthetics = best_design['Aesthetics']
            default_reliability = best_design['Reliability']
            default_efficiency = best_design['Efficiency'] 
            default_tech = best_design['Tech']
            default_price = best_design['Price']
        
        disabled = st.session_state.game_state == "game_over"
        
        with st.container():
            st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
            speed = st.slider("Speed", 1, 10, default_speed, disabled=disabled, 
                             help="Higher speed increases cost but appeals to Sports segment")
            aesthetics = st.slider("Aesthetics", 1, 10, default_aesthetics, disabled=disabled,
                                 help="Higher aesthetics increases cost but appeals to Luxury segment")
            reliability = st.slider("Reliability", 1, 10, default_reliability, disabled=disabled,
                                  help="Higher reliability increases cost but appeals to Budget segment")
            efficiency = st.slider("Fuel Efficiency", 1, 10, default_efficiency, disabled=disabled,
                                 help="Higher efficiency increases cost but appeals to Eco-Friendly segment")
            tech = st.slider("Technology", 1, 10, default_tech, disabled=disabled,
                           help="Higher tech increases cost but appeals to Luxury & Sports segments")
            price = st.number_input("Price ($)", min_value=10000, max_value=200000, value=default_price, step=1000, disabled=disabled)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Simulate market button (only show during playing state)
            if st.session_state.game_state == "playing":
                sim_button = st.button("Simulate Market", type="primary")
                if sim_button:
                    with st.spinner("Simulating market performance..."):
                        # Reset tariff state when simulating new market
                        st.session_state.tariff_applied = False
                        
                        # Store design for future reference
                        st.session_state.car_designs.append({
                            "Speed": speed,
                            "Aesthetics": aesthetics, 
                            "Reliability": reliability,
                            "Efficiency": efficiency,
                            "Tech": tech,
                            "Price": price
                        })
                        
                        # Simulate market
                        st.session_state.result = simulate_market_performance(speed, aesthetics, reliability, efficiency, tech, price)
                        st.session_state.attempts_results.append(st.session_state.result)
                        st.session_state.attempts_used += 1
                        
                        # Check for achievements
                        new_achievements = check_achievements(st.session_state.result, st.session_state.car_designs[-1])
                        if new_achievements:
                            st.session_state.new_achievements = new_achievements
                            st.session_state.total_achievements_earned += len(new_achievements)
                        
                        # Generate AI image only on final attempt
                        if st.session_state.attempts_used >= 3:
                            st.session_state.car_image_url = generate_car_image(speed, aesthetics, reliability, efficiency, tech, price)
                            st.session_state.game_state = "game_over"
                        
                        st.rerun()
        
        # Show achievements in sidebar on game screen
        if sum(1 for value in st.session_state.achievements.values() if value) > 0:
            st.markdown("### 🏆 Your Achievements")
            achievement_html = "<div style='display: flex; flex-wrap: wrap;'>"
            
            if st.session_state.achievements["first_profit"]:
                achievement_html += """
                <div class="achievement-badge" style="margin-bottom: 5px;">
                    <span class="achievement-icon">💰</span>
                    <span class="achievement-name">First Profit!</span>
                </div>
                """
            
            if st.session_state.achievements["big_seller"]:
                achievement_html += """
                <div class="achievement-badge" style="margin-bottom: 5px;">
                    <span class="achievement-icon">🚗</span>
                    <span class="achievement-name">Big Seller!</span>
                </div>
                """
                
            if st.session_state.achievements["luxury_master"]:
                achievement_html += """
                <div class="achievement-badge" style="margin-bottom: 5px;">
                    <span class="achievement-icon">👑</span>
                    <span class="achievement-name">Luxury Master!</span>
                </div>
                """
                
            if st.session_state.achievements["eco_genius"]:
                achievement_html += """
                <div class="achievement-badge" style="margin-bottom: 5px;">
                    <span class="achievement-icon">🌱</span>
                    <span class="achievement-name">Eco Genius!</span>
                </div>
                """
                
            if st.session_state.achievements["sports_king"]:
                achievement_html += """
                <div class="achievement-badge" style="margin-bottom: 5px;">
                    <span class="achievement-icon">🏎️</span>
                    <span class="achievement-name">Speed Demon!</span>
                </div>
                """
                
            if st.session_state.achievements["budget_master"]:
                achievement_html += """
                <div class="achievement-badge" style="margin-bottom: 5px;">
                    <span class="achievement-icon">📊</span>
                    <span class="achievement-name">Budget Master!</span>
                </div>
                """
                
            if st.session_state.achievements["family_favorite"]:
                achievement_html += """
                <div class="achievement-badge" style="margin-bottom: 5px;">
                    <span class="achievement-icon">👨‍👩‍👧‍👦</span>
                    <span class="achievement-name">Family Favorite!</span>
                </div>
                """
                
            if st.session_state.achievements["mega_profit"]:
                achievement_html += """
                <div class="achievement-badge" style="margin-bottom: 5px;">
                    <span class="achievement-icon">💎</span>
                    <span class="achievement-name">Mega Profit!</span>
                </div>
                """
                
            achievement_html += "</div>"
            st.markdown(achievement_html, unsafe_allow_html=True)
            
            # Show achievement count
            earned = sum(1 for value in st.session_state.achievements.values() if value)
            st.markdown(f"""
            <p style="margin-top: 10px;">
                You've earned {earned} out of 8 possible achievements!
            </p>
            """, unsafe_allow_html=True)
    
    # Right column for results display
    with main_col2:
        st.markdown('<div class="results-panel">', unsafe_allow_html=True)
        
        # Display results if we have them
        if st.session_state.result is not None:
            try:
                # Display car image only on final attempt if available
                if st.session_state.game_state == "game_over" and st.session_state.car_image_url and "Error" not in st.session_state.car_image_url:
                    try:
                        # Add attractive box about AI-generated image with better contrast
                        st.markdown("""
                        <div style="background-color: #3498db; color: white; padding: 12px; 
                        border-radius: 5px; text-align: center; margin-bottom: 10px; font-weight: bold;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                        ✨ This image is uniquely generated by AI based on your chosen customization ✨
                        </div>
                        """, unsafe_allow_html=True)
                        st.image(st.session_state.car_image_url, use_container_width=True)
                    except:
                        st.write("Unable to display car image")
                
                # Show attempts left or final status
                if st.session_state.game_state == "playing":
                    attempts_left = 3 - st.session_state.attempts_used
                    st.markdown(f"<div class='attempt-counter'>You have {attempts_left} attempt{'s' if attempts_left != 1 else ''} left</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='attempt-counter'>Final Result</div>", unsafe_allow_html=True)
                
                # Display results
                result = st.session_state.result
                st.markdown(f"""
                <div class="custom-container">
                    <h2 class="header-green">📊 Market Simulation Results</h2>
                    <p><strong>Best Market Segment:</strong> {result['Best Market Segment']}</p>
                    <p><strong>Estimated Sales:</strong> {result['Estimated Sales']} units</p>
                    <p><strong>Estimated Profit:</strong> ${result['Profit']:,}</p>
                    <div class="section-divider">
                        <h3 class="header-orange">💡 Profit Feedback</h3>
                        <p>{result['Feedback']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display market event if one occurred
                if result.get('Market_Event'):
                    event = result['Market_Event']
                    profit_change_class = "market-event-positive" if event['profit_change'] >= 0 else "market-event-negative"
                    sales_change_class = "market-event-positive" if event.get('sales_change', 0) >= 0 else "market-event-negative"
                    
                    # Format change indicators with plus sign for positive changes
                    profit_change_str = f"+${event['profit_change']:,}" if event['profit_change'] >= 0 else f"-${abs(event['profit_change']):,}"
                    sales_change_str = f"+{event['sales_change']}" if event.get('sales_change', 0) >= 0 else f"-{abs(event['sales_change'])}"
                    
                    st.markdown(f"""
                    <div class="market-event-container">
                        <h2 class="header-purple">📢 Market Event!</h2>
                        <h3>{event['name']}</h3>
                        <p><strong>Effect:</strong> {event['effect']}</p>
                        <div class="section-divider">
                            <p><strong>Impact on Profit:</strong> <span class="{profit_change_class}">{profit_change_str}</span></p>
                            {f'<p><strong>Impact on Sales:</strong> <span class="{sales_change_class}">{sales_change_str} units</span></p>' if event.get('sales_change') != 0 else ''}
                        </div>
                        <p style="font-style: italic; margin-top: 10px;">Market events occur randomly and can help or hinder your car's performance!</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display tariff information if it has been applied
                if st.session_state.tariff_applied:
                    tariffed_cost = st.session_state.result['Cost'] * 1.25  # Adding 25% tariff
                    latest_design = st.session_state.car_designs[-1]
                    tariffed_profit = st.session_state.result['Estimated Sales'] * (latest_design['Price'] - tariffed_cost)
                    tariffed_feedback = get_feedback_for_profit(tariffed_profit, st.session_state.result['Estimated Sales'])
                    
                    st.markdown(f"""
                    <div class="custom-container-tariff">
                        <h2 class="header-orange">📊 Updated Market Results (After Tariff)</h2>
                        <p><strong>Best Market Segment:</strong> {st.session_state.result['Best Market Segment']}</p>
                        <p><strong>Estimated Sales:</strong> {st.session_state.result['Estimated Sales']} units</p>
                        <p><strong>Original Profit:</strong> ${st.session_state.result['Profit']:,}</p>
                        <p><strong>New Estimated Profit:</strong> ${tariffed_profit:,.2f}</p>
                        <p><strong>Profit Change:</strong> ${tariffed_profit - st.session_state.result['Profit']:,.2f}</p>
                        <div class="section-divider">
                            <h3 class="header-orange">💡 Updated Profit Feedback</h3>
                            <p>{tariffed_feedback}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Game over summary at the end
                if st.session_state.game_state == "game_over":
                    # Calculate best attempt
                    profits = [result['Profit'] for result in st.session_state.attempts_results]
                    best_attempt_index = profits.index(max(profits))
                    best_attempt = st.session_state.attempts_results[best_attempt_index]
                    best_design = st.session_state.car_designs[best_attempt_index]
                    
                    st.markdown("""
                    <div class="section-divider"></div>
                    <h2 style="text-align: center; margin-top: 20px;">Game Summary</h2>
                    """, unsafe_allow_html=True)
                    
                    # Best design callout
                    st.markdown(f"""
                    <div style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; border: 2px solid #3498db; margin-bottom: 20px;">
                        <h3 style="color: #3498db; text-align: center;">🏆 Best Performing Design: Attempt {best_attempt_index+1}</h3>
                        <p><strong>Profit:</strong> ${best_attempt['Profit']:,}</p>
                        <p><strong>Market Segment:</strong> {best_attempt['Best Market Segment']}</p>
                        <p><strong>Settings:</strong> Speed: {best_design['Speed']}, Aesthetics: {best_design['Aesthetics']}, 
                        Reliability: {best_design['Reliability']}, Efficiency: {best_design['Efficiency']}, 
                        Tech: {best_design['Tech']}, Price: ${best_design['Price']:,}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create a DataFrame for the summary
                    import pandas as pd
                    summary_data = []
                    for i, (design, result) in enumerate(zip(st.session_state.car_designs, st.session_state.attempts_results)):
                        is_best = i == best_attempt_index
                        best_badge = "🏆 " if is_best else ""
                        
                        # Add market event indicator if there was one
                        event_badge = "📢 " if result.get('Market_Event') else ""
                        
                        summary_data.append({
                            "Attempt": f"{best_badge}{event_badge}Attempt {i+1}",
                            "Market Segment": result['Best Market Segment'],
                            "Sales": result['Estimated Sales'],
                            "Profit": f"${result['Profit']:,}",
                            "Speed": design['Speed'],
                            "Aesthetics": design['Aesthetics'],
                            "Reliability": design['Reliability'],
                            "Efficiency": design['Efficiency'],
                            "Tech": design['Tech'],
                            "Price": f"${design['Price']:,}"
                        })
                    
                    summary_df = pd.DataFrame(summary_data)
                    
                    # Display the summary table
                    st.markdown("### All Attempts Comparison")
                    st.dataframe(summary_df, use_container_width=True)
                    
                    # Achievements earned summary
                    earned_achievements = sum(1 for value in st.session_state.achievements.values() if value)
                    if earned_achievements > 0:
                        st.markdown(f"""
                        <h3 class="header-gold" style="text-align: center; margin-top: 20px;">🏆 Achievements Earned: {earned_achievements}/8 🏆</h3>
                        """, unsafe_allow_html=True)
                        
                        achievement_html = "<div style='display: flex; flex-wrap: wrap; justify-content: center;'>"
                        
                        if st.session_state.achievements["first_profit"]:
                            achievement_html += """
                            <div class="achievement-badge">
                                <span class="achievement-icon">💰</span>
                                <span class="achievement-name">First Profit!</span>
                            </div>
                            """
                        
                        if st.session_state.achievements["big_seller"]:
                            achievement_html += """
                            <div class="achievement-badge">
                                <span class="achievement-icon">🚗</span>
                                <span class="achievement-name">Big Seller!</span>
                            </div>
                            """
                            
                        if st.session_state.achievements["luxury_master"]:
                            achievement_html += """
                            <div class="achievement-badge">
                                <span class="achievement-icon">👑</span>
                                <span class="achievement-name">Luxury Master!</span>
                            </div>
                            """
                            
                        if st.session_state.achievements["eco_genius"]:
                            achievement_html += """
                            <div class="achievement-badge">
                                <span class="achievement-icon">🌱</span>
                                <span class="achievement-name">Eco Genius!</span>
                            </div>
                            """
                            
                        if st.session_state.achievements["sports_king"]:
                            achievement_html += """
                            <div class="achievement-badge">
                                <span class="achievement-icon">🏎️</span>
                                <span class="achievement-name">Speed Demon!</span>
                            </div>
                            """
                            
                        if st.session_state.achievements["budget_master"]:
                            achievement_html += """
                            <div class="achievement-badge">
                                <span class="achievement-icon">📊</span>
                                <span class="achievement-name">Budget Master!</span>
                            </div>
                            """
                            
                        if st.session_state.achievements["family_favorite"]:
                            achievement_html += """
                            <div class="achievement-badge">
                                <span class="achievement-icon">👨‍👩‍👧‍👦</span>
                                <span class="achievement-name">Family Favorite!</span>
                            </div>
                            """
                            
                        if st.session_state.achievements["mega_profit"]:
                            achievement_html += """
                            <div class="achievement-badge">
                                <span class="achievement-icon">💎</span>
                                <span class="achievement-name">Mega Profit!</span>
                            </div>
                            """
                            
                        achievement_html += "</div>"
                        st.markdown(achievement_html, unsafe_allow_html=True)
                        
                        remaining = 8 - earned_achievements
                        if remaining > 0:
                            st.markdown(f"""
                            <p style="text-align: center; margin-top: 10px;">
                                {remaining} more achievements still to unlock! Play again to collect them all.
                            </p>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <p style="text-align: center; margin-top: 10px; font-weight: bold; color: #FFD700;">
                                🎉 Congratulations! You've unlocked all achievements! 🎉
                            </p>
                            """, unsafe_allow_html=True)
                    
                    # Educational message about relevant courses
                    st.markdown("""
                    <div style="background-color: #e6f7ff; padding: 15px; border-radius: 10px; border: 2px solid #1890ff; margin: 20px 0;">
                        <h3 style="color: #1890ff; margin-top: 0;">📚 Educational Note</h3>
                        <p>Taking courses at Coast Mountain College such as <strong>Introduction to Marketing</strong> and <strong>Business Finance</strong> would help you understand markets and how to price products accordingly!</p>
                        <p>Interested in more information? Visit the <a href="https://coastmountaincollege.ca/programs/study/business" target="_blank">Coast Mountain College Business Administration website</a></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Tariff button after 3rd attempt if not already applied
                    col1, col2 = st.columns(2)
                    with col1:
                        if not st.session_state.tariff_applied:
                            # Fix for tariff button disappearing
                            tariff_button = st.button(
                                "Impose Trump Tariff +25%", 
                                key="apply_tariff",
                                type="secondary"
                            )
                            if tariff_button:
                                st.session_state.tariff_applied = True
                                st.rerun()
                                st.session_state.tariff_applied = True
                                st.rerun()
                    
                    with col2:
                        # New game button
                        if st.button("Start New Game", key="new_game_button", type="primary"):
                            reset_game()
                            st.rerun()
            
            except Exception as e:
                st.error(f"Error displaying results: {str(e)}")
        
        # Show a placeholder message if no results to display yet
        else:
            st.markdown("""
            <div style="text-align: center; padding: 30px; background-color: #f5f5f5; border-radius: 10px;">
                <h3>Your results will appear here</h3>
                <p>Adjust the car settings on the left and click "Simulate Market" to see how your design performs.</p>
                <p style="margin-top: 15px; font-weight: bold; color: #9C27B0;">Watch for random market events that can affect your car's performance!</p>
                <p style="font-weight: bold; color: #FFD700;">Earn achievements by reaching special milestones!</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
