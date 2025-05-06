from datetime import datetime, timedelta
from collections import defaultdict
from app.models import Entry
import plotly.graph_objs as go
from plotly.offline import plot

def generate_sleep_plot(week_offset=0):
    today = datetime.today().date() + timedelta(weeks=week_offset)
    one_week_ago = today - timedelta(days=6)

    entries = Entry.query.filter(
        Entry.sleep_datetime >= datetime.combine(one_week_ago, datetime.min.time())
    ).all()

    # Build dict with actual date objects
    start_of_week = datetime.today().date() + timedelta(weeks=week_offset-1)
    
    sleep_dict = {
        start_of_week + timedelta(days=i): 0
        for i in range(7)
    }
    # Use date keys directly
    for entry in entries:
        if entry.wake_datetime and entry.sleep_datetime:
            duration = (entry.wake_datetime - entry.sleep_datetime).total_seconds() / 3600
            entry_date = entry.sleep_datetime.date()
            if entry_date in sleep_dict:
                sleep_dict[entry_date] += duration  # Only if it's within the week
    # Plot-ready output
    x_vals = list(sleep_dict.keys())     # Dates
    y_vals = list(sleep_dict.values())   # [7.2, 6.5, ..., 0]

    # Plotly bar chart
    fig = go.Figure(
    data=[go.Scatter(x=x_vals, y=y_vals, mode='lines+markers', line=dict(color='mediumpurple', width=3))],
    )
    fig.update_layout(
    yaxis=dict(title='Hours', range=[0, max(y_vals + [0]) + 1]),  # ensure starts from 0
    xaxis=dict(title='Day')
    )   

    # Return as HTML-div
    return plot(fig, output_type='div', include_plotlyjs=False)
