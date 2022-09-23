# Project Name
* ImportExport SQL - version 1.1.2.10

Project date: 09/2022


## Additional infromation
- Icon from: https://icon-icons.com/icon/file-archive/193973

- This project will save me a lot of time at work because I have a many cyclical operation on database with import and export excels.
- I wrote this program after my job, because it is an element of my self-development.
- If you find a bug you can write to me :)


## Table of Contents
* [General Info](#general-information)
* [Additional infromation](#additional-infromation)
* [General Information](#general-information)
* [Technologies Used](#technologies-used)
* [Usage](#usage)
* [Project Status](#project-status)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
The program has:
- Getting params from configuration file
- Securing password in configuration file
- Import data to database by Excel or SQL file
- Export data from database by table name or SQL file
- Sending SMS on the end script
- Sending E-Mail after error 


## Technologies Used
- Python - version 3.10.1
  - SMTPLib
  - UrlLib
  - gc
- Requests - verson 2.25.1
- SQLAlchemy - version 1.4.41
- PyODBC - version 4.0.31
- Pandas - version 1.2.3
- XLSXWriter - version 3.0.3
- ConfigParser - version 5.0.2
- ConfigUpdater - version 2.0
- PyInstaller - version 4.2

<!--
## Features
None


## Screenshots
![Example screenshot](./img/screenshot.png)


## Setup
What are the project requirements/dependencies? Where are they listed? A requirements.txt or a Pipfile.lock file perhaps? Where is it located?

Proceed to describe how to install / setup one's local environment / get started with the project.
-->

## Usage
If you would like to run from script:
1. Run main.py
2. Complete config.ini
3. Run main.py
4. Look at the log file

If u would like to run EXE (and then example put it into Task Scheduler, like me):

Generate EXE file - CMD ->
```batch
pip install pyinstaller --proxy http://user:pass@proxy.pl:3128
cd Building
pyinstaller ImportExportSQL.spec
```

1. Run .\dist\ImportExportSQL.exe
2. Complete config.ini
3. Run again ImportExportSQL.exe
4. Look at the log file


## Project Status
Project is: _in tested_

<!-- _complete_ / _no longer being worked on_ (and why) -->

<!--
## Room for Improvement
No plans
-->

## Contact
Created by [@Majster](mailto:rachuna.mikolaj@gmail.com)
