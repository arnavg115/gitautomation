import argparse
import os
try:
    from github import Github
    from os import name, path
    import os
    import json
    import base64
    import bcrypt
    import getpass
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except Exception:
    print("Ignore this comment if you do not wish to use github integration")
def getkey(password,salt):
  kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend= default_backend())
  key = base64.urlsafe_b64encode(kdf.derive(password))
  return key
def github():
    if path.exists("user.json"):
        with open("user.json","r") as json_file:
            data = json.load(json_file)
        salt = data["usrsalt"].encode("latin-1")
        p = getpass.getpass("Enter your password: ").encode()
        if bcrypt.checkpw(p,data["ps"].encode()):
            key = getkey(p,salt)
            d = Fernet(key)
            usrnm = d.decrypt(data["gusr"].encode()).decode()
            apik = d.decrypt(data["gapi"].encode()).decode()
            try:
                global g
                g = Github(usrnm,apik)
            except Exception:
                print("uh oh there has been an error. Delete user.json and try again")
    else:
        p = getpass.getpass("Enter a password to keep your data safe: ")
        usrdict = {}
        salt = os.urandom(16)
        usrdict["usrsalt"] = salt.decode("latin-1")
        key = getkey(p.encode(),salt)
        encryptor = Fernet(key)
        h = input("Github Username: ")
        apit = input("GitHub Api Token: ")
        eg = encryptor.encrypt(h.encode())
        dh = encryptor.encrypt(apit.encode())
        usrdict["gusr"] = eg.decode()
        usrdict["gapi"] = dh.decode()
        hashed = bcrypt.hashpw(p.encode(),bcrypt.gensalt())
        usrdict["ps"] = hashed.decode()
        with open("user.json","w") as jsonfile:
            json.dump(usrdict,jsonfile)
        github()

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")
parser = argparse.ArgumentParser()

parser.add_argument("-oc", "--onelinecommit", help="Commit and add everything in one line",default=None)
parser.add_argument("-v","--usevim",help="Open a file in vim and then add it to a git repo with one line",default=None)
parser.add_argument("-n","--usenano",help="Open a file in nano and then add it to a git repo with one line",default=None)
parser.add_argument("-ar","--addremoteandpush",help="Add a remote and push to it immediately",default=False)
parser.add_argument("-mp","--makerepo",help="Makes a repo and adds all files.",default=False)
parser.add_argument("-mpg","--makerepoandgithub",help="Makes a repo and adds all files. Then it makes a github repo with the given name",default=None)
parser.add_argument("-pr","--pushtoremote",help="Push to a remote of your choosing",default=None)
parser.add_argument("-pg","--pushtogithub",help="Commits everything and pushes it to your github repo",default=None)
parser.add_argument("-br","--branch",help="Checks out the branch and then uses it for its pushes",default="master")
parser.add_argument("-brc","--branchandcommit",help="makes a branch like -br but it also commits.",default=None)
parser.add_argument("-mkp","--makeaproject",help="makes a project",default=None)
args = parser.parse_args()
def checkgitrepo():
    return os.path.exists(".git")
def oneline(message):
    if checkgitrepo():
        os.system("git add .")
    else:
        os.system("git init")
        os.system("git add .")
    os.system('git commit -m "{}" '.format(message))
def vim(filename):
    os.system("vim -c':syntax on' -c ':set number' {}".format(filename))
    if checkgitrepo():
        os.system("git add {}".format(filename))
    else:
        os.system("git init")
        os.system("git add {}".format(filename))
def nano(filename):
    os.system("nano {}".format(filename))
    if checkgitrepo():
        os.system("git add {}".format(filename))
    else:
        os.system("git init")
        os.system("git add {}".format(filename))
def makerepoandgithub(reponame):
    if checkgitrepo():
        os.system("git add .")
    else:
        os.system("git init")
        os.system("git add .")
    github()
    user = g.get_user()
    repo = user.create_repo(reponame)
    os.system("git remote add gh {}".format(repo.clone_url))
def pr(ren,branch):
    os.system("git push {} {}".format(ren,branch))
def ptg(message,branch):
    os.system("git add .")
    os.system("git commit -m'{}'".format(message))
    os.system("git push gh {}".format(branch))
def checkbr(branchn):
    os.system("git checkout -b {}".format(branchn))
    os.system("git add .")
def checkbrc(branchn):
    os.system("git checkout -b {}".format(branchn))
    os.system("git add .")
    os.system("git commit -m'default commit'")
def makeaproj(name):
    os.system("mkdir {}".format(name))
    os.system("cp gitauto {}/gitauto".format(name))
    os.system("cp scripts.py {}/scripts.py".format(name))
    os.system("cd {}".format(name))
    os.system("git init")
    os.system("cd ..")
if args.makeaproject!= None:
    makeaproj(args.makeaproject)
if args.branch != "master":
    checkbr(args.branch)
if args.branchandcommit != None:
    checkbrc(args.branchandcommit)
if args.usevim != None:
    vim(args.usevim)
if args.usenano != None:
    nano(args.usenano)
if args.onelinecommit != None:
    oneline(args.onelinecommit)
if args.makerepoandgithub != None:
    makerepoandgithub(args.makerepoandgithub)
if args.pushtogithub!=None:
    if args.branchandcommit != None:   
        ptg(args.pushtogithub,args.branchandcommit)
    else:
        ptg(args.pushtogithub,args.branch)