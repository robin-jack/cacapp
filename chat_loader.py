# chat_loader.py
import re
import pandas as pd
from datetime import datetime
import config

def parse_chat_log(file_path):
    """
    Parses a WhatsApp txt export into a list of dictionaries.
    Handles multi-line messages.
    """
    data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_entry = None

    for line in lines:
        line = line.strip()
        # Skip system messages like "<Media omitted>" if desired, 
        # but for now we keep them as they might be context.
        
        match = re.match(config.LOG_PATTERN, line)
        
        if match:
            # If we have a previous entry pending, append it
            if current_entry:
                data.append(current_entry)
            
            date_str, time_str, user, message = match.groups()
            
            # Combine date and time
            dt_obj = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
            
            # Map user name (if in config, otherwise keep original)
            clean_user = config.USER_MAPPING.get(user, user)
            
            current_entry = {
                'timestamp': dt_obj,
                'user': clean_user,
                'content': message.lower() # Lowercase for easier analysis
            }
        else:
            # Handle multi-line messages (append to previous message)
            if current_entry:
                current_entry['content'] += f" {line.lower()}"

    # Append the last entry
    if current_entry:
        data.append(current_entry)

    return data