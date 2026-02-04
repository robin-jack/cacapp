# config.py

# User Mapping: Chat Name -> Real Name
USER_MAPPING = {
    'Pablo Ella': 'Pablo',
    'Chachito Mixes': 'Sergio',
    'Robin Jack': 'Robin',
    'Carlos Chacho': 'Carlos',
    'Ryan Memesmierda': 'Ryan',
    'Alexander': 'Alexander'
}

# Synonyms for logic
YESTERDAY_KEYWORDS = [
    "ayer", "cacayer", "del dia anterior", 
    "gestern", "anoche", "madrugada pasada"
]

# Words that indicate time but shouldn't trigger a mathematical shift
VAGUE_TIME_KEYWORDS = [
    "antes", "de antes", "esta mañana", "pronto", 
    "luego", "rato", "ya", "tarde"
]

# Keywords for specific types of poop
COTIZADA_KEYWORDS = ["cotizada", "pagada", "remunerada"]

# Regex Patterns
# Matches: 12/07/2024, 10:12 - User: Message
LOG_PATTERN = r'^(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}) - ([^:]+): (.+)$'

# Matches times like: 9am, 10:30, 15:00h, 4 pm
TIME_PATTERN = r'\b(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm|h)?\b'

# Matches relative time: hace 2 horas, hace 30 min
RELATIVE_TIME_PATTERN = r'hace\s+(\d+)\s*(h|horas|hours|m|min|minutos)'