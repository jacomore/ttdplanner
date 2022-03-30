import argparse

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='possible actions', dest='subparser')
    
    insert_parser = subparsers.add_parser('insert', help='Insert a new item into the planner')
    insert_parser.add_argument('note', help='Note to be saved', type=str)
    # optional argument
    # square_parser.add_argument("power", 
    #    help="power to raised at", 
    #    type=float,
    #    nargs='?', # this argument might be absent
    #    default=2, # the default value it takes if it absent
    #)
    
    print_parser = subparsers.add_parser('print', help='Print out all the notes')    

    search_parser = subparser.add_pasers('search', help='Find and print the notes that contain -word-')
    search_parser.add_argument('word',
            help='word to be searched in planner and printed out',
            type=str)

    args = parser.parse_args()
    
    if args.subparser=='insert':
        add_note(args)
    if args.subparser=='print':
        print_planner(args)
    if args.subparser=='search':
        search_and_print(args)
        
if __name__=='__main__':
    main()
    


