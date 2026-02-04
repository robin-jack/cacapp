# main.py
import chat_loader
import poop_processor
import analytics
import config
import os
import pandas as pd

# Name of your file
FILE_NAME = "inputs/cacas_11_25.txt"

def main():
    print("--- 💩 Cacapp Analyzer 2.2 (TimeZones Edition) ---")
    
    # 1. Load Data
    print(f"Loading chat log: {FILE_NAME}...")
    try:
        raw_messages = chat_loader.parse_chat_log(FILE_NAME)
    except FileNotFoundError:
        print(f"Error: File '{FILE_NAME}' not found.")
        return

    print(f"Parsed {len(raw_messages)} messages.")
    
    # 2. Process Logic (NLP, Time Travel & Time Zones)
    # Note: We process ALL data first to handle "Yesterday" logic correctly across month boundaries.
    print("Crunching numbers and applying timezones...")
    poop_events = poop_processor.process_poops(raw_messages)
    
    # 3. Analytics (Filtering happens here)
    pivot_table, df_events_filtered, target_month = analytics.create_pivot_table(poop_events)
    
    print(f"Target Month Detected: {target_month}")
    print(f"Valid Poops in Target Month: {len(df_events_filtered)}")

    # 4. Ryan's Rainbows (Passing raw messages to check text)
    rainbows = analytics.get_ryan_rainbow_days(raw_messages, target_month)
    
    cotizadas = analytics.get_cotizada_stats(df_events_filtered)
    
    # 5. Output to Console
    print(f"\n--- 📅 MATRIX FOR {target_month} ---")
    if not pivot_table.empty:
        print(pivot_table)
    else:
        print("No data found for the dominant month.")
    
    print("\n--- 🌈 RAINBOW DAYS (Ryan said 'Rainbow') ---")
    if rainbows:
        for date in rainbows:
            print(f" -> {date.strftime('%d/%m/%Y')}")
    else:
        print("Ryan did not declare any Rainbows this month.")
        
    print("\n--- 💰 CACO-TIZADAS (Paid Poops) ---")
    print(cotizadas if not cotizadas.empty else "No cotizadas detected.")

    # 6. Export to CSV
    if not pivot_table.empty:
        if not os.path.exists(config.OUTPUT_FOLDER):
            os.makedirs(config.OUTPUT_FOLDER)
            
        csv_path = os.path.join(config.OUTPUT_FOLDER, "poop_stats.csv")
        pivot_table.to_csv(csv_path)
        print(f"\n✅ Stats successfully exported to: {csv_path}")

if __name__ == "__main__":
    main()