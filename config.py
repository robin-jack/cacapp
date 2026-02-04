# config.py
import os

# User Mapping: Chat Name -> Real Name
USER_MAPPING = {
    'Pablo Ella': 'Pablo',
    'Chachito Mixes': 'Sergio',
    'Robin Jack': 'Robin',
    'Carlos Chacho': 'Carlos',
    'Ryan Memesmierda': 'Ryan',
    'Alexander': 'Alexander'
}

# Time Zone Offsets (in Hours)
TIMEZONE_OFFSETS = {
    'Pablo': -9,
    'Sergio': 0,
    'Robin': 0,
    'Carlos': -1,
    'Ryan': -1,
    'Alexander': 0
}

# Strict Output Order
USER_ORDER = ['Pablo', 'Sergio', 'Robin', 'Carlos', 'Ryan', 'Alexander']

# Output Configuration
OUTPUT_FOLDER = "output"

# Synonyms for logic
YESTERDAY_KEYWORDS = [
    "ayer", "cacayer", "del dia anterior", 
    "gestern", "anoche", "madrugada pasada",
    "yesterday", "ayet"
]

VAGUE_TIME_KEYWORDS = [
    "antes", "de antes", "esta mañana", 
    "tarde", "cacantes", "cacamañana", "cacanoche",
    "rato", "de hace"
]

COTIZADA_KEYWORDS = ["cotizada", "pagada", "remunerada"]

# New: Rainbow detection now relies on text, not poop count
RAINBOW_KEYWORDS = ["rainbow"]

# Regex Patterns
LOG_PATTERN = r'^(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}) - ([^:]+): (.+)$'
TIME_PATTERN = r'\b(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm|h)?\b'
RELATIVE_TIME_PATTERN = r'hace\s+(\d+)\s*(h|horas|hours|m|min|minutos)'