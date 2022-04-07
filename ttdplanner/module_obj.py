import pickle
import os

from Planner import Planner


def save_void_plan(path):
    """
    this function create a file.pkl in path with a void plan inside and return a void plan
    """
    with open(path, 'wb') as out:
        void_plan = Planner()
        pickle.dump(void_plan, out, pickle.HIGHEST_PROTOCOL)
    return void_plan


def save_plan(plan, path):
    """
    this function saves plan in file.pkl in path
    """
    with open(path, 'wb') as out:
        pickle.dump(plan, out, pickle.HIGHEST_PROTOCOL)


def read_plan(path):
    """
    this function read a plan from a file.pkl in path
    """
    with open(path, 'rb') as inp:
        return pickle.load(inp)


def init_plan():

    # paths to dir and data.pkl
    loc_dir = os.path.abspath(os.getcwd())
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))
    data_path = os.path.abspath(os.path.join(dir_path, "data.pkl"))

    # If the folder does not exist yet
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        plan = save_void_plan(data_path)
    # If the folder already exists
    else:
        # If "data.pkl" does not exist yet
        if not os.path.exists(data_path):
            plan = save_void_plan(data_path)
        # If "data.pkl" already exists
        else:
            plan = read_plan(data_path)

    # returning plan
    return plan
