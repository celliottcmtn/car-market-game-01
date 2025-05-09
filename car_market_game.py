import streamlit as st
import pandas as pd
import requests
import os
import time
from io import BytesIO
from PIL import Image

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

# Market simulation function
def simulate_market_performance(speed, aesthetics, reliability, efficiency, tech, price):
    market_data["Score"] = (
        abs(market_data["Preferred_Speed"] - speed) +
        abs(market_data["Preferred_Aesthetics"] - aesthetics) +
        abs(market_data["Preferred_Reliability"] - reliability) +
        abs(market_data["Preferred_Efficiency"] - efficiency) +
        abs(market_data["Preferred_Tech"] - tech)
    )
    best_match = market_data.loc[market_data["Score"].idxmin()]
    
    price_factor = max(0, 1 - abs(price - best_match["Avg_Price"]) / best_match["Avg_Price"])
    estimated_sales = int(best_match["Market_Size"] * (1 - best_match["Score"] / 50) * price_factor)
    cost = (speed * 2000) + (aesthetics * 1500) + (reliability * 1800) + (efficiency * 1700) + (tech * 2500)
    profit = estimated_sales * (price - cost)
    
    feedback = ""
    if estimated_sales == 0:
        feedback = "No sales! Your price is too high for the options you've chosen. Try lowering your price or better matching your car's features to a market segment."
    elif profit < -10000000:
        feedback = "Catastrophic Loss! Your car is losing an extreme amount of money. You need to **completely rethink** your strategy—reduce production costs, increase the price, and make sure your car matches the right market segment."
    elif profit < -1000000:
        feedback = "Huge Loss! Your losses are very high. Consider making significant adjustments—lowering expensive features, improving efficiency, or adjusting pricing to better fit the market."
    elif profit < -100000:
        feedback = "Major Loss! Your car is losing a significant amount of money. You need to make drastic changes—consider lowering production costs, increasing the price, or improving the balance of features to appeal to buyers."
    elif profit < -50000:
        feedback = "Moderate Loss! Your car is losing money. Try reducing unnecessary costs, adjusting the price, or making the car more appealing to its target market."
    elif profit < 0:
        feedback = "Your car is losing money. Consider increasing the price or reducing costs by adjusting features like speed, aesthetics, or technology."
    elif profit < 20000:
        feedback = "Low Profit! Your profit is minimal. Consider small adjustments to your price or features to make your car more appealing."
    elif profit < 50000:
        feedback = "Your profit is low. Try optimizing your price or enhancing the car's appeal to boost sales."
    else:
        feedback = "Your car is profitable! Maintain a balance between cost and market demand for even better results."
    
    return {
        "Feedback": feedback,
        "Best Market Segment": best_match["Segment"],
        "Estimated Sales": estimated_sales,
        "Profit": profit,
        "Cost": cost
    }

# Function to generate feedback for a profit amount
def get_feedback_for_profit(profit, sales=None):
    if sales == 0 or sales is not None and sales < 10:
        return "No sales! Your price is too high for the options you've chosen. Try lowering your price or better matching your car's features to a market segment."
    
    if profit < -10000000:
        return "Catastrophic Loss! Your car is losing an extreme amount of money. You need to **completely rethink** your strategy—reduce production costs, increase the price, and make sure your car matches the right market segment."
    elif profit < -1000000:
        return "Huge Loss! Your losses are very high. Consider making significant adjustments—lowering expensive features, improving efficiency, or adjusting pricing to better fit the market."
    elif profit < -100000:
        return "Major Loss! Your car is losing a significant amount of money. You need to make drastic changes—consider lowering production costs, increasing the price, or improving the balance of features to appeal to buyers."
    elif profit < -50000:
        return "Moderate Loss! Your car is losing money. Try reducing unnecessary costs, adjusting the price, or making the car more appealing to its target market."
    elif profit < 0:
        return "Your car is losing money. Consider increasing the price or reducing costs by adjusting features like speed, aesthetics, or technology."
    elif profit < 20000:
        return "Low Profit! Your profit is minimal. Consider small adjustments to your price or features to make your car more appealing."
    elif profit < 50000:
        return "Your profit is low. Try optimizing your price or enhancing the car's appeal to boost sales."
    else:
        return "Your car is profitable! Maintain a balance between cost and market demand for even better results."

# AI image generation function using OpenAI DALL·E - IMPROVED ERROR HANDLING
def generate_car_image(speed, aesthetics, reliability, efficiency, tech, price):
    try:
        # Try to get API key from Streamlit secrets first, then environment variable
        if hasattr(st, 'secrets') and 'openai_api_key' in st.secrets:
            openai_api_key = st.secrets['openai_api_key']
        else:
            openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not openai_api_key:
            print("No OpenAI API key found")
            return "Error: No API Key found. Check Streamlit secrets or environment variables."
        
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }
        
        # Enhanced prompt to strongly prevent text in images
        prompt = f"A {'sports car' if price > 80000 else 'luxury sedan' if price > 60000 else 'mid-range SUV' if price > 25000 and efficiency < 8 else 'eco-friendly SUV' if price > 25000 and efficiency >= 8 else 'eco-friendly compact' if price > 20000 and efficiency >= 8 else 'budget hatchback'} with a {'plain and basic' if aesthetics <= 3 else 'sleek and stylish' if aesthetics <= 7 else 'wild and extravagant'} design and funky color palette. The car should match its market segment: a high-performance sports car for extreme speed, a refined luxury sedan for premium comfort, a mid-range SUV for versatility, an eco-friendly SUV for sustainable family travel, an eco-friendly compact for maximum efficiency, or a budget hatchback for affordability. The car should be driving on a winding mountain road. The image should be comic/photorealistic. VERY IMPORTANT: DO NOT INCLUDE ANY TEXT, LETTERS, NUMBERS, WORDS, LABELS, WATERMARKS, LOGOS, OR SYMBOLS OF ANY KIND IN THE IMAGE."
        
        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": "1024x1024",
            "n": 1
        }
        
        # Log request data (without API key)
        print("Sending request to OpenAI with model:", data["model"])
        
        response = requests.post("https://api.openai.com/v1/images/generations", json=data, headers=headers)
        
        # Log response status
        print("Response status:", response.status_code)
        
        if response.status_code == 200:
            json_response = response.json()
            print("API Response received successfully")
            
            if "data" in json_response and len(json_response["data"]) > 0 and "url" in json_response["data"][0]:
                return json_response["data"][0]["url"]
            else:
                print("Unexpected response format:", json_response)
                return f"Error: Unexpected response format from OpenAI API"
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return f"Error: {response.status_code} - {response.text[:200]}..."
    except Exception as e:
        import traceback
        print("Exception in generate_car_image:", str(e))
        print(traceback.format_exc())
        return f"Error generating image: {str(e)}"

# Function to download and display images safely (compatible with older Streamlit versions)
def fetch_and_display_image(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            # Using width parameter instead of use_container_width for compatibility
            st.image(image, width=600)
            return True
        else:
            st.error(f"Failed to load image: HTTP {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return False

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
        .custom-container, .custom-container-tariff, .instructions-container {
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

# Function to reset the game
def reset_game():
    st.session_state.game_state = "instructions"
    st.session_state.result = None
    st.session_state.car_image_url = None
    st.session_state.tariff_applied = False
    st.session_state.attempts_used = 0
    st.session_state.attempts_results = []
    st.session_state.car_designs = []

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
        if st.button("Start Game", key="start_game_button", help="Click to start the game", type="primary"):
            st.session_state.game_state = "playing"
            st.session_state.attempts_used = 0
            st.session_state.attempts_results = []
            st.session_state.car_designs = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

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
                if st.button("Simulate Market", type="primary"):
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
                        
                        # Generate AI image only on final attempt
                        if st.session_state.attempts_used >= 3:
                            try:
                                with st.spinner("Generating your car image (this might take a moment)..."):
                                    st.session_state.car_image_url = generate_car_image(speed, aesthetics, reliability, efficiency, tech, price)
                                    
                                    # If we got an error back, use a fallback image
                                    if isinstance(st.session_state.car_image_url, str) and "Error" in st.session_state.car_image_url:
                                        car_type = "sports" if price > 80000 else "luxury" if price > 60000 else "suv" if price > 25000 else "compact"
                                        st.session_state.car_image_url = f"https://placehold.co/600x400?text=Your+{car_type.capitalize()}+Car"
                            except Exception as e:
                                st.session_state.car_image_url = "https://placehold.co/600x400?text=Your+Custom+Car"
                                
                            st.session_state.game_state = "game_over"
                            
                        st.rerun()
    
    # Right column for results display
    with main_col2:
        st.markdown('<div class="results-panel">', unsafe_allow_html=True)
        
        # Display results if we have them
        if st.session_state.result is not None:
            # Display car image only on final attempt if available
            if st.session_state.game_state == "game_over" and st.session_state.car_image_url:
                try:
                    # Add attractive box about AI-generated image with better contrast
                    st.markdown("""
                    <div style="background-color: #3498db; color: white; padding: 12px; 
                    border-radius: 5px; text-align: center; margin-bottom: 10px; font-weight: bold;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                    This image is uniquely generated by AI based on your chosen customization
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Check if URL starts with http (actual image URL) or Error
                    if st.session_state.car_image_url.startswith("http"):
                        success = fetch_and_display_image(st.session_state.car_image_url)
                        if not success:
                            st.warning("Could not load the car image. Using a placeholder instead.")
                            st.image("https://placehold.co/600x400?text=Your+Custom+Car", width=600)
                    else:
                        st.warning(f"Unable to generate car image. Using a placeholder instead.")
                        st.image("https://placehold.co/600x400?text=Your+Custom+Car", width=600)
                        
                except Exception as e:
                    st.warning(f"Unable to display car image: {str(e)}")
                    st.image("https://placehold.co/600x400?text=Your+Custom+Car", width=600)
            
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
                <h2 class="header-green">Market Simulation Results</h2>
                <p><strong>Best Market Segment:</strong> {result['Best Market Segment']}</p>
                <p><strong>Estimated Sales:</strong> {result['Estimated Sales']} units</p>
                <p><strong>Estimated Profit:</strong> ${result['Profit']:,}</p>
                <div class="section-divider">
                    <h3 class="header-orange">Profit Feedback</h3>
                    <p>{result['Feedback']}</p>
                </div>
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
                    <h2 class="header-orange">Updated Market Results (After Tariff)</h2>
                    <p><strong>Best Market Segment:</strong> {st.session_state.result['Best Market Segment']}</p>
                    <p><strong>Estimated Sales:</strong> {st.session_state.result['Estimated Sales']} units</p>
                    <p><strong>Original Profit:</strong> ${st.session_state.result['Profit']:,}</p>
                    <p><strong>New Estimated Profit:</strong> ${tariffed_profit:,.2f}</p>
                    <p><strong>Profit Change:</strong> ${tariffed_profit - st.session_state.result['Profit']:,.2f}</p>
                    <div class="section-divider">
                        <h3 class="header-orange">Updated Profit Feedback</h3>
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
                    <h3 style="color: #3498db; text-align: center;">Best Performing Design: Attempt {best_attempt_index+1}</h3>
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
                    best_badge = "Best " if is_best else ""
                    summary_data.append({
                        "Attempt": f"{best_badge}Attempt {i+1}",
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
                
                # Educational message about relevant courses
                st.markdown("""
                <div style="background-color: #e6f7ff; padding: 15px; border-radius: 10px; border: 2px solid #1890ff; margin: 20px 0;">
                    <h3 style="color: #1890ff; margin-top: 0;">Educational Note</h3>
                    <p>Taking courses at Coast Mountain College such as <strong>Introduction to Marketing</strong> and <strong>Business Finance</strong> would help you understand markets and how to price products accordingly!</p>
                    <p>Interested in more information? Visit the <a href="https://coastmountaincollege.ca/programs/study/business" target="_blank">Coast Mountain College Business Administration website</a></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Tariff button after 3rd attempt if not already applied
                col1, col2 = st.columns(2)
                with col1:
                    if not st.session_state.tariff_applied:
                        # Fix for tariff button disappearing
                        if st.button(
                            "Impose Trump Tariff +25%", 
                            key="apply_tariff",
                            type="secondary"
                        ):
                            st.session_state.tariff_applied = True
                            st.rerun()
                
                with col2:
                    # New game button
                    if st.button("Start New Game", key="new_game_button", type="primary"):
                        reset_game()
                        st.rerun()
                        
        # Show a placeholder message if no results to display yet
        else:
            st.markdown("""
            <div style="text-align: center; padding: 30px; background-color: #f5f5f5; border-radius: 10px;">
                <h3>Your results will appear here</h3>
                <p>Adjust the car settings on the left and click "Simulate Market" to see how your design performs.</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
