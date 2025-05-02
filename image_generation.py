import os
import requests

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
