# Copyright (c) 2024, espehon
# License: https://www.gnu.org/licenses/gpl-3.0.html


import os
import sys
import argparse
import json
import importlib.metadata

import copykitten


try:
    __version__ = f"fetchy {importlib.metadata.version('fetchy_cli')} from fetchy_cli"
except importlib.metadata.PackageNotFoundError:
    __version__ = "Package not installed..."

# Set file paths
storage_folder = os.path.expanduser("~/.share/fetchy/")
storage_file = "fetchy.json"
storage_path = storage_folder + storage_file


# Check if storage folder exists, create it if missing.
if os.path.exists(os.path.expanduser(storage_folder)) == False:
    os.makedirs(storage_folder)

# Check if storage file exists, create it if missing.
if os.path.exists(storage_path) == False:
    with open(storage_path, 'w', encoding='utf-8') as file:
        json.dump({}, file)

# read storage file
try:
    with open(storage_path, 'r') as file:
        data = json.load(file)
except ValueError:
    print(f"Error reading {storage_path}! Try deleting the file :(")
    sys.exit(1)

# Set argument parsing
parser = argparse.ArgumentParser(
    description="Fetchy: Fetch strings from your system rather than your own memory!",
    epilog="Example:\n> fet -n pi 3.14159265359\n> fet pi\n3.14159265359\n\nHomepage: https://github.com/espehon/fetchy-cli",
    allow_abbrev=False,
    add_help=False,
    usage="fet [Name] [-n Name Value] [-c Name] [-d Name1 ...] [-r OldName NewName] [-l] [-?] ",
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument('-?', '--help', action='help', help='Show this help message and exit.')
parser.add_argument('-v', '--version', action='version', version=__version__, help="Show package version and exit.")
parser.add_argument('-c', '--copy', nargs=1, metavar='N', action='store', type=str, help='Copy the value of [N] to the clipboard.')
parser.add_argument('-l', '--list', action='store_true', help='List saved variable names.')
parser.add_argument('-n', '--new', nargs=2, type=str, metavar=('N', 'V'), action='store', help='Create [N] with the value of [V]. (Overwrite existing)')
parser.add_argument('-d', '--delete', nargs='+', metavar=('N1', 'N2'), action='store', type=str, help='Delete [N1] etc.')
parser.add_argument('-r', '--rename', nargs=2, type=str, metavar=('O', 'N'), action='store', help='Rename [O] to [N].')
parser.add_argument("name", nargs='?', help="Name of entry to fetch.")


def sort_dict(dictionary) -> dict:
    sorted_dict = dict(sorted(dictionary.items()))
    return sorted_dict


def save_data(dictionary, file_path):
    with open(file_path, 'w') as file:
        json.dump(sort_dict(dictionary), file)


def overwrite_note(dictionary, note_name, note_value):
    if note_name in dictionary:
        user = str.lower(input(f"{note_name} already exists; do you want to overwrite it? (N/y): "))
        if user[0] == 'y':
            dictionary[note_name] = note_value
            save_data(data, storage_path)
            print("Note has been overwritten.")
        else:
            print("No changes were made.")
    else:
        print(f"Error: {note_name} does not exist!")


def new_note(dictionary, note_name, note_value):
    if note_name in dictionary:
        overwrite_note(dictionary, note_name, note_value)
    else:
        dictionary[note_name] = note_value
        save_data(data, storage_path)
        print("Note created.")


def delete_notes(dictionary, note_name_list: list):
    items_deleted = 0
    for note_name in note_name_list:
        if note_name in dictionary:
            dictionary.pop(note_name)
            items_deleted += 1
            print(F"{note_name} marked for removal.")
        else:
            print(f"{note_name} is not an entry.")
    if items_deleted > 0:
        save_data(dictionary, storage_path)
        print(f"{items_deleted} entries deleted.")
    else:
        print("No changes were made.")


def rename_note(dictionary, old_name, new_name):
    if old_name in dictionary:
        dictionary[new_name] = dictionary[old_name]
        dictionary.pop(old_name)
        save_data(dictionary, storage_path)
        print("Entry renamed.")
    else:
        print(f"{old_name} is not an entry.")


def list_items(dictionary):
    print(f"{len(dictionary)} entries:")
    for key in dictionary:
        print("\t" + key)


def copy_to_clipboard(dictionary, note_name):
    if note_name in dictionary:
        copykitten.copy(dictionary[note_name])
    else:
        print(f"No item matched {note_name}")


def fetch(dictionary, note_name):
    try:
        print(dictionary[note_name])
    except ValueError:
        print(f"No item matched {note_name}")


def cli(argv=None):
    args = parser.parse_args(argv) #Execute parse_args()
    if len(sys.argv) == 1:
        parser.print_usage()
    elif args.new:
        new_note(data, args.new[0], args.new[1])
    elif args.list:
        list_items(data)
    elif args.copy:
        copy_to_clipboard(data, args.copy[0])
    elif args.rename:
        rename_note(data, args.rename[0], args.rename[1])    
    elif args.delete:
        delete_notes(data, args.delete)
    elif args.name:
        print(f"{args.name}:\n{data[args.name]}")

    
