import argparse
import os
import pandas as pd
from datetime import datetime
from tabulate import tabulate

def init_data():
    features = ["title","note","date"]
    plan = pd.DataFrame(columns = features)

    loc_dir = os.path.abspath(os.getcwd())
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))
    data_path = os.path.abspath(os.path.join(dir_path,"data.csv"))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        plan.to_csv(data_path,index = False)
    else:
        if not os.path.exists(data_path):
            plan.to_csv(data_path,index = False)

        else:
            plan = pd.read_csv(data_path,index_col = False)
    return plan

def update_data(plan):
    loc_dir = os.path.abspath(os.getcwd())
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))
    data_path = os.path.abspath(os.path.join(dir_path,"data.csv"))
    plan.to_csv(data_path,index = False)
    return 

def add_note(args,plan):
    item = {}
    for name in plan.columns:
        item[str(name)] = vars(args)[str(name)]

    plan = plan.append(pd.DataFrame(item,index=[0]))    
    update_data(plan)
    
    return plan 

def print_planner(plan):
    plan_tab = lambda plan:tabulate(plan,
            headers = [str(plan.columns[0]),str(plan.columns[1]),str(plan.columns[2])],
            tablefmt="fancy_grid",
            showindex=False)
    print(plan_tab(plan))
    return
    

def search_and_print(args):
    pass

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='possible actions', dest='subparser')
    
    plan = init_data()

    insert_parser = subparsers.add_parser('insert', help = 'Insert a new item into the planner')
    insert_parser.add_argument(str(plan.columns[0]),
        help ='Title of the note', type=str,nargs='?', default = "...")
    insert_parser.add_argument(str(plan.columns[1]),
        help ='Body of the note', type=str,nargs='?' , default = "...")
    insert_parser.add_argument(str(plan.columns[2]),
        help ='Date of the note', type=str,nargs='?',default = datetime.today().strftime('%Y-%m-%d'))
   
    print_parser = subparsers.add_parser('print', help='Print out all the notes')    

    search_parser = subparsers.add_parser('search', help='Find and print the notes that contain -word-')
    search_parser.add_argument('word',
            help='word to be searched in planner and printed out',
            type=str)

    args = parser.parse_args()
    
    if args.subparser=='insert':
        plan = add_note(args,plan)
    if args.subparser=='print':
        print_planner(plan)
    if args.subparser=='search':
        search_and_print(args)


if __name__ == '__main__':
    main()


