from todoist import TodoistClient
from google_calendar import CalendarClient
import os
import json
from pathlib import Path
from time import sleep
from dotenv import load_dotenv

load_dotenv()

def compose_state(titles, contents):
    if len(titles) != len(contents):
        print("titles and contents must have the same length")
        return 1

    state = {}
    for title, html in zip(titles, contents):
        state[title] = html

    out_path = Path("./site/state.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def update():
    m = TodoistClient(os.environ.get('M_TODOIST_KEY'))
    m_today = m.get_today()
    m_today = "<h1>Martin Henry</h1>\n" + m_today

    i = TodoistClient(os.environ.get('I_TODOIST_KEY'))
    i_today = i.get_today()
    i_today = "<h1>Isabella Josephine</h1>\n" + i_today

    grocery = i.get_section("GROCERY LIST")
    grocery = "<h1>Provisions</h1>\n" + grocery

    c = CalendarClient()
    c_events = c.get_upcoming_events_html()
    c_events = "<h1>On the Morrow</h1>\n" + c_events

    compose_state(["martin", "izzy", "grocery", "upcoming"], [m_today, i_today, grocery, c_events])


def main():

    while True:
        update()
        sleep(300)

main()