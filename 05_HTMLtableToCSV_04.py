__author__ = 'Ye Wang'




import os
import shutil
import re
from bs4 import BeautifulSoup
import csv
from pattern.web import URL, plaintext
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def ExtractTableHTML(file):
    ### Creat the soup ###
    with open(f) as datafile:
        lines =datafile.readlines()
        datafile.close()
        page = ' '.join(lines)
    page = page.replace("<br/>", " ")
    page = page.replace("<br>", " ")
    page = page.replace("</br>", " ")
    page = page.replace("$", " ")
    soup = BeautifulSoup(page)
    tables = soup.find_all('table')

    data = []
    for table in tables:

        for row in table.find_all('tr'):
            rr = []
            for cell in row.find_all('td'):
                #for string in cell.strings:
                string = cell.get_text()
                s = str(repr(string).encode('ascii', 'ignore'))
                rr += [s]
            data.append(rr)


    ret = []
    for i in range(0, len(data)):
        tr = []
        for j in range(0, len(data[i])):
            if len(data[i][j])>0:
                sss = eval(data[i][j].replace('\\xa0', ' '))
                sss = sss.replace('\n', '')
                tr += [sss]
        ret.append(tr)
    return ret


def TableTitle(f):
    import dateutil.parser as dparser

    table = ExtractTableHTML(f)
    numline = 0
    for i in range(0, len(table)):
        for cell in table[i]:
            if not cell.isspace():
                date = 0
                try:
                    date = dparser.parse(str(cell), fuzzy=False)
                except:
                    pass
                if date != 0:
                    year = date.year
                    if 1990 < year < 2014:
                        numline = i
                        break
    return numline


def FixWideSplitPos(f):
    table = ExtractTableHTML(f)
    numline = TableTitle(f)
    table = table[numline+1:]

    pos = []
    lines = table

    maxlen = 0
    for line in lines:
        if len(line) > maxlen:
            maxlen = len(line)

    for i in range(0, maxlen):
        test = 0
        for line in lines:
            try:
                s = str(line[i])
            except:
                s = ""
            print s
            try:
                if (s.isspace()):
                    test +=1
            except:
                test += 1
        if test == len(lines):
            pos.append(i)

    pos = [0] + pos

    posvec = []
    for k in range(1, len(pos)):
        if pos[k]-pos[k-1]>1:
            posvec.append(pos[k])
    posvec = [0] + posvec + [maxlen]

    return posvec



def ExtractContent(f):
    lines = ExtractTableHTML(f)
    numline = TableTitle(f)
    posvec = FixWideSplitPos(f)
    print posvec
    data = []
    for line in lines[numline+1:]:
        row = []
        for p in range(1, len(posvec)):
            s = " ".join(line[posvec[p-1]:posvec[p]])
            #s = str(repr(s).encode('ascii', 'ignore'))
            s = str(s)
            row += [s]
        data.append(row)
    return data






path = "C:/Users/Administrator/Dropbox/eric.ye.wang_gmail/Dropbox/PythonProjects/ResearchAsistant/"
path_data = path + "Data/"
path_target = path

file = 'pageHTML.txt'

f = path_data + file


for l in ExtractContent(f):
    print l

table = ExtractTableHTML(f)

with open(path_target + "page.csv", 'wb') as csvfile:
    tablewriter = csv.writer(csvfile, delimiter=';')
    for line in table:
        tablewriter.writerow(line)
csvfile.close()

