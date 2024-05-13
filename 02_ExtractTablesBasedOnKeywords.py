__author__ = 'Ye Wang'


from Form10K import *
import os
import shutil
import re
from bs4 import BeautifulSoup
import csv
from pattern.web import URL, plaintext



def all_occurences(file, str):
    initial = 0
    while True:
        initial = file.find(str, initial)
        if initial == -1:
            return
        yield initial
        initial += len(str)


def ReadFile(f):
    from pattern.web import plaintext, strip_between
    import re

    with open(f) as datafile:
        lines =datafile.readlines()
        datafile.close()

        ### Remove the header
        lines = ' '.join(lines)
        lines = lines.replace("&#151;", "---")
        first = '</SEC-HEADER>'
        temp = lines.find(first)
        if temp == -1:
            item=1
        else:
            item = lines.index(first) + 14
        lines = lines[item:]

        ### Just keep the first document in 10-K
        last = '</DOCUMENT>'
        temp1 = list(all_occurences(lines,last))
        if len(temp1) != 0:
            if temp1 != []:
                item1 = temp1[0]
        else:
            item1 = len(lines)
        lines = lines[:item1]

        insensitive_hippo = re.compile(re.escape('table of contents'), re.IGNORECASE)
        lines = insensitive_hippo.sub(' ', lines)

    return lines


def Alpha(string):
    ret = 0
    for char in string:
        if char.isalpha():
            ret = 1
            break
    return ret


def TableHTML(file, savefile):
    ### Creat the soup ###
    page = ReadFile(file)
    soup = BeautifulSoup(page)
    tables = soup.find_all('table')
    text_file = open(savefile, "w")
    for table in tables:
        rc = 0
        for row in table.find_all('tr'):
            for cell in row.find_all('td'):
                for string in cell.strings:
                    s = str(repr(string).encode('ascii', 'ignore'))
                    temp = ''.join(s)
                    temp = str(temp).lower()
                    if ('restricted cash' in temp) and (len(temp) < 100):
                        rc = 1
        if rc == 1:
            text_file.write(str(table) + "\n\n\n")
            break
    text_file.close()
    return 1


def TableTXT(file, savefile):
    ### Creat the soup ###
    page = ReadFile(file)
    soup = BeautifulSoup(page)
    tables = soup.find_all('table')
    text_file = open(savefile, "w")
    for table in tables:
        rc = 0
        s = str(table)
        lines = s.split("\n")
        for line in lines:
            temp = str(line).lower()
            if 'restricted cash' in temp:
                rc = 1
        if rc == 1:
            text_file.write(str(table) + "\n\n\n")
            break
    text_file.close()
    return 1


path = "H:/Projects/RestrictedCash/"
path_data = "H:/SECfilings/10-K/Form10K/"
path_targetHTML = path + "10KtablesHTML/"
path_targetTXT = path + "10KtablesTXT/"

try:
    shutil.rmtree(path_targetHTML, ignore_errors=True)
except IOError:
    pass

try:
    shutil.rmtree(path_targetTXT, ignore_errors=True)
except IOError:
    pass


if not os.path.exists(path_targetHTML):
    os.makedirs(path_targetHTML)

if not os.path.exists(path_targetTXT):
    os.makedirs(path_targetTXT)




files = os.listdir(path_data)
os.chdir(path_data)

for file in files:
    print file
    try:
        if TypeHTML(file) == 1:
            f = path_data + file
            sf = path_targetHTML + file
            TableHTML(f, sf)
            if os.path.getsize(sf) == 0:
                os.remove(sf)

        else:
            f = path_data + file
            sf = path_targetTXT + file
            TableTXT(f, sf)
            if os.path.getsize(sf) == 0:
                os.remove(sf)
                
    except:
        pass
print "Done!"


