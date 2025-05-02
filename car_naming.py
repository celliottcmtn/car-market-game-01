import random

def generate_tagline(speed, aesthetics, reliability, efficiency, tech):
    """Generate a marketing tagline based on car's top features"""
    taglines = []
    
    if speed >= 8:
        taglines.append(random.choice(["Fast as lightning", "Speed redefined", "Feel the rush"]))
    if aesthetics >= 8:
        taglines.append(random.choice(["Beauty on wheels", "Turn heads everywhere", "Stunning design"]))
    if reliability >= 8:
        taglines.append(random.choice(["Built to last", "Reliability guaranteed", "Never lets you down"]))
    if efficiency >= 8:
        taglines.append(random.choice(["Eco-friendly power", "Green machine", "Efficiency champion"]))
    if tech >= 8:
        taglines.append(random.choice(["Future on wheels", "Tech marvel", "Smart driving"]))
    
    if len(taglines) > 0:
        return random.choice(taglines)
    
    # Default taglines if no attribute is high enough
    default_taglines = [
        "Drive the difference",
        "Your journey begins here",
        "Designed for you",
        "The smart choice",
        "Go beyond expectations"
    ]
    return random.choice(default_taglines)

def generate_model_name(segment, speed, aesthetics):
    """Generate a model name based on car segment and features"""
    
    # Prefixes based on segment
    segment_prefixes = {
        "Budget": ["Eco", "Smart", "City", "Metro", "Value"],
        "Family": ["Voyage", "Journey", "Comfort", "Family", "Explore"],
        "Luxury": ["Elite", "Premium", "Prestige", "Sovereign", "Royal"],
        "Sports": ["Turbo", "Velocity", "Raptor", "Thunder", "Sprint"],
        "Eco-Friendly": ["Green", "Leaf", "Earth", "Eco", "Nature"]
    }
    
    # Suffixes based on speed and aesthetics
    suffixes = []
    if speed >= 7:
        suffixes.extend(["GT", "X", "Sport", "Turbo", "RS"])
    if aesthetics >= 7:
        suffixes.extend(["Elegance", "Style", "Design", "Lux", "SL"])
    if len(suffixes) == 0:
        suffixes = ["S", "SE", "LE", "XE", "Plus"]
    
    # Generate name
    prefix = random.choice(segment_prefixes.get(segment, ["Model"]))
    suffix = random.choice(suffixes)
    
    # Add a random number between 100 and 900 (in increments of 50)
    number = random.randrange(1, 10) * 100 + random.choice([0, 5]) * 10
    
    # Assemble the name in one of several formats
    name_format = random.choice([
        f"{prefix} {number}",
        f"{prefix} {number}{suffix}",
        f"{prefix}{suffix} {number}",
        f"{prefix} {suffix}"
    ])
    
    return name_format
