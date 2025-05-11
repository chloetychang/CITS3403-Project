import plotly.graph_objs as go
from plotly.offline import plot
from app.get_weekly_entries import get_weekly_entries

# Sleep Plot
def generate_sleep_plot(week_offset=0):
    # Get metrics for the week - logic in app.get_weekly_entries
    _, sleep_dict = get_weekly_entries(week_offset)
                
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
    return plot(fig, output_type='div', include_plotlyjs=False)

# Sleep Metrics
def generate_sleep_metrics(week_offset=0):
    # Get metrics for the week - logic in app.get_weekly_entries
    _, sleep_dict = get_weekly_entries(week_offset)
    
    # Average Sleep Duration - Weekly: Calculate average hours of sleep in a week
    total_sleep = sum(sleep_dict.values())
    days_with_data = sum(1 for hours in sleep_dict.values() if hours > 0)
    if days_with_data > 0:
        avg_sleep = total_sleep / days_with_data
    else:
        avg_sleep = 0 
        
    # Sleep Consistency: Check if sleep duration is consistent by looking at how many days of sleep data falls within a certain range
    ## Calculate median sleep time of the week (time that user went to bed)
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

    # Plot: Return as HTML-div, plus other metrics
    return avg_sleep, duration_consistency

# Mood Metrics
def generate_mood_metrics(week_offset=0):
    # Get metrics for the week - logic in app.get_weekly_entries
    entries, _ = get_weekly_entries(week_offset)
    
    count_mood = sum([1 if entry.mood is not None else 0 for entry in entries])
    
    # Get the entry with the highest mood, and break ties by duration
    if entries:
        best_entry = max(
            entries,
            key=lambda e: (e.mood, (e.wake_datetime - e.sleep_datetime).total_seconds())
        )
    else:
        best_entry = None
    
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
        # Now extract what you need
        highest_day = best_entry.wake_datetime.strftime('%Y-%m-%d (%A)')
        hours = (best_entry.wake_datetime - best_entry.sleep_datetime).total_seconds() / 3600
        highest_day_sleep = best_entry.sleep_datetime
        highest_day_wake = best_entry.wake_datetime
        
    return average_mood, max_mood, highest_day, hours, highest_day_sleep, highest_day_wake
