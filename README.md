# What is this?

This was a small project I made to clean up my downloads folder. Deleting everything manually is a pain in the ass and Python doesn't have feelings so this is much easier.

It uses RegExp's. All of the expressions are in the `patterns.json` file. The script compiles all of the strings into expressions, then prompts the user with some options on what they would like to do with all of the found files. The user also has the option to exclude some files from deletion.

If you want the script to detect additional files to be deleted, just add a RegExp to `patterns.json`.

Excluding files is easy, then you run the script,
