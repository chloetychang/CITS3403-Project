from app.models import Entry
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from flask_login import current_user

def rem_cycle(week_offset=0):
    # Step 1: Compute the week range
    start_of_week = datetime.today().date() + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)

    # Step 2: Get the best mood entry within that week
    best_entry = Entry.query.filter(
        Entry.user_id == current_user.user_id,
        Entry.wake_datetime >= datetime.combine(start_of_week, datetime.min.time()),
        Entry.wake_datetime <= datetime.combine(end_of_week, datetime.max.time()),
        Entry.sleep_datetime.isnot(None),
        Entry.wake_datetime.isnot(None),
        Entry.mood.isnot(None)
    ).order_by(Entry.mood.desc()).first()

    if best_entry:
        best_sleep_datetime = best_entry.sleep_datetime
        best_wake_datetime = best_entry.wake_datetime
        return best_sleep_datetime, best_wake_datetime
    return None, None

def simulate_rem_cycle(start, end):
    total_minutes = int((end - start).total_seconds() // 60)
    time_stamps = [start + timedelta(minutes=i) for i in range(total_minutes)]

    cycle_pattern = [1, 2, 3, 2, 1, 4]  # Light -> Moderate -> Deep -> REM
    cycle_length = 90
    stage_map = {1: "Stage 1", 2: "Stage 2", 3: "Stage 3", 4: "REM"}
    stages = []

    for _ in range(total_minutes // cycle_length):
        for stage in cycle_pattern:
            duration = cycle_length // len(cycle_pattern)
            stages += [stage_map[stage]] * duration

    stages = stages[:len(time_stamps)]
    if len(stages) < len(time_stamps):
        stages += [stages[-1]] * (len(time_stamps) - len(stages))

    return list(zip(time_stamps, stages))

def generate_rem_plot(rem_data):
    df = pd.DataFrame(rem_data, columns=["Time", "Stage"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Time'],
        y=df['Stage'],
        mode='lines',
        line_shape='hv',
        name='Sleep Stage'
    ))

    fig.update_layout(
        yaxis=dict(
            title='Sleep Stage',
            categoryorder='array',
            categoryarray=["REM", "Stage 1", "Stage 2", "Stage 3"]
        ),
        xaxis_title='Time',
        height=500
    )
    return fig.to_html(full_html=False)
