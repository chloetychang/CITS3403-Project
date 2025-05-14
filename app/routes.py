# Contains routing logic
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from app.forms import UploadSleepDataForm, RecordDateSearchForm, SearchUsernameForm # Import forms
from datetime import date, datetime, timedelta
import calendar
from app.models import db, User, Entry, FriendRequest  # Import models from database
from app.results import generate_sleep_plot, generate_sleep_metrics, generate_mood_metrics
from app.rem_cycle import rem_cycle, simulate_rem_cycle, generate_rem_plot
from app.friend_results import generate_friend_sleep_plot, generate_friend_sleep_metrics

main = Blueprint('main', __name__)

# Welcome / Introductory Page Route
@main.route("/")
def welcome():
    return render_template("welcome.html")


# Sleep Page Routes (Upload Sleep Data)
@main.route("/sleep")
@login_required # Protected page - added decorator to ensure user is logged in
def sleep():
    # Check if the user is logged in using Flask-Login
    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "error")
        return redirect(url_for("main.login"))
    form = UploadSleepDataForm()                            # Create an instance of the UploadSleepDataForm
    return render_template("sleep.html", form=form)


@main.route("/form_popup", methods=["POST"])
def form_popup():
    form = UploadSleepDataForm()
    if form.validate_on_submit():
        # Get the user ID via Flask-Login
        user_id = current_user.user_id
        entry_date_sleep = form.entry_date_sleep.data
        sleep_time = form.sleep_time.data
        entry_date_wake = form.entry_date_wake.data
        wake_time = form.wake_time.data

        sleep_datetime = datetime.combine(entry_date_sleep, sleep_time)
        wake_datetime = datetime.combine(entry_date_wake, wake_time) if entry_date_wake and wake_time else None

        # Check if the sleep time is before the wake time
        if wake_datetime and sleep_datetime >= wake_datetime:
            flash("Unsuccessful Submission - Sleep time must be before wake time.", "error")
            return render_template("sleep.html", form=form)

        # Check if the sleep time is in the future
        if sleep_datetime > datetime.now():
            flash("Unsuccessful Submission - Sleep time cannot be in the future.", "error")
            return render_template("sleep.html", form=form)

        # Check if the wake time is in the future
        if wake_datetime and wake_datetime > datetime.now():
            flash("Unsuccessful Submission - Wake time cannot be in the future.", "error")
            return render_template("sleep.html", form=form)

        # Create a new entry instance - fields as defined in forms.py
        new_entry = Entry(
            user_id = user_id,
            sleep_datetime = sleep_datetime,
            wake_datetime = wake_datetime,                  # Optional
            mood = form.mood.data
        )
        db.session.add(new_entry) # Add the new entry to the session
        db.session.commit()  # Save the new entry to the database

        flash("Sleep data recorded successfully!", "success")
        return redirect(url_for("main.sleep"))  # Redirect to sleep page after successful submission

    return render_template("sleep.html", form=form)


# Record Page Routes
@main.route("/record")
@login_required
def record():
    form = RecordDateSearchForm()
    # Get the current month or the one from the query string
    month_str = request.args.get("month")
    if month_str:
        try:
            year, month = map(int, month_str.split("-"))
            current_date = datetime(year, month, 1)
        except ValueError:
            flash("Invalid month format.", "error")
            return redirect(url_for("main.record"))
    else:
        current_date = datetime.now()

    # Get the current year and month
    year = current_date.year
    month = current_date.month
    month_name = current_date.strftime("%B")

    # Get the number of days in the month and the starting weekday
    days_in_month = calendar.monthrange(year, month)[1]
    first_weekday = calendar.monthrange(year, month)[0]  # 0 = Monday, 6 = Sunday
    days = list(range(1, days_in_month + 1))

    # Get navigation links
    prev_month = (current_date.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
    next_month = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1).strftime("%Y-%m")

    # Query sleep data for the current month
    start_of_month = datetime(year, month, 1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    entries = Entry.query.filter(
        Entry.user_id == current_user.user_id,
        Entry.wake_datetime >= start_of_month,
        Entry.wake_datetime <= end_of_month
    ).all()

    # Calculate sleep durations for each day based on wake-up date
    sleep_data = {}
    for entry in entries:
        if entry.wake_datetime and entry.sleep_datetime:
            duration = (entry.wake_datetime - entry.sleep_datetime).total_seconds() / 3600
            date_key = entry.wake_datetime.date().strftime("%Y-%m-%d")  # Use wake-up date as the key
            sleep_data[date_key] = sleep_data.get(date_key, 0) + duration

    return render_template(
        "record.html",
        days=days,
        year=year,
        month=month,
        month_name=month_name,
        month_number=f"{month:02}",
        prev_month=prev_month,
        next_month=next_month,
        current_month=datetime.now().strftime("%Y-%m"),
        sleep_data=sleep_data,
        first_weekday=first_weekday  # Pass the starting weekday to the template
    )

# Fetch sleep data for a specific date
@main.route('/get_sleep_data')
def get_sleep_data():
    date_str = request.args.get('date')  # Expected format: 'YYYY-MM-DD'
    if not date_str:
        return jsonify({"error": "Date parameter is missing"}), 400

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid date format"}), 400

    try:
        # Filter entries where the wake_datetime date matches the selected date
        entries = Entry.query.filter(
            Entry.user_id == current_user.user_id,
            db.func.date(Entry.wake_datetime) == selected_date
        ).all()

        if not entries:
            return jsonify([])  # Return an empty list if no entries are found

        result = []
        for entry in entries:
            # Calculate sleep duration if wake_datetime is available
            if entry.wake_datetime:
                duration = entry.wake_datetime - entry.sleep_datetime
                duration_hours = duration.total_seconds() // 3600
                duration_minutes = (duration.total_seconds() % 3600) // 60
                formatted_duration = f"{int(duration_hours)}h {int(duration_minutes)}m"
            else:
                formatted_duration = "N/A"

            # Format the fields for results
            result.append({
                "entry_id": entry.entry_id,
                "sleep_date": entry.sleep_datetime.strftime("%d %B %Y"),
                "sleep_time": entry.sleep_datetime.strftime("%H:%M"),
                "wake_date": entry.wake_datetime.strftime("%d %B %Y") if entry.wake_datetime else None,
                "wake_time": entry.wake_datetime.strftime("%H:%M") if entry.wake_datetime else None,
                "mood": entry.mood,
                "sleep_duration": formatted_duration
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching data"}), 500

# Delete a sleep entry in the database
@main.route('/delete_sleep_entry/<int:entry_id>', methods=['DELETE'])
@login_required
def delete_sleep_entry(entry_id):
    try:
        entry = Entry.query.get_or_404(entry_id)
        
        # Check if the user owns this entry
        if entry.user_id != current_user.user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message": "Entry deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
   
   
# Results Page Routes 
@main.route("/results")
@login_required # Protected page
def results():
    # Check if the user is logged in using Flask-Login
    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "error")
        return redirect(url_for("main.login"))
    
    week_offset = int(request.args.get("week_offset", -1))          # Default to -1 if not provided - previous week's (past 7 days) data
    
    # Don't allow next week if it's in the future
    today = date.today()
    requested_start_date = today + timedelta(1) + timedelta(weeks=week_offset)
    if requested_start_date > today:
        week_offset = -1  # reset if user tries to go too far forward
        
    start_date = date.today() + timedelta(1) + timedelta(weeks=week_offset)
    end_date = start_date + timedelta(days=6)
    week_range = f"{start_date.strftime('%b %d (%A)')} – {end_date.strftime('%b %d (%A)')}"
    
    sleep_plot_div = generate_sleep_plot(week_offset)                           # Sleep Plot - Generates Weekly Overview of Sleep Duration
    avg_sleep, duration_consistency = generate_sleep_metrics(week_offset)       # Sleep Metrics
    avg_mood, max_mood, max_day, hours, highest_day_sleep, highest_day_wake = generate_mood_metrics(week_offset)     # Mood Metrics
    
    best_sleep, best_wake = rem_cycle(week_offset)
    if best_sleep and best_wake:
        rem_data = simulate_rem_cycle(best_sleep, best_wake)
        rem_plot_div = generate_rem_plot(rem_data)
    else:
        rem_plot_div = "<p>No mood-based REM data for this week.</p>" 
    
    return render_template(
        "results.html", 
        week_offset=week_offset, 
        week_range=week_range, 
        plot_div=sleep_plot_div, 
        average_sleep=avg_sleep, 
        duration_consistency_percentage=duration_consistency, 
        average_mood=avg_mood, 
        highest_mood=max_mood, 
        highest_day=max_day, 
        mood_duration=hours, 
        highest_mood_sleep = highest_day_sleep, 
        highest_mood_wake = highest_day_wake, 
        rem_plot_div=rem_plot_div
    )


# Share Page Routes
@main.route('/share', methods=['GET', 'POST'])
@login_required
def share():
    search_term = request.args.get('search', '')
    search_results = []

    # If there's a search term in the query parameters, perform the search
    if search_term:
        # Search for usernames containing the search term (case-insensitive)
        search_results = User.query.filter(
            User.username.ilike(f'%{search_term}%'),
            User.user_id != current_user.user_id  # Exclude current user
        ).all()

        if not search_results:
            flash("No users found with that username", "info")

    # Get friends and pending requests
    friends = current_user.friends.all()

    pending_requests = []
    friend_requests = FriendRequest.query.filter(
        FriendRequest.recipient_id == current_user.user_id,
        FriendRequest.status == 'pending'
    ).all()

    # Add sender's name to each request for display
    for friend_request in friend_requests:
        sender = User.query.get(friend_request.sender_id)
        if sender:
            # Add these attributes for the template
            friend_request.sender_name = sender.username
            friend_request.request_id = friend_request.id  # Make sure ID is accessible
            pending_requests.append(friend_request)

    return render_template('share.html',
                         friends=friends,
                         pending_requests=pending_requests,
                         search_results=search_results)

@main.route('/send_friend_request/<int:user_id>', methods=['POST'])
@login_required
def send_friend_request(user_id):
    recipient = User.query.get(user_id)

    if not recipient:
        flash("User not found", "error")
        return redirect(url_for('main.share'))

    if recipient.user_id == current_user.user_id:
        flash("You can't send a friend request to yourself", "error")
        return redirect(url_for('main.share'))

    # Check if request already exists
    existing_request = FriendRequest.query.filter_by(
        sender_id=current_user.user_id,
        recipient_id=user_id
    ).first()

    if existing_request:
        flash("Friend request already sent", "info")
        return redirect(url_for('main.share'))

    # Create new request
    new_request = FriendRequest(
        sender_id=current_user.user_id,
        recipient_id=user_id
    )

    db.session.add(new_request)
    db.session.commit()

    flash("Friend request sent successfully!", "success")
    return redirect(url_for('main.share'))

@main.route('/handle_friend_request/<int:request_id>', methods=['POST'])
@login_required
def handle_friend_request(request_id):
    # Parse the JSON data from the request
    data = request.json
    action = data.get('action')

    # Find the friend request
    friend_request = FriendRequest.query.get(request_id)

    if not friend_request:
        return jsonify({'error': 'Request not found'}), 404

    # Make sure the current user is the recipient of the request
    if friend_request.recipient_id != current_user.user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    if action == 'accept':
        # Update request status
        friend_request.status = 'accepted'

        # Add to friends list (both ways since it's a mutual friendship)
        sender = User.query.get(friend_request.sender_id)

        # Add the sender to current user's friends
        if sender not in current_user.friends:
            current_user.friends.append(sender)

        # Add current user to sender's friends
        if current_user not in sender.friends:
            sender.friends.append(current_user)

        db.session.commit()

        flash("Friend request accepted!", "success")
        return jsonify({'status': 'success', 'message': 'Friend request accepted'})

    elif action == 'decline':
        # Update request status
        friend_request.status = 'declined'
        db.session.commit()

        flash("Friend request declined", "info")
        return jsonify({'status': 'success', 'message': 'Friend request declined'})

    else:
        return jsonify({'error': 'Invalid action'}), 400

@main.route('/unfriend/<int:friend_id>', methods=['POST'])
@login_required
def unfriend(friend_id):
    # Get the friend user object
    friend = User.query.get(friend_id)

    if not friend:
        return jsonify({'error': 'User not found'}), 404

    # Remove from current_user's friends list
    if friend in current_user.friends:
        current_user.friends.remove(friend)

    # Remove current_user from friend's friends list (mutual friendship)
    if current_user in friend.friends:
        friend.friends.remove(current_user)

    # Clean up any existing friend requests between these users (in both directions)
    # This allows them to send friend requests to each other again in the future
    FriendRequest.query.filter(
        ((FriendRequest.sender_id == current_user.user_id) & 
         (FriendRequest.recipient_id == friend_id)) |
        ((FriendRequest.sender_id == friend_id) & 
         (FriendRequest.recipient_id == current_user.user_id))
    ).delete()

    # Commit the changes
    db.session.commit()

    flash("Friend removed successfully", "info")
    return jsonify({'status': 'success', 'message': 'Friend removed successfully'})

@main.route("/friend_sleep_data/<int:friend_id>")
@login_required
def friend_sleep_data(friend_id):
    # Verify this user is a friend
    friend = User.query.get_or_404(friend_id)
    if friend not in current_user.friends:
        flash("You can only view sleep data for your friends.", "error")
        return redirect(url_for("main.share"))
    
    # Get sleep data for the friend (similar to the results route)
    week_offset = int(request.args.get("week_offset", -1))
    
    # Don't allow next week if it's in the future
    today = date.today()
    requested_start_date = today + timedelta(1) + timedelta(weeks=week_offset)
    if requested_start_date > today:
        week_offset = -1 # reset if user tries to go too far forward
    
    start_date = date.today() + timedelta(1) + timedelta(weeks=week_offset)
    end_date = start_date + timedelta(days=6)
    week_range = f"{start_date.strftime('%b %d (%A)')} – {end_date.strftime('%b %d (%A)')}"
    
    # Generate friend's sleep plot
    sleep_plot_div = generate_friend_sleep_plot(friend_id, week_offset)
    avg_sleep, duration_consistency = generate_friend_sleep_metrics(friend_id, week_offset)
    
    return render_template(
        "friend_sleep_data.html", 
        friend=friend,
        week_offset=week_offset, 
        week_range=week_range, 
        plot_div=sleep_plot_div, 
        average_sleep=avg_sleep, 
        duration_consistency_percentage=duration_consistency
    )