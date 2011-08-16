#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
from os import path, makedirs
from datetime import datetime

from journal import __version__

JOURNAL_ROOT = path.expanduser("~")
JOURNAL_DEST = path.join(JOURNAL_ROOT, ".journal")
JOURNAL_ENTRY_FORMAT = "%a %I:%M:%S %Y-%m-%d"
JOURNAL_FILE_FORMAT = "%Y.%m.%d"

def make_sure_dir_exists(some_dir):
    if not path.exists(some_dir):
        try:
            makedirs(some_dir)
        except:
            print "journal: error: creating", some_dir
            sys.exit()

def parse_args():
    parser = argparse.ArgumentParser(
            description='Simple CLI tool to help with keeping a work/personal journal',
            version=__version__)
    parser.add_argument('entry',
            action="store",
            help="Text to make an entry in your journal")
    return parser, parser.parse_args()

def check_journal_dest():
    make_sure_dir_exists(JOURNAL_DEST)

def build_journal_path(date):
    return path.join(JOURNAL_DEST, date.strftime(JOURNAL_FILE_FORMAT) + ".txt")

def record_entry(entry):
    check_journal_dest()
    current_date = datetime.today()
    update_date = current_date.strftime(JOURNAL_ENTRY_FORMAT)
    entry = update_date + "\n-" + entry + "\n\n"
    with open(build_journal_path(current_date), "a") as date_file:
        date_file.write(entry)

def show_entry(date):
    """
    returns entry text for given date or None if entry doesn't exist
    """
    try:
        with open(build_journal_path(date), "r") as entry_file:
            return entry_file.read()
    except IOError:
        return None

def show_today():
    return show_entry(datetime.today())

def main():
    parser, args = parse_args()

    if not str.strip(args.entry):
        parser.print_help()
        sys.exit()
    elif args.entry == 'today':
        entry = show_today()
        if entry:
            print entry
        else:
            print "journal: error: entry not found on that date"
            sys.exit()
    else:
        record_entry(args.entry)

if __name__ == "__main__":
    main()
