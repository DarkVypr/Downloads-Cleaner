import os
import configparser
import re
import json
import time
import humanize
import pathlib
from termcolor import cprint, colored

# Parse the INI file.
config = configparser.ConfigParser()
config.read("./settings.ini")

# Get patterns from patterns file.
with open("./patterns.json", encoding="UTF-8") as patterns:
    patterns = json.load(patterns)

# Clear screen function.
clearscreen = (
    lambda userOS=os.name: os.system("cls") if userOS == "nt" else os.system("clear")
)
clearscreen()

# Check if the user provided a downloads folder location.
folderLocation = config["Locations"]["DownloadsFolder"]
if not folderLocation or not os.path.isdir(folderLocation):
    exit(
        colored(
            "Please put the location of your downloads folder in the settings.ini, and ensure that it is the correct directory without quotes.",
            "red",
            attrs=["bold", "underline"],
        )
    )

# Get the downloads folders contents.
def downloadsFolder():
    downloads = pathlib.Path(folderLocation)
    return [str(i) for i in list(downloads.iterdir())]


# Remove all of the files.
def removeFiles(files: list):
    for i in files:
        if i["excluded"]:
            continue
        os.remove(i["fullPath"])


# Compile all of the RegExp's.
def compileAll(patternList: list):
    compiled = [re.compile(i, re.I) for i in patternList]
    return compiled


# For each compiled RegExp, get all of the matching files in the directory, and then append them to a master list.
def getMatchingFiles(patterns: list, downloads: list):
    files = []
    for i in patterns:
        matched = list(filter(i.match, downloads))
        [files.append(j) for j in matched]
    return files


# Format all of the files.
def formatFiles(files: list):
    counter = 0
    formatted = []
    for i in files:
        counter += 1
        fileName = i.split("\\")
        formatted.append(
            {
                "index": counter,
                "path": "/".join(fileName[0:-1]),
                "file": fileName[-1],
                "fullPath": i,
                "excluded": False,
            }
        )
    return formatted


# View all of the files.
def viewFiles(files: list):
    for i in files:
        print(
            f"Index: {i['index']} --> File: {i['file']} --> Path: {i['path']} {colored('[EXCLUDED]', 'red', attrs=['bold']) if i['excluded'] else ''}"
        )


# Excluding files function.
def excludeFiles(files: list, exclusions: list):
    for i in files:
        if i["index"] in exclusions:
            i["excluded"] = True


def getAllFileSizes(files: list):
    totalBytes = 0
    for i in files:
        if i["excluded"]:
            continue
        fileSize = pathlib.Path(i["fullPath"]).stat().st_size
        totalBytes += fileSize
    return totalBytes


# Call the function to search the downloads folder.
downloads = downloadsFolder()

# If there is nothing in the downloads folder, exit.
if not downloads:
    cprint(
        "There are no files in your downloads folder!",
        "red",
        attrs=["bold", "underline"],
    )
    exit(1)

# If there is nothing in the patterns file, exit.
if not patterns:
    cprint(
        "There are no patterns in the patterns.json file! Add some RegExp's and try again.",
        "red",
        attrs=["bold", "underline"],
    )
    exit(1)

# Call the function to compile all of the RegExp's.
compiled = compileAll(patterns)

# Call the function to get all of the files, then format them.
files = getMatchingFiles(compiled, downloads)


# Check if there were any found files.
if not files:
    cprint(
        "No files were found with the RegExp patterns provided.",
        "red",
        attrs=["bold", "underline"],
    )
    exit(0)

files = formatFiles(files)

totalFileSizes = humanize.naturalsize(getAllFileSizes(files))

if config["UserInput"]["AlwaysAskBeforeDeleting"] == "false":
    clearscreen()
    removeFiles(files)
    exit(
        colored(
            f"Successfully deleted {totalFileSizes} of files!",
            "green",
            attrs=["bold", "underline"],
        )
    )

excluded = []
while True:
    clearscreen()

    totalFileSizes = humanize.naturalsize(getAllFileSizes(files))

    # Print # of files found.
    cprint(
        f"Found {len(files)} files. ({totalFileSizes} Total Of Non-Excluded Files)",
        "green",
        attrs=["bold"],
    )
    print("\n----------\n")

    viewFiles(files)
    print("\n----------\n")
    choice = input(
        colored(
            "What would you like to do with the files? (Enter A Number)\n\n1. Cancel\n2. Exclude Files From Deletion\n3. Remove All Non-Excluded Files\n\n> ",
            attrs=["bold"],
        )
    )

    if choice not in "123":
        clearscreen()
        cprint(
            f'"{choice}" was not a valid option! Please pick from 1-4. (Try Again In 4 Seconds)',
            "yellow",
            attrs=["bold", "underline"],
        )
        time.sleep(4)
        clearscreen()
        continue

    if choice == "1":
        exit("Exited With No Error. (Cancelled By User)")
    elif choice == "2":
        clearscreen()
        viewFiles(files)
        print()
        exclusions = input(
            colored(
                'What files would you like to exclude? (Enter Their Index, Comma-Separated For Multiple, Eg: "1,4,245")\n\n> ',
                attrs=["bold"],
            )
        )
        exclusions = exclusions.split(",")
        try:
            exclusions = [int(i) for i in exclusions]
        except:
            cprint(
                "There was an error converting on of the indexes you provided into an interger... (Try again in 3 seconds)",
                "red",
                attrs=["bold", "underline"],
            )
            time.sleep(3)
            clearscreen()
            continue
        excludeFiles(files, exclusions)
        excluded += exclusions
        clearscreen()
    elif choice == "3":
        clearscreen()
        removeFiles(files)
        exit(
            colored(
                f"Successfully deleted {totalFileSizes} of files!",
                "green",
                attrs=["bold", "underline"],
            )
        )
    else:
        exit("Error Getting Choice.")
