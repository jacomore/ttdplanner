from datetime import datetime
from tabulate import tabulate
import json


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

    def add_note_verbose(self):
        # title
        title = input("Please, insert the title: ")
        # body
        body = input("It's time to write your note: ")
        # date
        date = input("Insert the date 'Y-m-d'. Press Enter to use the current date: ")
        if date == '':  # insert the current data if requested
            date = datetime.today().strftime('%Y-%m-%d')
        # tags
        tags = input("Insert the tags (separated by a space or a comma): ")
        tags = tags.split(sep=",") if "," in tags else tags.split(sep=" ")
        # create the note
        self.add_note(title, body, date, tags)

    def save(self, path):
        """
        this function saves plan in json format in path
        """
        with open(path, 'w') as outfile:
            json.dump(self, outfile, default=lambda o: o.__dict__, indent=1)

    def read_plan(self, path):
        with open(path, 'r') as json_file:
            temp = json.load(json_file)

        for note in temp["list_of_notes"]:
            self.add_note(note["title"], note["body"], note["date"], note["tags"])

    # def json_to_xlsx (implementazione luigi)

    def print_plan(self):
        plan = []
        for note in self.list_of_notes:
            plan.append([note.title, note.body, note.date, ', '.join(note.tags)])
        print(tabulate(plan, headers=["title", "note", "date", "tags"], tablefmt="fancy_grid", showindex=False))
