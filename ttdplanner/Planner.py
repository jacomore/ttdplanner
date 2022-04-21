from datetime import datetime
from tabulate import tabulate
import json
import numpy as np


class Planner:

    def __init__(self):
        self.list_of_notes = []


    class Note:

        def __init__(self, title, body, date, tags, id_note):
            self.title = title
            self.body = body
            self.date = date
            self.tags = tags
            self.id = id_note

    def add_note(self, title, body, date, tags, id_note=-1):
        if int(id_note) not in range(9999):
            self.list_of_notes.append(self.Note(title, body, date, tags, self.id_note()))
        else:
            self.list_of_notes.append(self.Note(title, body, date, tags, int(id_note)))

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
            self.add_note(note["title"], note["body"], note["date"], note["tags"], note["id"])

    # def json_to_xlsx (implementazione luigi)

    def print_plan(self):
        plan = []
        for note in self.list_of_notes:
            plan.append([str(note.id).zfill(4), note.title, note.body, note.date, ', '.join(note.tags)])
        print(tabulate(plan, headers=["id", "title", "note", "date", "tags"], tablefmt="fancy_grid", showindex=False))

    def id_note(self):
        if self.list_of_notes == []:
            print("if è verificato")
            return 1

        else:
            return max(note.id for note in self.list_of_notes)+1


    def search_tag(self, tag, notag):
        # writing tag and notag in list form
        tag = tag.split(sep=",") if "," in tag else tag.split()
        notag = notag.split(sep=",") if "," in notag else notag.split()

        #  row indexes to be used for the returned DataFrame
        rows_idx = []

        # tags and list
        tag_list = []
        for note in self.list_of_notes:
            tag_list.append(note.tags)

        # tags searching and notags rejecting
        for idx, tags in enumerate(tag_list):
            if \
                    all(item in tag_list[idx] for item in tag) and \
                    list(np.intersect1d(notag, tag_list[idx])) == []:
                rows_idx.append(idx)

        # creating the planner to return
        plan_by_tag = Planner()
        for idx in rows_idx:
            plan_by_tag.add_note(self.list_of_notes[idx].title, self.list_of_notes[idx].body,
                                 self.list_of_notes[idx].date, self.list_of_notes[idx].tags,
                                 self.list_of_notes[idx].id)

        return plan_by_tag

    def note_by_id(self, id_note):
        id_note = int(id_note)
        for idx, note in enumerate(self.list_of_notes):
            if note.id == id_note:
                return idx

    def search_word(self, word):
        # rewriting word without capital letter
        word = word.lower()
        rows_idx = []

        for idx, item in enumerate(self.list_of_notes):
            title = item.title.lower()
            note = item.body.lower()

            if word in title or word in note:
                rows_idx.append(idx)

        plan_by_word = Planner()
        for idx in rows_idx:
            plan_by_word.add_note(self.list_of_notes[idx].title, self.list_of_notes[idx].body,
                                  self.list_of_notes[idx].date, self.list_of_notes[idx].tags,
                                  self.list_of_notes[idx].id)
        return plan_by_word

    def set_note_title(self, idx, title):
        self.list_of_notes[idx].title = title

    def set_note_title_verbose(self, idx):
        print("insert the new title:")
        title = input()
        self.set_note_title(idx, title)

    def set_note_body(self, idx, body):
        self.list_of_notes[idx].body = body

    def set_note_body_verbose(self, idx):
        print("insert the new note:")
        body = input()
        self.set_note_body(idx, body)

    def set_note_date(self, idx, date):
        self.list_of_notes[idx].date = date

    def set_note_date_verbose(self, idx):
        print("insert the new date:")
        date = input()
        self.set_note_date(idx, date)

    def set_note_tags(self, idx, tags):
        self.list_of_notes[idx].tags = tags

    def set_note_tags_verbose(self, idx):
        print("insert the new tags separated by commas or blank spaces:")
        tags = input()
        tags = tags.split(sep=",") if "," in tags else tags.split(sep=" ")
        self.set_note_tags(idx, tags)
