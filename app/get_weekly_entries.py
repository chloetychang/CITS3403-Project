from datetime import datetime, timedelta
from app.models import Entry
from flask_login import current_user

def get_weekly_entries(week_offset = 0):
    start_of_week = datetime.today().date() + timedelta(1) + timedelta(weeks=week_offset)
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
    
    # Use date keys directly
    for entry in entries:
        if entry.wake_datetime and entry.sleep_datetime:
            duration = (entry.wake_datetime - entry.sleep_datetime).total_seconds() / 3600
            entry_date = entry.wake_datetime.date()
            if entry_date in sleep_dict:
                sleep_dict[entry_date] += duration  # Only if it's within the week
    
    return entries, sleep_dict