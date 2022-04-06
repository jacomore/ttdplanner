import os
import pandas as pd


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
