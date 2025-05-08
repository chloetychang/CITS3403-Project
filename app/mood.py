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
    average_mood = sum(entry.mood for entry in entries if entry.mood is not None) / count_mood
    
    return average_mood