# main.py
import chat_loader
import poop_processor
import analytics
import pandas as pd

# Name of your file
FILE_NAME = "cacas_11_25.txt"

def main():
    print("--- 💩 Cacapp Analyzer 2.0 ---")
    
    # 1. Load Data
    print(f"Loading chat log: {FILE_NAME}...")
    raw_messages = chat_loader.parse_chat_log(FILE_NAME)
    print(f"Parsed {len(raw_messages)} messages.")
    
    # 2. Process Logic (NLP & Time Travel)
    print("Crunching numbers and detecting anomalies...")
    poop_events = poop_processor.process_poops(raw_messages)
    print(f"Detected {len(poop_events)} valid poop events.")
    
    # 3. Analytics
    pivot_table, df_events = analytics.create_pivot_table(poop_events)
    rainbows = analytics.get_rainbow_days(df_events)
    cotizadas = analytics.get_cotizada_stats(df_events)
    
    # 4. Output
    print("\n--- 📅 MONTHLY MATRIX ---")
    print(pivot_table)
    
    print("\n--- 🌈 RAINBOW DAYS (All 6 users pooped) ---")
    if rainbows:
        for date in rainbows:
            print(f" -> {date.strftime('%d/%m/%Y')}")
    else:
        print("No Rainbows found in this period :(")
        
    print("\n--- 💰 CACO-TIZADAS (Paid Poops) ---")
    print(cotizadas if not cotizadas.empty else "No cotizadas detected.")

    # Optional: Export to CSV
    # pivot_table.to_csv("poop_stats.csv")
    # print("\nStats exported to poop_stats.csv")

if __name__ == "__main__":
    main()