# analytics.py
import pandas as pd
import config

def filter_by_dominant_month(df):
    """
    Finds the most frequent Month/Year tuple in the data
    and filters the DataFrame to only include that month.
    """
    if df.empty:
        return df, None

    # Create a temporary column for Year-Month
    df['year_month'] = df['timestamp'].dt.to_period('M')
    
    # Find the mode (most frequent month)
    # We take the first one in case of a tie
    dominant_period = df['year_month'].mode()[0]
    
    # Filter the dataframe
    filtered_df = df[df['year_month'] == dominant_period].copy()
    
    # Clean up
    filtered_df.drop(columns=['year_month'], inplace=True)
    df.drop(columns=['year_month'], inplace=True) # clean original just in case
    
    return filtered_df, dominant_period

def create_pivot_table(poop_events):
    """
    Creates a DataFrame Matrix (User x Day).
    1. Converts list to DataFrame.
    2. Filters for the Dominant Month.
    3. Pivots and Reindexes.
    """
    if not poop_events:
        return pd.DataFrame(), pd.DataFrame(), "None"

    df = pd.DataFrame(poop_events)
    
    # --- FILTERING LOGIC ---
    # We only want to show the main month, ignoring the extra days 
    # captured due to timezone shifts or log cutoffs.
    df_filtered, target_month_period = filter_by_dominant_month(df)
    
    if df_filtered.empty:
        return pd.DataFrame(), df_filtered, "None"

    # Create a 'Date' column (removing time)
    df_filtered['date_only'] = df_filtered['timestamp'].dt.date
    
    # Pivot Table: Count of events
    pivot = df_filtered.pivot_table(
        index='user', 
        columns='date_only', 
        values='timestamp', 
        aggfunc='count',
        fill_value=0
    )
    
    # --- ENFORCE USER ORDER ---
    pivot = pivot.reindex(config.USER_ORDER, fill_value=0)
    pivot = pivot.astype(int)

    # Calculate Total column
    pivot['TOTAL'] = pivot.sum(axis=1)
    
    return pivot, df_filtered, str(target_month_period)

def get_ryan_rainbow_days(raw_messages, target_month_str):
    """
    Identifies dates where 'Ryan' said the word 'Rainbow'.
    Also ensures these dates fall within the target month.
    """
    rainbow_dates = set()
    
    # Convert target string (e.g., "2024-07") to check against
    # We will do a simple string check on the date for simplicity
    
    for msg in raw_messages:
        # Check User
        if msg['user'] == 'Ryan':
            # Check Content
            if any(kw in msg['content'] for kw in config.RAINBOW_KEYWORDS):
                # Check if it falls in the target month
                # msg['timestamp'] is a datetime object
                msg_period = msg['timestamp'].strftime("%Y-%m")
                
                if msg_period == target_month_str:
                    rainbow_dates.add(msg['timestamp'].date())
    
    return sorted(list(rainbow_dates))

def get_cotizada_stats(df_events):
    """
    Counts how many cotizadas each user has.
    """
    if df_events.empty:
        return pd.Series()
        
    cotizadas = df_events[df_events['is_cotizada'] == True]
    counts = cotizadas['user'].value_counts()
    
    # Also enforce order
    counts = counts.reindex(config.USER_ORDER, fill_value=0).astype(int)
    
    return counts