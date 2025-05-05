from datetime import datetime, timedelta
from collections import defaultdict
from app.models import Entry
import plotly.graph_objs as go
from plotly.offline import plot

def generate_sleep_plot():
    today = datetime.today().date()
    one_week_ago = today - timedelta(days=6)

    entries = Entry.query.filter(
        Entry.sleep_datetime >= datetime.combine(one_week_ago, datetime.min.time())
    ).all()

    # Group by day
    sleep_accumulator = defaultdict(list)
    for entry in entries:
        if entry.wake_datetime and entry.sleep_datetime:
            duration = (entry.wake_datetime - entry.sleep_datetime).total_seconds() / 3600
            day = entry.sleep_datetime.strftime('%A')
            sleep_accumulator[day].append(duration)

    # Prepare 7-day structure
    sleep_dict = { (today - timedelta(days=i)).strftime('%A'): 0 for i in reversed(range(7)) }
    for day, durations in sleep_accumulator.items():
        sleep_dict[day] = sum(durations)  # or use average if you prefer

    # Plot-ready output
    x_vals = list(sleep_dict.keys())     # ['Monday', ..., 'Sunday']
    y_vals = list(sleep_dict.values())   # [7.2, 6.5, ..., 0]

    # Plotly bar chart
    fig = go.Figure(
        data=[go.Bar(x=x_vals, y=y_vals, marker_color='lightblue')],
        layout_title_text='Weekly Sleep Duration (hours)'
    )
    fig.update_layout(yaxis=dict(title='Hours'), xaxis=dict(title='Day'))

    # Return as HTML-div
    return plot(fig, output_type='div', include_plotlyjs=False)
