__author__ = 'Ye Wang'


import os
import shutil
import re
import csv
from bs4 import BeautifulSoup
import asciitable
import string


def DelBiaodian(s):
    ret = s
    for c in string.punctuation:
        ret = ret.replace(c, " ")
    return ret


def Unit(s):
    page = s
    if "million" in page.lower():
        ret = "m"
    else:
        ret = "t"
    return ret


def ExtractTitle(f):
    ret = ""
    with open(f) as datafile:
        lines =datafile.readlines()
        datafile.close()

        ss = lines

        start = 0
        end = len(ss)

        for i in range(0, len(ss)):
            if "<table>" in ss[i].lower():
                start = i
                break
        for j in range(start, len(ss)):
            if ("<s>" in ss[j].lower()) or ("<c>" in ss[j].lower()):
                end = j
        temp = ""
        if end > start:
            temp = "".join(ss[start+1:end])
        temp = temp.split("\n")

        ret = []
        for ll in temp:
            if len(ll)>0:
                ret.append(ll)
    return ret


def ExtractTable(f):
    ret = ""
    with open(f) as datafile:
        lines =datafile.readlines()
        datafile.close()

        ss = lines

        start = 0
        end = len(ss)

        for i in range(0, len(ss)):
            if "<s>" in ss[i].lower():
                start = i
                break
        for j in range(start, len(ss)):
            if ("</s>" in ss[j].lower()) or ("total" in ss[j].lower()):
                end = j
        temp = ""
        if end > start:
            temp = "".join(ss[start+1:end])
        temp = temp.split("\n")

        ret = []
        for ll in temp:
            if len(ll)>0:
                ret.append(ll)
    return ret


def FixWideSplitPos(f):
    pos = []
    lines = ExtractTable(f)
    maxlen = 0
    for line in lines:
        if len(line) > maxlen:
            maxlen = len(line)
    for i in range(0, maxlen):
        test = 0
        for line in lines:
            try:
                if (line[i].isspace()):
                    test +=1
            except:
                test += 1
        if test >= 0.8*len(lines):
            pos.append(i)
    pos = [0] + pos

    posvec = []
    for k in range(1, len(pos)):
        if pos[k]-pos[k-1]>1:
            posvec.append(pos[k])
    posvec = [0] + posvec + [maxlen]

    return posvec


def ExtractContent(f):
    lines = ExtractTable(f)
    posvec = FixWideSplitPos(f)
    data = []
    for line in lines:
        row = []
        for p in range(1, len(posvec)):
            row += [line[posvec[p-1]:posvec[p]].rstrip().lstrip()]
        #data.append([f] + row)
        data.append(row)
    return data


def ExtractYear(f):
    lines = ExtractTitle(f)
    posvec = FixWideSplitPos(f)
    data = []
    for line in lines:
        row = []
        for p in range(1, len(posvec)):
            row += [line[posvec[p-1]:posvec[p]].rstrip().lstrip()]

        for cc in range(0, len(row)):
            row[cc] = DelBiaodian(row[cc])

        k = 0
        for cell in row:
            try:
                if 1990 < int(cell) < 2014:
                    k +=1
            except:
                pass
        if k>0:
            data.append(row)

    return data


def RestrictedCash(f):
    data = []
    table = ExtractContent(f)
    title = ExtractYear(f)

    titletext = " ".join(ExtractTitle(f))

    if len(title)==1:
        data.append(title[0])
    for line in table:
        data.append(line)
    if len(title)==1:
        table = data
    else:
        table = []

    RCrow = []
    for row in table:
        s = row[0].lower()
        s = DelBiaodian(s)
        if ("restricted cash" in s) and (not "change" in s) and (not "includ" in s):
            RCrow = row
            break

    data = []
    for j in range(1, len(RCrow)):
        if table[0][j].isdigit():
            sign = 1
            rc = RCrow[j]
            if ("(" in rc) and (")" in rc):
                sign = -1
            for c in string.punctuation:
                rc = rc.replace(c, "")
            try:
                rc = int(rc)
            except:
                rc = -1
            if Unit(titletext)=="m":
                rc = rc*1000
            rcr = [f, table[0][j], rc, sign]
            data.append(rcr)
    return data



path = "F:/003_RestrictedCash_Giambona/"
path_data = path + "ParsedFilings/COMPUSTATmatched/10KtablesTXT/"
path_target = path


#try:
#    shutil.rmtree(path_target, ignore_errors=True)
#except IOError:
#    pass

#if not os.path.exists(path_target):
#    os.makedirs(path_target)


title = ["FileName", "Year", "Restricted Cash"]
files = os.listdir(path_data)
os.chdir(path_data)



sf = path_target + "Restricted_Cash.csv"

with open(sf, 'wb') as csvfile:
    tablewriter = csv.writer(csvfile, delimiter=';')
    tablewriter.writerow(title)
    for f in files:
        print f
        table = RestrictedCash(f)
        for line in table:
            tablewriter.writerow(line)
    csvfile.close()














