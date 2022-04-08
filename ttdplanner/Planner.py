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

    def update_plan(self, plan):
        self.list_of_notes = plan

    def print_plan(self):
        heads = self.list_of_notes[0]
        tab_plan = tabulate(self.list_of_notes[1:], headers=heads,
        tablefmt='orgtbl')
        print(tab_plan)
