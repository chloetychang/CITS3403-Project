from datetime import datetime, timedelta
from collections import defaultdict
from app.models import Entry
from flask_login import current_user
import plotly.graph_objs as go
from plotly.offline import plot

def generate_mood_insights(week_offset=0):
    start_of_week = datetime.today().date() + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)
    
    # Query entries only from the current user, as well as between start and end of the target week
    entries = Entry.query.filter(
        Entry.user_id == current_user.user_id,
        Entry.wake_datetime >= datetime.combine(start_of_week, datetime.min.time()),
        Entry.wake_datetime <= datetime.combine(end_of_week, datetime.max.time())
    ).all()
    
    sleep_dict = {
        start_of_week + timedelta(days=i): 0
        for i in range(7)
    }
    
    count_mood = sum([1 if entry.mood is not None else 0 for entry in entries])
    
    if count_mood == 0:
        average_mood = "____"
        max_mood = "____"
        highest_day = "____"
        hours = "____"
        highest_day_sleep= "____"
        highest_day_wake = "____"
    else:
        average_mood = sum(entry.mood for entry in entries if entry.mood is not None) / count_mood
        max_mood = max(entry.mood for entry in entries if entry.mood is not None)
        highest_day = max(entries, key=lambda entry: entry.mood).wake_datetime.strftime('%Y-%m-%d (%A)')
        hours = (max(entries, key=lambda entry: entry.mood).wake_datetime - max(entries, key=lambda entry: entry.mood).sleep_datetime).total_seconds() / 3600
        highest_day_sleep = max(entries, key=lambda entry: entry.mood).sleep_datetime
        highest_day_wake = max(entries, key=lambda entry: entry.mood).wake_datetime
        
    return average_mood, max_mood, highest_day, hours, highest_day_sleep, highest_day_wake