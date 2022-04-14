from Planner import Planner
import argparse
from datetime import datetime
from module_obj import *


def main():
    # parser initialization
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help='possible actions', dest='subparser')

    # plan initialization
    plan = Planner()

    # fill the plan
    init_plan(plan)

    # DATA TO PATH
    _, data_path = data_to_path()

    # INSERT argument
    insert_parser = subparsers.add_parser(
        'insert', help='Insert a new item into the planner')
    insert_parser.add_argument("-v", "--verbose",
                               help="Increase output verbosity", action="store_true")

    # Title
    insert_parser.add_argument("title",
                               help='Title of the note', type=str, nargs='?', default="...")
    # Body of the note
    insert_parser.add_argument("body",
                               help='Body of the note', type=str, nargs='?', default="...")
    # Date
    insert_parser.add_argument("date",
                               help='Date of the note', type=str, nargs='?',
                               default=datetime.today().strftime('%Y-%m-%d'))
    # Tags
    insert_parser.add_argument("tags",
                               help="Tags of the note", nargs='?', default="generic")

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

    # DELETE_NOTE argument
    delete_note_parser = subparsers.add_parser('delete_tag',
                                              help='delete a note by its id')
    delete_note_parser.add_argument('id',
                                   help='id of the note to be deleted',
                                   type=str, nargs='+', default='-1')

    # arguments are converted into an argparser.Namespace object
    args = parser.parse_args()

    # MAIN IF STATEMENTS
    # insert
    if args.subparser == 'insert':
        if args.verbose:
            plan.add_note_verbose()
        else:
            plan.add_note(args.title, args.body, args.date, split_tags(args.tags))
        plan.save(data_path)

    # print
    elif args.subparser == 'print':
        plan.print_plan()

    # search for words
    elif args.subparser == 'search':
        # selected_plan = search_word(args, plan)
        # print_planner(selected_plan)
        pass

    # search/reject for tags
    elif args.subparser == 'search_tag':
        # this condition is necessary when there are no -tags- but only -notags-
        if args.notags:
            args.notag, args.tags = args.tags, ' '
        plan_by_tag = plan.search_tag(args.tags, args.notag)
        plan_by_tag.print_plan()

    elif args.subparser == 'delete_tag':
        for note_id in args.id:
            if isinstance(plan.note_by_id(note_id), int):
                del plan.list_of_notes[plan.note_by_id(note_id)]
            else:
                print(note_id, " not found")
        plan.save(data_path)


if __name__ == '__main__':
    main()
