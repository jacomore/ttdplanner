import argparse
import pandas as pd
from ast import literal_eval
import numpy as np


def search_word(
        args: argparse.Namespace,  # parser arguments
        plan: pd.DataFrame  # DataFrame where search -word-
) -> pd.DataFrame:  # DataFrame with only the notes with -word-

    # rewriting 'word' without capital letter
    word = vars(args)["word"].lower()

    # row indexes whose title contains word
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
