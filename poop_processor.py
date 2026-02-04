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
    Iterates messages to find poops and applies context rules AND Time Zones.
    """
    poop_events = []
    
    for i, msg in enumerate(messages):
        if '💩' in msg['content']:
            
            # --- CONTEXT WINDOW ---
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
            is_yesterday = any(kw in combined_context or kw in msg['content'] for kw in config.YESTERDAY_KEYWORDS)
            if is_yesterday:
                final_time = final_time - timedelta(days=1)

            # --- PREPARE TO CREATE EVENTS ---
            events_to_add = []

            # --- RULE D & A: SPECIFIC TIMES ---
            found_times = extract_specific_times(combined_context)
            
            if found_times:
                for h, m in found_times:
                    new_dt = final_time.replace(hour=h, minute=m, second=0)
                    events_to_add.append(new_dt)
            else:
                # --- RULE B: RELATIVE TIME ---
                rel_match = re.search(config.RELATIVE_TIME_PATTERN, combined_context)
                if rel_match:
                    amount = int(rel_match.group(1))
                    unit = rel_match.group(2)
                    if 'h' in unit:
                        final_time = final_time - timedelta(hours=amount)
                    else:
                        final_time = final_time - timedelta(minutes=amount)
                
                events_to_add.append(final_time)

            # --- FINAL STEP: APPLY USER TIMEZONE OFFSET ---
            # Retrieve offset from config (default to 0 if not found)
            offset_hours = config.TIMEZONE_OFFSETS.get(msg['user'], 0)
            
            for dt in events_to_add:
                # Shift the time based on the user's timezone
                adjusted_dt = dt + timedelta(hours=offset_hours)

                poop_events.append({
                    'user': msg['user'],
                    'timestamp': adjusted_dt,
                    'is_cotizada': any(k in combined_context or k in msg['content'] for k in config.COTIZADA_KEYWORDS),
                    'original_msg_id': i
                })

    return poop_events