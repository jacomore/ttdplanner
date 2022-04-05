import argparse
import os
import pandas as pd
from datetime import datetime
from tabulate import tabulate
import re
from ast import literal_eval
import numpy as np


def init_data(
) -> pd.DataFrame:
    """
    Return
    -------
    Plan: pd.DataFrame. Item of the planner

    Notes
    -------
    Reads the plan from the file in "pwd/../data/data.csv" and initialise it 
    into the plan pandas DataFrame. If either "data" folder or "data.csv" or both
    of them do not exist, it creates this file.

    """
    # Features of the plan
    features = ["title", "note", "date", "tags"]

    # Initialise the plan as dataframe object
    plan = pd.DataFrame(columns=features)

    # finding the current directory
    loc_dir = os.path.abspath(os.getcwd())

    # moving to the parent folder and into "data" folder
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))

    # path to "data.csv" file
    data_path = os.path.abspath(os.path.join(dir_path, "data.csv"))

    # If the folder does not exist yet
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        plan.to_csv(data_path, index=False)
    # If the folder already exists
    else:
        # If "data.csv" does not exist yet
        if not os.path.exists(data_path):
            plan.to_csv(data_path, index=False)
        # If "data.csv" already exists 
        else:
            plan = pd.read_csv(data_path, index_col=False)
    # returning plan
    return plan


def update_data(
        plan: pd.DataFrame
):
    """
    Parameters
    ----------
    plan: pd.DataFrame. Contains all the notes
    
    Notes
    ----
    This function takes in input the updated version of plan and 
    overwrite the existing local copy in "Data/data.csv"
    """
    # finding the current directory
    loc_dir = os.path.abspath(os.getcwd())

    # moving to the parent directory and into "data" folder
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))

    # path to the "data.csv" file
    data_path = os.path.abspath(os.path.join(dir_path, "data.csv"))

    #    plan["date"] = pd.to_datetime(plan["date"], format = '%Y-%m-%d', errors='coerce')

    #    plan["date"] = plan["date"].dt.date

    #    plan_sorted = plan.sort_values(by="date")

    # overwriting data
    plan.to_csv(data_path, index=False)
    pass


def sort_by_date(
        plan: pd.DataFrame  # DataFrame to be sorted
):
    """
     Parameters
    ----------
    plan: pd.DataFrame. Contains all the notes

    Returns
    -------
    plan_sorted: pd.DataFrame. Contains all the note sorted by time

    Notes
    ----
    This function sort the notes by time, from the oldest to the most recent.
    """

    plan["date"] = pd.to_datetime(plan["date"], format='%Y-%m-%d', errors='coerce')

    plan["date"] = plan["date"].dt.date

    plan_sorted = plan.sort_values(by="date")

    return plan_sorted


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


def print_planner(
        plan: pd.DataFrame
):
    """
    Parameters
    ----------
    plan: pd.DataFrame. Contains all the notes
    
    Notes
    ----
    The function prints in the terminal all the notes in a table
    """

    # Extracting the actual indexes of the pandas (it may have been
    # truncated in search_word)
    idx_plan = plan.index.to_list()

    #  convert the tags in a readable format, it accepts both list and string convertible in list
    for i, tag in enumerate(plan["tags"]):
        if type(tag) is str:
            plan.at[idx_plan[i], "tags"] = ', '.join(literal_eval(plan.at[idx_plan[i], 'tags']))
        elif type(tag) is list:
            plan.at[idx_plan[i], "tags"] = ', '.join(tag)

    # table creation
    plan_tab = lambda plan: tabulate(plan,
                                     headers=[str(plan.columns[0]), str(plan.columns[1]), str(plan.columns[2]),
                                              str(plan.columns[3])],
                                     tablefmt="fancy_grid",
                                     showindex=False)
    # printing the plan in the table
    print(plan_tab(plan))


def search_word(
        args: argparse.Namespace,  # parser arguments
        plan: pd.DataFrame  # DataFrame where search -word-
) -> pd.DataFrame:  # DataFrame with only the notes with -word-

    # rewriting 'word' without capital letter
    word = vars(args)["word"].lower()

    # row indeces whose title contains word
    rows_idx = []

    # Converting plan to a list of lists to fasten the iteration through it
    list_plan = plan.values

    # Iterating through arr_plan
    for idx, row in enumerate(list_plan):

        # rewriting title and note without capital letters
        title = str(row[0]).lower()
        note = str(row[1]).lower()
        # checking if 'word' is either in title or note or both
        if word in title or word in note:
            rows_idx.append(idx)

    # selecting only those rows whose titles or notes contain 'word'
    selected_plan = plan.iloc[rows_idx, :]
    return selected_plan


def search_by_tag(
        args: argparse.Namespace,  # parser arguments
        plan: pd.DataFrame  # DataFrame where search the tags
) -> pd.DataFrame:  # DataFrame with only the notes with the correct tags

    """
    Parameters
    ----------
    plan: pd.DataFrame. Contains all the notes
    args: parse.parse_args(). Contains the tags to be searched and/or rejected, tags must be only in a string,
                              both commas or spaces can be used as separators

    Returns
    -------
    selected_plan : pd.DataFrame. Contains all the notes with the searched tags

    Notes
    ----
    The function return a pd.DataFrame with all the notes that contains the -tags- and/or do not contain the -notags-
    """

    # creating two list with the -tags- and -notags-
    tag_to_search = args.tags
    no_tags = args.notag
    # convert from str format to list format, it accepts both commas or spaces as separators
    tag_to_search = tag_to_search.split(sep=",") if "," in tag_to_search else tag_to_search.split()
    no_tags = no_tags.split(sep=",") if "," in no_tags else no_tags.split()

    #  row indexes to be used for the returned DataFrame
    rows_idx = []

    # Converting plan["tags"] to a list of lists to fasten the iteration through it
    list_plan = plan["tags"].values

    # tags searching and notags rejecting
    for idx, tags in enumerate(list_plan):
        list_plan[idx] = literal_eval(tags)
        if \
                all(item in list_plan[idx] for item in tag_to_search) and \
                list(np.intersect1d(no_tags, list_plan[idx])) == []:

            rows_idx.append(idx)

    # creating the plan to be returned
    selected_plan = plan.iloc[rows_idx, :]

    return selected_plan


def main():
    # parser initialization
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='possible actions', dest='subparser')

    # plan initialization
    plan = init_data()

    # INSERT argument
    insert_parser = subparsers.add_parser('insert', help='Insert a new item into the planner')
    insert_parser.add_argument("-v", "--verbose",
                               help="Increase output verbosity", action="store_true")

    # Title
    insert_parser.add_argument(str(plan.columns[0]),
                               help='Title of the note', type=str, nargs='?', default="...")
    # Body of the note
    insert_parser.add_argument(str(plan.columns[1]),
                               help='Body of the note', type=str, nargs='?', default="...")
    # Date
    insert_parser.add_argument(str(plan.columns[2]),
                               help='Date of the note', type=str, nargs='?',
                               default=datetime.today().strftime('%Y-%m-%d'))
    # Tags
    insert_parser.add_argument("tags",
                               help="Tags of the note", nargs='*', default=str(["generic"]))

    # PRINT argument
    subparsers.add_parser('print', help='Print out all the notes')

    # SEARCH argument
    search_parser = subparsers.add_parser('search', help='Find and print the notes that contain -word-')
    search_parser.add_argument('word',
                               help='word to be searched in the body and the title of the notes',
                               type=str, nargs='?')

    # SEARCH_TAG argument
    search_tab_parser = subparsers.add_parser('search_tag',
                                              help='Find and print the notes that contain -tag- or -tags-')
    search_tab_parser.add_argument("-nt", "--notags",
                                   help="no tag to search", action="store_true")
    search_tab_parser.add_argument('tags',
                                   help='tag/tags to be searched in the notes',
                                   type=str, nargs='?', default=' ')
    search_tab_parser.add_argument('notag',
                                   help='tags to be excluded',
                                   type=str, nargs='?', default=' ')

    # SORT argument
    sort_parser = subparsers.add_parser('sort', help='Sort the notes by date')
    sort_parser.add_argument("sort", help='sort the notes by date', type=str,
                             nargs='?')

    # arguments are converted into a argparser.Namespace object
    args = parser.parse_args()

    # MAIN IF STATEMENTS
    # insert
    if args.subparser == 'insert':
        if args.verbose:
            add_note_verbose(plan)
        else:
            add_note(args, plan)

    # print
    elif args.subparser == 'print':
        print_planner(plan)

    # search for words
    elif args.subparser == 'search':
        selected_plan = search_word(args, plan)
        print_planner(selected_plan)

    # search/reject for tags
    elif args.subparser == 'search_tag':
        # this condition is necessary when there are no -tags- but only -notags-
        if args.notags:
            args.notag, args.tags = args.tags, ' '
        selected_plan = search_by_tag(args, plan)
        print_planner(selected_plan)

    # sort by date
    elif args.subparser == 'sort':
        sorted_plan = sort_by_date(plan)
        print_planner(sorted_plan)


if __name__ == '__main__':
    main()
