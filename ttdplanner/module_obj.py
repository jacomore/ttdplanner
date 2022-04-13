import os
import json

from Planner import Planner


def data_path():
    """
    path to data.pkl
    """
    loc_dir = os.path.abspath(os.getcwd())
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))
    return os.path.abspath(os.path.join(dir_path, "data.json"))


def split_tags(tags):
    """
    split tags
    """
    return tags.split(sep=",") if "," in tags else tags.split(sep=" ")


def save_void_plan(path):
    """
    this function create a file.pkl in path with a void plan inside and return a void plan
    """
    void_plan = Planner()
    void_plan.save(path)
    return void_plan


def save_plan(plan, path):
    """11
    this function saves plan in file.json in path
    """
    with open(path, 'w') as outfile:
        json.dump(plan, outfile, default=lambda o: o.__dict__, indent=0)


def read_plan(path):
    """
    this function read a plan from a file.json in path
    """
    with open(path, 'rb') as json_file:
        plan = json.load(json_file)

    # plan creation
    input_plan = Planner()
    for note in plan["list_of_notes"]:
        input_plan.add_note(note["title"], note["body"], note["date"], note["tags"])
    return input_plan


def init_plan():
    # paths to dir
    loc_dir = os.path.abspath(os.getcwd())
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))

    # If the folder does not exist yet
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        plan = save_void_plan(data_path())
    # If the folder already exists
    else:
        # If "data.pkl" does not exist yet
        if not os.path.exists(data_path()):
            plan = save_void_plan(data_path())
        # If "data.pkl" already exists
        else:
            plan = read_plan(data_path())

    # returning plan
    return plan
