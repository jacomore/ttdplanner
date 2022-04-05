import argparse
import pandas as pd
from datetime import datetime
import re

from general import update_data


def add_note(
        args: argparse.Namespace,  # parser arguments
        plan: pd.DataFrame  # DataFrame to be updated
):
    """
    Parameters
    ----------
    args: argparse.Namespace. Contains the arguments "title", "note" and "date"
    plan: pd.DataFrame. Contains all the notes

    Returns
    -------
    update_plan: pd.DataFrame with the added note

    Notes
    -----
    This function adds a new note to the existing planner.

    Warnings
    --------
    This function must be updated everytime the columns of the plan are changed
    """

    item = {}
    for name in plan.columns:
        if str(name) != "tags":
            item[str(name)] = vars(args)[str(name)]

    #  these three lines insert a list in the pd.DataFrame. ATTENTION: it is stored as a string
    #  they are needed because pd.DataFrame can't be initialized with nested data
    item["tags"] = "..."
    data = pd.DataFrame(item, index=[0])
    data.at[0, "tags"] = vars(args)[str("tags")]  # use literal_eval('[1.23, 2.34]') to read this data

    plan = plan.append(data)
    update_data(plan)


def add_note_verbose(
        plan: pd.DataFrame  # DataFrame to be updated
):
    """
    Parameters
    ----------
    plan: pd.DataFrame

    Returns
    -------
    plan: pd.DataFrame with the added note

    Notes
    -----
    This function adds a new note to the existing planner.
    It uses an input/output interface; this is more convenient to use with larger notes or notes with tags.

    Warnings
    --------
    This function must be updated everytime the columns of the plan are changed
    """

    item = {}  # initializing the new note

    # title
    title = input("Please, insert the title: ")
    item["title"] = title

    # body
    note = input("It's time to write your note: ")
    item["note"] = note

    # date
    date = input("Insert the date 'Y-m-d'. Press Enter to use the current date: ")
    if date == '':  # insert the current data if requested
        date = datetime.today().strftime('%Y-%m-%d')
    item["date"] = date

    # tags
    tags = input("Insert the tags (separated by a space or a comma): ")
    #  these three lines insert a list in the pd.DataFrame. ATTENTION: it is stored as a string.
    #  they are needed because pd.DataFrame can't be initialized with nested data
    item["tags"] = "..."
    data_bug = pd.DataFrame(item, index=[0])
    data_bug.at[0, "tags"] = re.sub(r"[^\w]", " ", tags).split()  # use literal_eval(list in format <str>) to read this

    # updating the plan
    plan = plan.append(data_bug)
    update_data(plan)
