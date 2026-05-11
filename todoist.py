from todoist_api_python.api import TodoistAPI
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict

class TodoistClient:
    def __init__(self, api_key: str):
        self.api = TodoistAPI(api_key)


    def get_today(self):
        print("Fetching tasks...")
        tasks_paginator = self.api.get_tasks()

        priority_buckets = defaultdict(list)

        for batch in tasks_paginator:
            for t in batch:
                if t.parent_id is not None:
                    continue
                if t.completed_at is not None:
                    continue
                if t.due is None or t.due.date is None:
                    continue

                due_date = t.due.date

                if isinstance(due_date, datetime):
                    due_date = due_date.date() # strip time if applicable

                today = datetime.now().date()

                if due_date <= today:
                    reversed_priority = 5 - t.priority
                    priority_buckets[reversed_priority].append(t.content)

        html_lines = []
        for prio in sorted(priority_buckets.keys()):
            tasks = priority_buckets[prio]
            if not tasks:
                continue
            labels = {
                1: "chief intent",
                2: "secondary",
                3: "perhaps later",
                4: "can't be bothered lol",
            }

            html_lines.append(f"<b>{labels.get(prio, f'Priority {prio}')}</b>")
            # html_lines.append("<hr>")
            html_lines.append("<ul>")
            for task_content in tasks:
                html_lines.append(f"<li>{task_content}</li>")
            html_lines.append("</ul>")

        html_string = "\n".join(html_lines)
        return html_string

    def _get_section_obj(self, section_name: str):
        sections = []
        for batch in self.api.get_sections():
            sections.extend(batch)
        section = next((s for s in sections if s.name.lower() == section_name.lower()), None)
        if section is None:
            raise ValueError(f"Section not found: {section_name}")
        return section

    def get_section(self, section_name: str) -> str:
        print(f"Fetching section '{section_name}'...")
        section = self._get_section_obj(section_name)

        tasks = []
        for batch in self.api.get_tasks(section_id=section.id):
            for t in batch:
                if t.parent_id is not None:
                    continue
                if t.completed_at is not None:
                    continue
                tasks.append(t.content)

        html_lines = ["<ul>"]
        for task_content in tasks:
            html_lines.append(f"<li>{task_content}</li>")
        html_lines.append("</ul>")

        return "\n".join(html_lines)

    def get_days_old(self, section_name: str) -> str:
        print(f"Fetching days-old section '{section_name}'...")
        section = self._get_section_obj(section_name)

        tasks = []
        for batch in self.api.get_tasks(section_id=section.id):
            for t in batch:
                if t.parent_id is not None:
                    continue
                if t.completed_at is not None:
                    continue
                tasks.append(t)

        today = date.today()
        html_lines = ["<ul>"]
        for t in tasks:
            created = t.created_at
            if isinstance(created, datetime):
                created = created.date()
            elif not isinstance(created, date):
                created = datetime.fromisoformat(str(created)).date()
            days_old = (today - created).days
            html_lines.append(f"<li><b>{days_old} Days old:</b> {t.content}</li>")
        html_lines.append("</ul>")

        return "\n".join(html_lines)

