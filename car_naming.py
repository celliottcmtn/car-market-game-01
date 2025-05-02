# car_naming.py
import random

# Lists for name generation
performance_prefixes = ["Thunder", "Bolt", "Viper", "Raptor", "Blaze", "Storm", "Fury", "Flash"]
efficiency_prefixes = ["Eco", "Volt", "Glide", "Flow", "Breeze", "Stream", "Vista", "Pulse"]
comfort_prefixes = ["Royal", "Luxe", "Plush", "Elite", "Velvet", "Serenity", "Harmony", "Zenith"]
style_prefixes = ["Aura", "Chroma", "Prism", "Mirage", "Eclipse", "Apex", "Phantom", "Cosmos"]

model_suffixes = ["X", "GT", "RS", "LX", "Sport", "Prime", "Plus", "Elite", "EV", "ZX"]
number_models = ["100", "200", "300", "500", "750", "1000", "3000", "5000"]

# Tagline components
performance_taglines = [
    "Unleash the power within",
    "Dominate every road",
    "Feel the adrenaline rush",
    "Performance that speaks for itself",
    "Leave the competition behind",
]

efficiency_taglines = [
    "Efficiency reimagined",
    "Go further, use less",
    "Smart driving for a smarter world",
    "Efficiency without compromise",
    "The future of sustainable driving",
]

comfort_taglines = [
    "Where luxury meets comfort",
    "Experience first-class travel on wheels",
    "Comfort that embraces you",
    "Redefining the driving experience",
    "Your sanctuary on the road",
]

style_taglines = [
    "Turn heads wherever you go",
    "Style that stands out",
    "Design that makes a statement",
    "Beauty in motion",
    "Crafted to perfection",
]

price_taglines = [
    "Luxury within reach",
    "Premium quality without the premium price",
    "Value that exceeds expectations",
    "The smart choice for discerning drivers",
    "Engineered for excellence, priced for reality",
]

def generate_model_name(performance, efficiency, comfort, style):
    """Generate a car model name based on its attributes."""
    # Determine the dominant attribute
    attributes = {
        "performance": performance,
        "efficiency": efficiency,
        "comfort": comfort,
        "style": style
    }
    
    dominant_attribute = max(attributes, key=attributes.get)
    
    # Select a prefix based on the dominant attribute
    if dominant_attribute == "performance":
        prefix = random.choice(performance_prefixes)
    elif dominant_attribute == "efficiency":
        prefix = random.choice(efficiency_prefixes)
    elif dominant_attribute == "comfort":
        prefix = random.choice(comfort_prefixes)
    else:  # style
        prefix = random.choice(style_prefixes)
    
    # Choose a suffix format
    suffix_type = random.randint(1, 3)
    
    if suffix_type == 1:
        # Letter/word suffix
        suffix = random.choice(model_suffixes)
        return f"{prefix} {suffix}"
    elif suffix_type == 2:
        # Number suffix
        number = random.choice(number_models)
        return f"{prefix} {number}"
    else:
        # Combined suffix
        suffix = random.choice(model_suffixes)
        number = random.choice(number_models)
        return f"{prefix} {suffix}-{number}"

def generate_tagline(performance, efficiency, comfort, style):
    """Generate a tagline based on car attributes."""
    # Determine the top two attributes
    attributes = [
        ("performance", performance),
        ("efficiency", efficiency),
        ("comfort", comfort),
        ("style", style)
    ]
    
    # Sort by attribute value (descending)
    attributes.sort(key=lambda x: x[1], reverse=True)
    
    # Get the top two attributes
    top_attribute = attributes[0][0]
    second_attribute = attributes[1][0]
    
    # Select taglines based on the top attributes
    if top_attribute == "performance":
        main_tagline = random.choice(performance_taglines)
    elif top_attribute == "efficiency":
        main_tagline = random.choice(efficiency_taglines)
    elif top_attribute == "comfort":
        main_tagline = random.choice(comfort_taglines)
    else:  # style
        main_tagline = random.choice(style_taglines)
    
    # Sometimes add a price-based tagline
    if random.random() < 0.3:
        second_tagline = random.choice(price_taglines)
    else:
        if second_attribute == "performance":
            second_tagline = random.choice(performance_taglines)
        elif second_attribute == "efficiency":
            second_tagline = random.choice(efficiency_taglines)
        elif second_attribute == "comfort":
            second_tagline = random.choice(comfort_taglines)
        else:  # style
            second_tagline = random.choice(style_taglines)
    
    # Combine taglines with a connector
    connector = random.choice([".", " ", ". ", " - "])
    return f"{main_tagline}{connector}{second_tagline}"
