from module import *


def main():
    # parser initialization
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help='possible actions', dest='subparser')

    # plan initialization
    plan = init_data()

    # INSERT argument
    insert_parser = subparsers.add_parser(
        'insert', help='Insert a new item into the planner')
    insert_parser.add_argument("-v", "--verbose",
                               help="Increase output verbosity", action="store_true")

    # Title
    insert_parser.add_argument(str(plan.columns[0]),
                               help='Title of the note', type=str, nargs='?', default="...")
    # Body of the note
    insert_parser.add_argument(str(plan.columns[1]),
                               help='Body of the note', type=str, nargs='?', default="...")
    # Date
    insert_parser.add_argument(str(plan.columns[2]),
                               help='Date of the note', type=str, nargs='?',
                               default=datetime.today().strftime('%Y-%m-%d'))
    # Tags
    insert_parser.add_argument("tags",
                               help="Tags of the note", nargs='*', default=str(["generic"]))

    # PRINT argument
    subparsers.add_parser('print', help='Print out all the notes')

    # SEARCH argument
    search_parser = subparsers.add_parser(
        'search', help='Find and print the notes that contain -word-')
    search_parser.add_argument('word',
                               help='word to be searched in the body and the title of the notes',
                               type=str, nargs='?')

    # SEARCH_TAG argument
    search_tab_parser = subparsers.add_parser('search_tag',
                                              help='Find and print the notes that contain -tag- or -tags-')
    search_tab_parser.add_argument("-nt", "--notags",
                                   help="no tag to search", action="store_true")
    search_tab_parser.add_argument('tags',
                                   help='tag/tags to be searched in the notes',
                                   type=str, nargs='?', default=' ')
    search_tab_parser.add_argument('notag',
                                   help='tags to be excluded',
                                   type=str, nargs='?', default=' ')

    # arguments are converted into an argparser.Namespace object
    args = parser.parse_args()

    # MAIN IF STATEMENTS
    # insert
    if args.subparser == 'insert':
        if args.verbose:
            add_note_verbose(plan)
        else:
            add_note(args, plan)

    # print
    elif args.subparser == 'print':
        print_planner(plan)

    # search for words
    elif args.subparser == 'search':
        selected_plan = search_word(args, plan)
        print_planner(selected_plan)

    # search/reject for tags
    elif args.subparser == 'search_tag':
        # this condition is necessary when there are no -tags- but only -notags-
        if args.notags:
            args.notag, args.tags = args.tags, ' '
        selected_plan = search_by_tag(args, plan)
        print_planner(selected_plan)


if __name__ == '__main__':
    main()
