import argparse
import os
import pandas as pd
from datetime import datetime
from tabulate import tabulate
import re
from ast import literal_eval

def init_data():
    features = ["title", "note", "date", "tags"]
    plan = pd.DataFrame(columns=features)

    loc_dir = os.path.abspath(os.getcwd())
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))
    data_path = os.path.abspath(os.path.join(dir_path, "data.csv"))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        plan.to_csv(data_path, index=False)
    else:
        if not os.path.exists(data_path):
            plan.to_csv(data_path, index=False)

        else:
            plan = pd.read_csv(data_path, index_col=False)
    return plan


def update_data(
        plan: pd.DataFrame):
    """
    Parameters
    ----------
    plan: pd.DataFrame. Contains all the notes
    
    Notes
    ----
    This function takes in input the updated version of plan and 
    overwrite the existing local copy in "Data/data.csv"
    """
    # finding the local dir
    loc_dir = os.path.abspath(os.getcwd())

    # moving to the parent dir
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))
    
    # path of the file "data.csv"
    data_path = os.path.abspath(os.path.join(dir_path, "data.csv"))
    
    # overwriting data
    plan.to_csv(data_path, index=False)
    return


def add_note(
        args: argparse.Namespace,  # parser arguments
        plan: pd.DataFrame  # DataFrame to be updated
        ) -> pd.DataFrame:
    """
    Parameters
    ----------
    args: argparse.Namespace. Contains the arguments "title", "note" and "date"
    plan: pd.DataFrame. Contains all the notes

    Returns
    -------
    plan: pd.DataFrame with the added note

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

    return plan  # questo credo che vada eliminato


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

    "title"
    title = input("Please, insert the title: ")
    item["title"] = title

    "body"
    note = input("It's time to write your note: ")
    item["note"] = note

    "date"
    date = input("Insert the date 'Y-m-d'. Press Enter to use the current date: ")
    if date == '':  # insert the current data if requested
        date = datetime.today().strftime('%Y-%m-%d')
    item["date"] = date

    "tags"
    tags = input("Insert the tags (separated by a space or a comma): ")
    #  these three lines insert a list in the pd.DataFrame. ATTENTION: it is stored as a string
    #  they are needed because pd.DataFrame can't be initialized with nested data
    item["tags"] = "..."
    data_bug = pd.DataFrame(item, index=[0])
    data_bug.at[0, "tags"] = re.sub("[^\w]", " ",  tags).split()  # use literal_eval('[1.23, 2.34]') to read this data

    "updating the plan"
    plan = plan.append(data_bug)
    update_data(plan)

def print_planner(
        plan: pd.DataFrame):
    """
    Parameters
    ----------
    plan: pd.DataFrame. Contains all the notes
    
    Notes
    ----
    The function prints in the terminal all the notes 
    """

    #  convert the tags in a readable format
    for i in range(plan.shape[0]):
        plan.at[i,"tags"] = ', '.join(literal_eval(plan.at[i,"tags"]))

    plan_tab = lambda plan: tabulate(plan,
                                     headers=[str(plan.columns[0]), str(plan.columns[1]), str(plan.columns[2]), str(plan.columns[3])],
                                     tablefmt="fancy_grid",
                                     showindex=False)
    print(plan_tab(plan))

def search_and_print(args):
    pass


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='possible actions', dest='subparser')

    plan = init_data()

    # insert parser
    insert_parser = subparsers.add_parser('insert', help='Insert a new item into the planner')
    insert_parser.add_argument("-v", "--verbose",
                               help="Increase output verbosity", action="store_true")
    insert_parser.add_argument(str(plan.columns[0]),
                               help='Title of the note', type=str, nargs='?', default="...")
    insert_parser.add_argument(str(plan.columns[1]),
                               help='Body of the note', type=str, nargs='?', default="...")
    insert_parser.add_argument(str(plan.columns[2]),
                               help='Date of the note', type=str, nargs='?',
                               default=datetime.today().strftime('%Y-%m-%d'))
    insert_parser.add_argument("-t", "--tags",
                               help="Tags of the note", nargs='+', default=str(["generic"]))

    # print parser
    print_parser = subparsers.add_parser('print', help='Print out all the notes')

    # search parser
    search_parser = subparsers.add_parser('search', help='Find and print the notes that contain -word-')
    search_parser.add_argument('word',
                               help='word to be searched in planner and printed out',
                               type=str)

    args = parser.parse_args()

    if args.subparser == 'insert':
        if args.verbose:
            plan = add_note_verbose(plan)
        else:
            plan = add_note(args, plan)

    elif args.subparser == 'print':
        print_planner(plan)

    elif args.subparser == 'search':
        search_and_print(args)


if __name__ == '__main__':
    main()
