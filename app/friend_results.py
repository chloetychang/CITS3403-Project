import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime, timedelta
from app.models import Entry
from app import db

def get_friend_weekly_entries(friend_id, week_offset=0):
    # Calculate date range for the week
    start_of_week = datetime.today().date() + timedelta(1) + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)
    
    # Query entries for the week
    entries = Entry.query.filter(
        Entry.user_id == friend_id,
        Entry.wake_datetime >= datetime.combine(start_of_week, datetime.min.time()),
        Entry.wake_datetime <= datetime.combine(end_of_week, datetime.max.time())
    ).all()
    
    sleep_dict = {
        start_of_week + timedelta(days=i): 0
        for i in range(7)
    }
    
    for entry in entries:
        if entry.wake_datetime and entry.sleep_datetime:
            duration = (entry.wake_datetime - entry.sleep_datetime).total_seconds() / 3600
            entry_date = entry.wake_datetime.date()
            if entry_date in sleep_dict:
                sleep_dict[entry_date] += duration
    
    return entries, sleep_dict

def generate_friend_sleep_plot(friend_id, week_offset=0):
    # Get metrics for the week
    _, sleep_dict = get_friend_weekly_entries(friend_id, week_offset)
    
    # Plot-ready output
    x_vals = list(sleep_dict.keys())
    y_vals = list(sleep_dict.values())
    
    # Plotly bar chart
    fig = go.Figure(
        data=[go.Scatter(x=x_vals, y=y_vals, mode='lines+markers', line=dict(color='mediumpurple', width=3))],
    )
    fig.update_layout(
        yaxis=dict(title='Hours', range=[0, max(y_vals + [0]) + 1]),
        xaxis=dict(title='Day')
    )
    return plot(fig, output_type='div', include_plotlyjs=False)

def generate_friend_sleep_metrics(friend_id, week_offset=0):
    # Get metrics for the week
    _, sleep_dict = get_friend_weekly_entries(friend_id, week_offset)
    
    # Average Sleep Duration
    total_sleep = sum(sleep_dict.values())
    days_with_data = sum(1 for hours in sleep_dict.values() if hours > 0)
    if days_with_data > 0:
        avg_sleep = total_sleep / days_with_data
    else:
        avg_sleep = 0
    
    # Sleep Consistency
    sleep_dict_duration_consistency = [v for v in sleep_dict.values() if v > 0]
    sorted_sleep_dict = sorted(sleep_dict_duration_consistency)
    n = len(sorted_sleep_dict)
    
    if n > 0 and n % 2 == 1:
        median_sleep = sorted_sleep_dict[n // 2]
    elif n > 0 and n % 2 == 0:
        median_sleep = (sorted_sleep_dict[n // 2 - 1] + sorted_sleep_dict[n // 2]) / 2
    else:
        median_sleep = 0
    
    # Count how many days fall within +/- 30 minutes of the median
    counting_sleep_consistency = sum(1 for hours in sleep_dict_duration_consistency if abs(hours - median_sleep) <= 0.5)
    if counting_sleep_consistency > 0 and n > 0:
        duration_consistency = (counting_sleep_consistency / n) * 100
    else:
        duration_consistency = 0
    
    return avg_sleep, duration_consistency