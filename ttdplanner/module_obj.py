import os


def data_to_path():
    loc_dir = os.path.abspath(os.getcwd())
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))
    data_path = os.path.abspath(os.path.join(dir_path, "data.json"))
    return dir_path, data_path


def init_plan(plan):
    # paths to dir
    dir_path, data_path = data_to_path()

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


def split_tags(tags):
    """
    split tags
    """
    return tags.split(sep=",") if "," in tags else tags.split(sep=" ")
