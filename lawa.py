#!/usr/bin/env python3

import sys
import re
import click
import pytz
from os.path import exists
from datetime import datetime
from pathlib import Path

CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0;0m'

posRegex = r'(\+[a-zA-Z]*)'
negRegex = r'(-[a-zA-Z]*)'
tagRegex = r'(~[a-zA-Z]*)'

args = sys.argv

dataFile = str(Path.home()) + "/.lawa"

if not exists(dataFile):
    with open(dataFile, 'w') as fp:
        pass

print('')
data = open(dataFile, "r").read().strip().split('\n')

# comment out this line to use system timezone, otherwise change
# it to your timezone if it's inaccurate
tz = pytz.timezone("America/Los_Angeles")

def getDate():
    return datetime.today().astimezone(tz).strftime('%Y-%m-%d')

def help():
    print('Usage: lawa [args]')
    print('')
    print('help                 Displays this help screen')
    print('about                Displays information about this program')
    print('all                  Display all posts')
    print('list                 Display a list of all posts')
    print('today                Display today\'s post')
    print('last                 Display the most recent post')
    print('view [YYYY-MM-DD]    Display the specified post')
    print('tagged [+,-,~][tag]  Display all posts with the specified tag')
    print('add                  Create or update today\'s post')
    print('edit [YYYY-MM-DD]    Edit the specified post')
    print('delete [YYYY-MM-DD]  Delete the specified post')

def about():
    print('Version:    1.0.1')
    print('Author:     0xdstn')
    print('Source:     https://github.com/0xdstn/lawa')
    print('More info:  https://tilde.town/~dustin/projects/lawa')

def getData(day):
    for x in data:
        if x.startswith(day):
            return x[11:]
    return ''

def displayAll():
    for x in data[::-1]:
        if len(x):
            display(x[0:11],x[11:])

def displayDates():
    for x in data[::-1]:
        if len(x):
            print(x[0:11] + ' ' + postStats(x[11:]))

def displayTagged(tag):
    color = ''
    if tag[0] == '+':
        color = GREEN
    elif tag[0] == '-':
        color = RED
    elif tag[0] == '~':
        color = CYAN

    if len(color):
        print('Posts tagged '+color+tag+RESET)
        for x in data:
            if tag.lower() in x.lower():
                display(x[0:11],x[11:])
    else:
        print('Please prepend tag with +, -, or ~')

def postStats(post):
        posWords = re.findall(posRegex,post)
        negWords = re.findall(negRegex,post)
        tagWords = re.findall(tagRegex,post)

        posCount = str(len(posWords))
        negCount = str(len(negWords))
        tagCount = str(len(tagWords))

        wordCount = str(len(post.replace('\\',' ').split(' ')))

        return '['+GREEN+'+'+posCount+' '+RED+'-'+negCount+' '+CYAN+'~'+tagCount+RESET+'] ('+wordCount+')'

def postTags(post):
        posWords = re.findall(posRegex,post)
        negWords = re.findall(negRegex,post)
        tagWords = re.findall(tagRegex,post)


        pos = ''
        neg = ''
        tag = ''
        for w in posWords:
            pos += w+' '
        for w in negWords:
            neg += w+' '
        for w in tagWords:
            tag += w+' '

        if len(pos) or len(neg) or len(tag):
            print('')
            print('---')
            print('')
        if len(pos):
            print(GREEN+pos+RESET)
        if len(neg):
            print(RED+neg+RESET)
        if len(tag):
            print(CYAN+tag+RESET)

def display(date,post):
    if len(post):

        print('')
        print('------------')
        print(' '+date)
        print('------------')
        print('')
        print(postStats(post))

        paragraphs = post.split('\\')
        for p in paragraphs:
            p = re.sub(negRegex,RED+r'\1'+RESET,p)
            p = re.sub(posRegex,GREEN+r'\1'+RESET,p)
            p = re.sub(tagRegex,CYAN+r'\1'+RESET,p)
            print('')
            print(p)

        postTags(post)
    else:
        print('Post not found for ' + date)

def add():
    d = getDate()
    cur = ""
    newPost = True
    for x in data:
        if x[0:10] == d:
            cur = x[11:].replace("\\","\n\n")
            newPost = False
    
    post = click.edit(cur)
    if post is not None:
        line = d + ' ' + post.strip().replace("\n\n","\\")
        updateData(d,line,newPost)
    else:
        print('No changes, nothing updated')

def edit(d):
    found = False
    cur = ""
    for x in data:
        if x.startswith(d):
            found = True 
            cur = x[11:].replace("\\","\n\n")
    if found:
        post = click.edit(cur)
        if post is not None:
            line = d + ' ' + post.strip().replace("\n\n","\\")
            updateData(d,line,False)
        else:
            print('No changes, nothing updated')
        
    else:
        print('Post not found for ' + d)


def delete(d):
    with open(dataFile, 'r+') as file:
        found = False
        content = file.read()
        newLines = []
        lines = content.strip().split("\n")
        for line in lines:
            if d not in line:
                newLines.append(line)
            else:
                found = True
        if found:
            content = "\n".join(newLines)
            file.seek(0)
            file.write(content)
            file.truncate()
            print('Deleted post for ' + d)
        else:
            print('Post not found for ' + d)

def updateData(d,line,newPost):
    with open(dataFile, 'r+') as file:
        content = file.read()
        if newPost:
            file.seek(0)
            file.write(line + "\n" + content)
            print('Added post for ' + d)
        else:
            lines = content.strip().split("\n")
            for i in range(len(lines)):
                if d in lines[i]:
                    lines[i] = line
            content = "\n".join(lines)
            file.seek(0)
            file.write(content)
            file.truncate()
            print('Updated post for ' + d)

if len(args) == 1:
    help()
elif args[1] == 'help':
    help()
elif args[1] == 'about':
    about()
elif args[1] == 'all':
    displayAll()
elif args[1] == 'list':
    displayDates()
elif args[1] == 'today':
    d = getDate()
    display(d,getData(d))
elif args[1] == 'last':
    d = data[0][0:11]
    display(d,getData(d))
elif args[1] == 'add':
    add()
elif len(args) == 3 and args[1] == 'edit':
    edit(args[2])
elif len(args) == 3 and args[1] == 'delete':
    delete(args[2])
elif len(args) == 3 and args[1] == 'view':
    display(args[2],getData(args[2]))
elif len(args) == 3 and args[1] == 'tagged':
    displayTagged(args[2])
else:
    print('Unrecognized command')
    help()
