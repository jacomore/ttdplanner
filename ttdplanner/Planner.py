import pickle
from datetime import datetime
from tabulate import tabulate


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
        this function saves plan in file.pkl in path
        """
        with open(path, 'wb') as out:
            pickle.dump(self, out, pickle.HIGHEST_PROTOCOL)


    def print_plan(self):
        heads = self.list_of_notes[0]
        tab_plan = tabulate(self.list_of_notes[1:], headers=heads,
        tablefmt='orgtbl')
        print(tab_plan)
