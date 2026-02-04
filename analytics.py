# analytics.py
import pandas as pd

def create_pivot_table(poop_events):
    """
    Creates a DataFrame Matrix (User x Day).
    """
    if not poop_events:
        return pd.DataFrame()

    df = pd.DataFrame(poop_events)
    
    # Create a 'Date' column (removing time)
    df['date_only'] = df['timestamp'].dt.date
    
    # Pivot Table: Count of events
    pivot = df.pivot_table(
        index='user', 
        columns='date_only', 
        values='timestamp', 
        aggfunc='count',
        fill_value=0
    )
    
    # Calculate Total column
    pivot['TOTAL'] = pivot.sum(axis=1)
    
    return pivot, df

def get_rainbow_days(df_events, total_users_count=6):
    """
    Identifies dates where unique user count == total_users_count
    """
    if df_events.empty:
        return []

    daily_users = df_events.groupby('date_only')['user'].nunique()
    rainbow_dates = daily_users[daily_users >= total_users_count].index.tolist()
    
    return rainbow_dates

def get_cotizada_stats(df_events):
    """
    Counts how many cotizadas each user has.
    """
    if df_events.empty:
        return pd.Series()
        
    cotizadas = df_events[df_events['is_cotizada'] == True]
    return cotizadas['user'].value_counts()