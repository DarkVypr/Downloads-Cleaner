# What is this?

This was a small project I made to clean up my downloads folder. Deleting everything manually is a pain in the ass and Python doesn't have feelings so this is much easier.

It uses RegExp's. All of the expressions are in the `patterns.json` file. The script compiles all of the strings into expressions, then prompts the user with some options on what they would like to do with all of the found files. The user also has the option to exclude some files from deletion.

# Before running

Before you run this script, make sure to add the location of your downloads folder into the `settings.ini` file. Also, there is other options in that file that may peak interest.

| Setting                   | Description |
| ------------------------- | ----------- |
| AlwaysAskBeforeDeleting   | This setting will toggle on/off the menu that pops up when deleting files. If you want to be asked about excluding and what to do with the files, toggle this off. This will allow for two-click operation of this script which is nice in a pinch.

# How to run.

This is pretty simple to run, all you have to do is launch `run.bat`. You can also just run it through the CLI of your choice.

# Adding file detections

If you want the script to detect additional files to be deleted, just add a RegExp to `patterns.json`.

# Excluding files

Excluding files is easy. Run the script, then when the user prompt pops up, pick the corresponding number. It will then ask you to provide a comma-separated list of files that you would like to preserve. It will alsp print **"[EXCLUDED]"** in red text next to the file when viewing.

When done excluding, just pick the **delete files** option.
