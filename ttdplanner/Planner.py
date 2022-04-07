import pickle
import csv
import os


class Planner:

    def __init__(self):
        self.list_of_notes = []

    class Note:

        def __init__(self, title, body, date, tags):
            self.title = title
            self.body = body
            self.date = date
            self.tags = tags

    def add_note(self, title, body, date, tags):
        self.list_of_notes.append(self.Note(title, body, date, tags))

    def update_planner(self, plan):
        self.list_of_notes = plan
