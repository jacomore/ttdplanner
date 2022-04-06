import pandas as pd
from tabulate import tabulate
from ast import literal_eval


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
                                     headers=[str(plan.columns[0]), str(plan.columns[1]),
                                              str(plan.columns[2]), str(plan.columns[3])
                                              ],
                                     tablefmt="fancy_grid",
                                     showindex=False)
    # printing the plan in the table
    print(plan_tab(plan))
