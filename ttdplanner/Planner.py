import pickle
import csv  # usare per leggere la classe
import os

class Planner:

    def __init__(self):
        self.list_of_notes = self.read_plan()

    def read_plan(self):
        # finding the current directory
        loc_dir = os.path.abspath(os.getcwd())

        # moving to the parent folder and into "data" folder
        dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))

        # path to "data.csv" file
        data_path = os.path.abspath(os.path.join(dir_path, "data.csv"))
        file = open(data_path, "r")
        rows = []
        for row in csv.reader(file):
            rows.append(row)
        print(rows)
        return rows

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
