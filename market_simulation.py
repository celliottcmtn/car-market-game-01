import pandas as pd
import random

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

# Improved market simulation function with random events
def simulate_market_performance(speed, aesthetics, reliability, efficiency, tech, price):
    # Check if this is a sports car
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
    
    # Random market event (increased chance to 40% to make them more common)
    market_event = None
    if random.random() < 0.40:  # Increased from 25% to 40%
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
    feedback = get_feedback_for_profit(profit, estimated_sales)
    
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
