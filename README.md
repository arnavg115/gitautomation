# Git Automation
A python CLI making git easy and more convenient.  This is an easy way to simplify git and what would have taken many lines now takes only one. 

---
## Requirements
- Linux/ unix
- Python*
- Git*
- Github Account
***requiered**
## Getting Started
Clone the Repo
```
$ git clone https://github.com/arnavg115/gitautomation.git
```
Open the folder and put the files into a projects folder or your desktop. (not needed but really helps) Now once you are done with that cd into the directory where the files are.
For Linux/Unix/ MacOS you can use the shell script to run commands. This is less tedious and is much more seamless. To use the script simply grant privelages to the file. You may have to do the same in each project folder.
```
chmod +x gitauto
```
Create a new project
Linux/Unix/ MacOS
```
$ gitauto -mkp <enter projectname>
```
Windows
```
python scripts.py -mkp <enter projectname>
```
In both substitute your project name for `<enter projectname>`
This should make a new folder with that name and put in two files the gitauto and scripts.py. Now you can make a file by
Linux/Unix/MacOS
```
$ gitauto -n <filename>
#or
$ gitauto -v <filename>
```
Note: I do not know how this would work on windows as I haven't tested it.
the -n stands for nano and -v is for vim. What this does it opens/ makes that file and opens up nano/vim. Then once you finish editing it adds it to your repo.
If you do not wish to use either then once you are finished editing in your editor of choice you can use the oneline commit functionality. 
Linux/Unix/MacOS
```
$ gitauto -oc <message>
```
Windows
```
python scripts.py -oc <message>
```
This will add all your files and commit this to your repo with the message as usual in one line.
## GitHub Integration
To use github you will need some python packages.
```
pip install bcyrpt
pip install cryptography
pip install PyGithub
```
Once installed you can use GitHub features.
To make a repo from one line in both github and locally just type
linux/Unix/MacOS
```
gitauto -mpg <reponame>
```
Windows
```
python scripts.py -mpg <reponame>
```
Now to push to github all in one line
Linux/Unix/MacOS
```
gitauto -pg <message>
```
Just like the other one line commit this adds, commits and pushes in one line.:
