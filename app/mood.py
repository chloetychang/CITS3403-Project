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
        Entry.sleep_datetime >= datetime.combine(start_of_week, datetime.min.time()),
        Entry.sleep_datetime <= datetime.combine(end_of_week, datetime.max.time())
    ).all()
    
    sleep_dict = {
        start_of_week + timedelta(days=i): 0
        for i in range(7)
    }
    
    count_mood = sum([1 if entry.mood is not None else 0 for entry in entries])
    if count_mood == 0:
        average_mood = "____"
    else:
        average_mood = sum(entry.mood for entry in entries if entry.mood is not None) / count_mood
        
    if count_mood == 0:
        max_mood = "____"
    else: 
        max_mood = max(entry.mood for entry in entries if entry.mood is not None)
    
    if count_mood == 0:
        highest_day = "____"
    else:
        highest_day = max(entries, key=lambda entry: entry.mood).wake_datetime.strftime('%Y-%m-%d (%A)')
        
    return average_mood, max_mood, highest_day