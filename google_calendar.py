import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class CalendarClient:
    def __init__(self, credentials_path="credentials.json", token_path="token.json"):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open(self.token_path, "w") as f:
                f.write(self.creds.to_json())

        self.service = build("calendar", "v3", credentials=self.creds)

    def _ordinal(self, n: int) -> str:
        if 10 <= n % 100 <= 20:
            return f"{n}th"
        return f"{n}{ {1:'st',2:'nd',3:'rd'}.get(n % 10, 'th') }"

    def get_upcoming_events_html(self, calendar_id="primary", max_events=5):
        now = datetime.datetime.utcnow().isoformat() + "Z"

        result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=max_events,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        events = result.get("items", [])

        if not events:
            return "<ul><li>No upcoming events</li></ul>"

        html = "<ul>"

        for i, event in enumerate(events):
            start_raw = event["start"].get("dateTime", event["start"].get("date"))

            if "dateTime" in event["start"]:
                start_dt = datetime.datetime.fromisoformat(start_raw.replace("Z", "+00:00"))
            else:
                start_dt = datetime.date.fromisoformat(start_raw)

            # date
            month = start_dt.strftime("%b")
            day = self._ordinal(start_dt.day)
            date_str = f"{month} {day}"

            # time
            time_str = ""
            if isinstance(start_dt, datetime.datetime):
                time_str = start_dt.strftime(" - %I:%M %p").lstrip("0")

            title = event.get("summary", "No Title")
            location = event.get("location", "").strip()

            html += "<li>"
            html += f"{date_str}{time_str}<br>"
            html += f"<b>{title}</b>"

            if location:
                html += f"<br>{location}"

            html += "</li>"

            if i < len(events) - 1:
                html += "<hr>"

        html += "</ul>"
        return html

