import os
from Planner import Planner


def data_to_path():
#) -> tuple[str, str]:  # [path to the directory, path to the .json file]
    """
    Returns
    -------
    dir_path: path. Path to the directory where is present the .json file
    data_path: path. Path to the .json file where the Planner is stored

    Note
    ----
    When is necessary to change the location of the .json file, only this function must be changed
    """

    loc_dir = os.path.abspath(os.getcwd())
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))  # directory path
    data_path = os.path.abspath(os.path.join(dir_path, "data.json"))  # .json file path
    return dir_path, data_path


def init_plan(
        plan: Planner  # initial Planner to be initialized
):
    """
    Parameters
    ----------
    plan: ttdplanner.Planner.Planner. Initial planner to be initialized

    Note
    ----
    The plan will be initialized by reading the path from the data_to_path() function.
    In order to change the path, that function must be modified.
    """

    # paths to dir and .json file
    dir_path, data_path = data_to_path()  # change data_to_path in order to change the path

    # If the folder does not exist yet
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        plan.save(data_path)
    # If the folder already exists
    else:
        # If "data.pkl" does not exist yet
        if not os.path.exists(data_path):
            plan.save(data_path)
        # If "data.pkl" already exists
        else:
            plan.read_plan(data_path)


def split_tags(
        tags: str  # string og tags separated by commas or spaces
) -> list:  # list of tags
    """
    Parameters
    ----------
    tags: str. String that contains all the tags separated by commas or spaces.

    Returns
    -------
    Type list. List of tags, created by separating the tags contained int the str "tags"

    Examples of usage
    -----------------
    Tags separated by spaces:
    -> split_tags("tag1 tag2 tag3")
    >> ["tag1", "tag2", "tag3"]

    tags separated by commas:
    -> split_tags("tag1,tag2, tag3")
    >> ["tag1", "tag2", " tag3"]

    Warnings
    --------
    When is present a comma in the input string the function will automatically separate the tags using commas.
    In that case any space will be computed as a character; this could cause issues.
    """

    return tags.split(sep=",") if "," in tags else tags.split(sep=" ")
