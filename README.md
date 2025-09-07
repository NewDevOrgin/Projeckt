# Projeckt!
Is a simple project management tool. It can create/setup and delete projects according to templates!.

# How does it work?
Projeckt reads a project template file `.prt` which is just a collection of bash commands e.g:
***EXAMPLE FOR A PYTHON PROJECT***
```bash
python -m venv .env
git init
touch App.py
```
---

All that does is create a new folder in your project directory then it will execute those commands in order. NB!! Make sure to have each command on a seperate LINE!!
After your project folder has been created it will make a new virtual enviroment, initialise git and create `App.py` ready for you to work on it <small>(acording to the template)</small>

# Using Projeckt!
***Create a conf.txt with the full path to a directory where all your projects will saved to!***

## Making a new project
Press the plus in the top left corner of the program a dialog box with two inputs will apear, first enter the name of your project then the template name **!!! Do not include .prt !!!** then press the check, *if no template is found only a folder will be created with a .projeckt file*. 

## Deleting a project
Press the delete button next to the plus button which will show another dialog box, simply enter the project name and press the check. **!!! This will delete any folder with the name you entered in your project directory and is irreversible !!!**

## Making a custom template
A template is just a collection of bash commands that will be executed from top to bottm, remember to press enter after each command! The commands will be executed in the newly created project folder.
