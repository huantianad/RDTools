# RDTools
Cool RD stuff in python with fun GUI

## Features/To-Do
- [x] Bulk Downloader
- [ ] Auto Extract
- [ ] Auto New Level Downloader
- [ ] Auto Daily Blend

## Installation
1. Clone the repository: `git clone https://github.com/huantianad/RDTools`
2. Install pipenv with `pip install -U pipenv`
3. Install required packages: `pipenv install`

## Usage
To start the program, run `main.py`. Under the "Tools" menu, select the required tool. You can use `Control + Shift + H` to hide the program.

### Bulk Downloader
There are two modes for this: "Positional" and "Difference". The positional mode allows you to select what levels to download through a range. The difference mode downloads all the levels that are not in a selected saved list of levels. 
The options "rename", "overwrite", and "skip" allow you to choose what the program does when it encounters a file with the same name.

## PyInstaller
To freeze the program with pyinstaller, just run the build.bat file, and it will output in the dist folder.