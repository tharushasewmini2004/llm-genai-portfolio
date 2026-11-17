"""Google Calendar tools: create an event and check today's schedule.

First run: a browser window opens so you can sign in to Google and allow access.
The permission is saved in token.json, so you only do this once.
Needs credentials.json (OAuth client, Desktop app) from the Google Cloud Console.
"""
import datetime
import os

from langchain_core.tools import tool

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TIMEZONE = "Asia/Colombo"
COLOMBO = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


def _service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


@tool
def get_todays_schedule() -> str:
    """Get today's events from the user's Google Calendar."""
    now = datetime.datetime.now(COLOMBO)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + datetime.timedelta(days=1)
    try:
        events = _service().events().list(
            calendarId="primary", timeMin=start.isoformat(), timeMax=end.isoformat(),
            singleEvents=True, orderBy="startTime").execute().get("items", [])
    except Exception as e:
        return f"Could not read the calendar: {e}"
    if not events:
        return "No events today."
    lines = []
    for ev in events:
        when = ev["start"].get("dateTime", ev["start"].get("date"))
        lines.append(f"- {when[11:16] if 'T' in when else 'All day'}  {ev.get('summary', '(no title)')}")
    return "Today's events:\n" + "\n".join(lines)


@tool
def create_calendar_event(title: str, date: str, start_time: str, duration_minutes: int = 60) -> str:
    """Create an event in the user's Google Calendar. date is YYYY-MM-DD, start_time is 24-hour HH:MM.
    The user is asked to approve before the event is created."""
    try:
        start = datetime.datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return "Could not understand the date or time. Use date YYYY-MM-DD and time HH:MM (24-hour)."
    end = start + datetime.timedelta(minutes=int(duration_minutes))
    answer = input(f"\n  Create event '{title}' on {date} at {start_time} for {duration_minutes} min? (y/n): ")
    if answer.strip().lower() != "y":
        return "The user did not approve, so no event was created."
    body = {"summary": title,
            "start": {"dateTime": start.isoformat(), "timeZone": TIMEZONE},
            "end": {"dateTime": end.isoformat(), "timeZone": TIMEZONE}}
    try:
        ev = _service().events().insert(calendarId="primary", body=body).execute()
    except Exception as e:
        return f"Could not create the event: {e}"
    return f"Event created: {title} on {date} at {start_time}. Link: {ev.get('htmlLink')}"
