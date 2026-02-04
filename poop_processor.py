# poop_processor.py
import re
from datetime import timedelta, datetime
import config

def extract_specific_times(text):
    """
    Finds specific times in text (e.g., "9am", "10:30") and returns (hour, minute).
    """
    matches = re.findall(config.TIME_PATTERN, text)
    times = []
    for h, m, period in matches:
        try:
            hour = int(h)
            minute = int(m) if m else 0
            
            # Handle AM/PM
            if period == 'pm' and hour < 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
                
            if 0 <= hour <= 24 and 0 <= minute < 60:
                times.append((hour, minute))
        except ValueError:
            continue
    return times

def process_poops(messages):
    """
    Iterates messages to find poops and applies context rules.
    Returns a list of 'PoopEvent' dictionaries.
    """
    poop_events = []
    
    for i, msg in enumerate(messages):
        # 1. Detect Poop
        if '💩' in msg['content']:
            
            # --- CONTEXT WINDOW SETUP ---
            # Look ahead at next 3 messages from the SAME user
            context_msgs = []
            for j in range(1, 4):
                if i + j < len(messages):
                    next_msg = messages[i+j]
                    if next_msg['user'] == msg['user']:
                        context_msgs.append(next_msg['content'])
            
            combined_context = " ".join(context_msgs)
            
            # Base timestamp
            final_time = msg['timestamp']
            
            # --- RULE C: YESTERDAY CHECK ---
            # Check keywords in context or original message
            is_yesterday = any(kw in combined_context or kw in msg['content'] for kw in config.YESTERDAY_KEYWORDS)
            
            if is_yesterday:
                final_time = final_time - timedelta(days=1)

            # --- RULE D: SPLITTING & RULE A: SPECIFIC TIME ---
            # Check if text contains explicit times (e.g., "una 9am otra 10am")
            # We check the context for specific times.
            found_times = extract_specific_times(combined_context)
            
            # If explicit times are found, they override the message time.
            # If multiple times found (Rule D), we create multiple events.
            if found_times:
                for h, m in found_times:
                    # Construct new time using the calculated date (handling yesterday logic)
                    new_dt = final_time.replace(hour=h, minute=m, second=0)
                    
                    poop_events.append({
                        'user': msg['user'],
                        'timestamp': new_dt,
                        'is_cotizada': any(k in combined_context for k in config.COTIZADA_KEYWORDS),
                        'original_msg_id': i
                    })
                continue # Skip standard processing since we handled specific times
            
            # --- RULE B: RELATIVE TIME ---
            # Only apply if no specific time was found
            rel_match = re.search(config.RELATIVE_TIME_PATTERN, combined_context)
            if rel_match:
                amount = int(rel_match.group(1))
                unit = rel_match.group(2)
                
                # Simple logic: assume hours if 'h' or 'horas', else minutes
                if 'h' in unit:
                    final_time = final_time - timedelta(hours=amount)
                else:
                    final_time = final_time - timedelta(minutes=amount)

            # --- RULE E: MADRUGADA ---
            # Logic: If time is 00:00-06:00 and NO "yesterday" keyword, keep as is.
            # This is already handled because we only subtract day if 'is_yesterday' is True.
            
            # Add the single event
            poop_events.append({
                'user': msg['user'],
                'timestamp': final_time,
                'is_cotizada': any(k in combined_context or k in msg['content'] for k in config.COTIZADA_KEYWORDS),
                'original_msg_id': i
            })

    return poop_events