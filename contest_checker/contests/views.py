from django.shortcuts import render
from django.utils.timezone import now
import requests
import pytz
from datetime import datetime, timedelta

def get_client_ip(request):
    """Extract the client's IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_timezone_from_ip(ip_address):
    """Get timezone based on IP address using a third-party API."""
    try:
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        data = response.json()
        return data.get('timezone', 'Asia/Dhaka')  # Default to 'Asia/Dhaka' if not available
    except Exception:
        return 'Asia/Dhaka'  # Fallback timezone

def get_future_contests(request):
    """Fetch future contests from the Codeforces API."""
    # Get client IP and timezone
    client_ip = get_client_ip(request)
    user_timezone = get_timezone_from_ip(client_ip)

    # Validate and handle timezone
    try:
        timezone = pytz.timezone(user_timezone)
    except Exception:
        timezone = pytz.timezone('Asia/Dhaka')

    # Fetch contests from Codeforces API
    response = requests.get('https://codeforces.com/api/contest.list')
    contests = response.json().get('result', [])

    # Filter future contests
    current_time = now()
    future_contests = []
    for contest in contests:
        if contest['phase'] == 'BEFORE':
            start_time = datetime.utcfromtimestamp(contest['startTimeSeconds']).replace(tzinfo=pytz.utc).astimezone(timezone)
            future_contests.append({
                'name': contest['name'],
                'start_time': start_time,
                'url': f"https://codeforces.com/contest/{contest['id']}"
            })

    # Prepare data for the calendar
    calendar = []
    today = current_time.astimezone(timezone).date()
    for i in range(30):  # Next 30 days
        date = today + timedelta(days=i)
        contests_on_day = [
            {
                'name': c['name'],
                'time': c['start_time'].strftime('%I:%M %p'),
                'url': c['url']
            }
            for c in future_contests if c['start_time'].date() == date
        ]
        calendar.append({
            'date': date.strftime('%Y-%m-%d'),
            'is_weekend': date.weekday() in [4, 5],  # Friday and Saturday
            'contests': contests_on_day
        })

    return render(request, 'calendar.html', {'calendar': calendar})
