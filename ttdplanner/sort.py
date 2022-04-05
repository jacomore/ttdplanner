import pandas as pd


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
