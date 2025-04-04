from dataclasses import dataclass, field
from datetime import datetime, date, time
from math import remainder
from typing import ClassVar

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error


@dataclass
class Reminder:
        EMAIL: ClassVar[str] = "email"
        SYSTEM: ClassVar[str] = "system"
        date_time: datetime
        type: str = EMAIL

        def __str__(self):
            return f"Reminder on {self.date_time} of type {self.type}"


@dataclass
class Event:
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    reminders: list[Reminder] = field(default_factory = list)
    id: str = field(default_factory=generate_unique_id)

    def add_reminder(self, date_time: datetime, type: str):
        reminder = Reminder(date_time, type)
        self.reminders.append(reminder)

    def delete_reminder(self, reminder_index:int):
        if 0 <= reminder_index < len(self.reminders):
            self.reminders.pop(reminder_index)
        else:
            reminder_not_found_error()

    def __str__(self):
            return f"ID: {self.id} Event title: {self.title} Description: {self.description} Time: {self.start_at} - {self.end_at}"


class Day:
    def __init__(self, date_: date, ):
        self.date_: date = date_
        self.slots: dict[time, str | None] = {}
        self._init_slots()

    def _init_slots(self):
        self.slots  = {
            time( minutos //60, minutos % 60): None
            for minutos in range (0, 24 * 60, 15)
                       }

    def add_event(self, event_id: str, start_at: time, end_at: time):
        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                    slot_not_available_error()
            return event_id


    def delete_event(self, event_id: str):
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True
        if not deleted:
            event_not_found_error()

    def update_event(self, event_id: str, start_at: time, end_at: time):
        for slot in self.slots:
            if self.slots[slot] == event_id:
                self.slots[slot] = None

        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                    slot_not_available_error()
                else:
                    self.slots[slot] = event_id

class Calendar:

    def __init__(self):
        self.days: dict[date, Day] = {}
        self.events: dict[str, Event] = {}

    def add_event(self, title: str, description: str, date_: date, start_at: time, end_at: time):
        if date_ < datetime.now().date():
            date_lower_than_today_error()
        if date_ not in self.days:
            self.days[date_] = Day(date_)







    











