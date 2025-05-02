import random

# Expanded libraries of car naming options
BUDGET_PREFIXES = [
    "Metro", "Civic", "Echo", "Swift", "Neo", "Spark", "Pulse", "Spirit", "Orbit", "Spree",
    "Thrift", "Eco", "Smart", "City", "Urban", "Compact", "Mini", "Micro", "Value", "Basic",
    "Prime", "Zip", "Quick", "Solo", "Link", "Slice", "Edge", "Core", "Pure", "Simply",
    "Express", "Agile", "Lite", "Easy", "Vista", "Breeze", "Focus", "Vita", "Essential", "Nimble",
    "Pace", "Bolt", "Flyer", "Ready", "Active", "Direct", "Point", "Spot", "Flash", "Dash",
    "Stride", "Step", "Path", "Way", "Route", "Street", "Stroll", "Walk", "Run", "Cruise",
    "Sync", "Wave", "Logic", "Sense", "True", "Wise", "Smart", "Sharp", "Keen", "Brief",
    "Short", "Small", "Tiny", "Neat", "Trim", "Slim", "Thin", "Petite", "Light", "Feather",
    "Fleet", "Brisk", "Prompt", "Rapid", "Hasty", "Swift", "Speedy", "Quick", "Fast", "Velocity"
]

FAMILY_PREFIXES = [
    "Journey", "Voyage", "Odyssey", "Quest", "Venture", "Expedition", "Pioneer", "Discovery", "Explorer", "Navigator",
    "Compass", "Guide", "Pilot", "Captain", "Leader", "Commander", "Ranger", "Scout", "Tracker", "Pathfinder",
    "Legacy", "Heritage", "Tribute", "Honor", "Respect", "Esteem", "Dignify", "Prestige", "Acclaim", "Renown",
    "Family", "Comfort", "Haven", "Sanctuary", "Refuge", "Shelter", "Harbor", "Dock", "Port", "Berth",
    "Oasis", "Retreat", "Resort", "Villa", "Manor", "Estate", "Domain", "Realm", "Kingdom", "Empire",
    "Harmony", "Unity", "Together", "Alliance", "Coalition", "Union", "League", "Fellowship", "Society", "Community",
    "Grace", "Elegance", "Poise", "Charm", "Appeal", "Allure", "Attract", "Entice", "Captivate", "Enchant",
    "Horizon", "Skyline", "Frontier", "Boundary", "Border", "Margin", "Edge", "Verge", "Brink", "Threshold",
    "Meadow", "Valley", "Prairie", "Plain", "Field", "Pasture", "Glade", "Clearing", "Opening", "Hollow"
]

LUXURY_PREFIXES = [
    "Elite", "Premium", "Sovereign", "Majestic", "Royal", "Noble", "Imperial", "Dynasty", "Monarch", "Regent",
    "Prestige", "Distinction", "Excellence", "Eminence", "Grandeur", "Splendor", "Magnificence", "Opulence", "Lavish", "Lush",
    "Supreme", "Paramount", "Foremost", "Preeminent", "Peerless", "Unmatched", "Unrivaled", "Unequaled", "Unsurpassed", "Unexcelled",
    "Caliber", "Quality", "Standard", "Grade", "Class", "Level", "Status", "Rank", "Standing", "Position",
    "Genesis", "Origin", "Source", "Wellspring", "Fount", "Fountain", "Spring", "Birthplace", "Cradle", "Root",
    "Legacy", "Heritage", "Lineage", "Descent", "Ancestry", "Pedigree", "Bloodline", "Line", "Stock", "Extraction",
    "Pinnacle", "Summit", "Peak", "Crest", "Top", "Zenith", "Crown", "Apex", "Acme", "Culmination",
    "Majesty", "Nobility", "Dignity", "Honor", "Glory", "Renown", "Fame", "Celebrity", "Notoriety", "Repute",
    "Sublime", "Exquisite", "Superb", "Elegant", "Graceful", "Refined", "Polished", "Cultured", "Cultivated", "Sophisticated"
]

SPORTS_PREFIXES = [
    "Turbo", "Velocity", "Raptor", "Thunder", "Bolt", "Sprint", "Surge", "Blitz", "Storm", "Cyclone",
    "Flash", "Speed", "Dash", "Thrust", "Torque", "Boost", "Power", "Force", "Drive", "Rush",
    "Jet", "Rocket", "Missile", "Comet", "Meteor", "Asteroid", "Blaze", "Flame", "Fire", "Inferno",
    "Viper", "Cobra", "Falcon", "Eagle", "Hawk", "Tiger", "Panther", "Leopard", "Jaguar", "Cheetah",
    "Nitro", "Octane", "Piston", "Charger", "Accelerator", "Dynamo", "Magnum", "Arsenal", "Fury", "Rage",
    "Agile", "Nimble", "Quick", "Rapid", "Brisk", "Swift", "Prompt", "Expedite", "Hasten", "Hurry",
    "Slipstream", "Airflow", "Current", "Tide", "Surge", "Swell", "Surge", "Crest", "Ridge", "Peak",
    "Adrenaline", "Impulse", "Stimulus", "Incentive", "Impetus", "Momentum", "Propulsion", "Thrust", "Push", "Shove",
    "Extreme", "Radical", "Intense", "Severe", "Acute", "Sharp", "Keen", "Fierce", "Vehement", "Ardent"
]

ECO_PREFIXES = [
    "Green", "Leaf", "Earth", "Nature", "Bio", "Eco", "Solar", "Terra", "Gaia", "Verdant",
    "Pure", "Clean", "Fresh", "Crisp", "Clear", "Bright", "Lush", "Vibrant", "Vivid", "Bloom",
    "Sustain", "Renew", "Revive", "Recycle", "Restore", "Replenish", "Reuse", "Reduce", "Recover", "Reclaim",
    "Breeze", "Wind", "Air", "Sky", "Cloud", "Mist", "Vapor", "Breath", "Gust", "Draft",
    "Meadow", "Prairie", "Field", "Garden", "Grove", "Forest", "Woods", "Thicket", "Jungle", "Wilderness",
    "Stream", "River", "Lake", "Pond", "Pool", "Spring", "Fountain", "Cascade", "Falls", "Flow",
    "Seed", "Sprout", "Bud", "Grow", "Bloom", "Blossom", "Flower", "Plant", "Tree", "Shrub",
    "Dawn", "Sunrise", "Morning", "Day", "Light", "Shine", "Glow", "Radiate", "Beam", "Ray",
    "Horizon", "Panorama", "Vista", "View", "Scene", "Landscape", "Terrain", "Region", "Zone", "Area"
]

# Suffixes based on attributes
SPEED_SUFFIXES = ["GT", "RS", "X", "Sport", "Turbo", "Dash", "Bolt", "Nitro", "Rush", "Racing"]
AESTHETICS_SUFFIXES = ["Elegance", "Design", "Style", "Lux", "SL", "Grand", "Premium", "Elite", "Signature", "Edition"]
RELIABILITY_SUFFIXES = ["Pro", "Plus", "Ultra", "Max", "Supreme", "Prime", "Excel", "Alpha", "One", "Top"]
EFFICIENCY_SUFFIXES = ["Eco", "Blue", "Green", "Smart", "Wise", "E", "Hybrid", "Pulse", "Flow", "Zero"]
TECH_SUFFIXES = ["Tech", "Connect", "Link", "Smart", "iDrive", "Sync", "Wave", "Future", "Next", "Vision"]

# Number formats
NUMBER_FORMATS = [
    lambda: str(random.randrange(1, 10) * 100),
    lambda: str(random.randrange(1, 10) * 100 + 50),
    lambda: str(random.randrange(1, 10) * 10),
    lambda: str(random.randrange(1, 10)),
    lambda: ""  # Sometimes no number
]

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

def generate_model_name(segment, speed, aesthetics, reliability, efficiency, tech):
    """Generate a model name based on car segment and features"""
    
    # Choose prefix library based on segment
    if segment == "Budget":
        prefix_library = BUDGET_PREFIXES
    elif segment == "Family":
        prefix_library = FAMILY_PREFIXES
    elif segment == "Luxury":
        prefix_library = LUXURY_PREFIXES
    elif segment == "Sports":
        prefix_library = SPORTS_PREFIXES
    elif segment == "Eco-Friendly":
        prefix_library = ECO_PREFIXES
    else:
        # Default/fallback
        prefix_library = FAMILY_PREFIXES
    
    # Choose a random prefix from the appropriate library
    prefix = random.choice(prefix_library)
    
    # Choose suffixes based on highest attributes (top 2)
    attributes = [
        ("speed", speed, SPEED_SUFFIXES),
        ("aesthetics", aesthetics, AESTHETICS_SUFFIXES),
        ("reliability", reliability, RELIABILITY_SUFFIXES),
        ("efficiency", efficiency, EFFICIENCY_SUFFIXES),
        ("tech", tech, TECH_SUFFIXES)
    ]
    
    # Sort by attribute value (highest first)
    attributes.sort(key=lambda x: x[1], reverse=True)
    
    # Get suffixes from the top 2 attributes if high enough (>= 7)
    potential_suffixes = []
    for attr_name, attr_value, suffix_list in attributes[:2]:
        if attr_value >= 7:
            potential_suffixes.extend(suffix_list)
    
    # If no attributes are high enough, use a default mixture
    if not potential_suffixes:
        potential_suffixes = SPEED_SUFFIXES + AESTHETICS_SUFFIXES + RELIABILITY_SUFFIXES[:3]
    
    # Choose a random suffix
    suffix = random.choice(potential_suffixes)
    
    # Generate a number (or empty string)
    number_format = random.choice(NUMBER_FORMATS)
    number = number_format()
    
    # Assemble the name in one of several formats
    name_formats = [
        f"{prefix} {number}",
        f"{prefix} {number} {suffix}",
        f"{prefix} {suffix} {number}",
        f"{prefix} {suffix}",
        f"{prefix}{suffix} {number}"
    ]
    
    # Filter out formats that would result in double spaces when number is empty
    valid_formats = [fmt.replace("  ", " ") for fmt in name_formats]
    if number == "":
        valid_formats = [fmt for fmt in valid_formats if "  " not in fmt]
    
    return random.choice(valid_formats).strip()

def generate_version_name(base_name, version):
    """Add version number to the car name"""
    return f"{base_name} V{version}"
