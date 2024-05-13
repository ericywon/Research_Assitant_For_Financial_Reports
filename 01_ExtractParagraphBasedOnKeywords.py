__author__ = 'Ye Wang'


from Form10K import *
import os
import shutil
import re
from nltk.tokenize import BlanklineTokenizer, word_tokenize, sent_tokenize
from bs4 import BeautifulSoup
import urllib2
import csv
from pattern.web import URL, plaintext
import json, ast
import nltk
from nltk.tag.stanford import NERTagger
import os
java_path = "C:/Program Files/Java/jdk1.8.0_05/bin/java.exe"
os.environ['JAVAHOME'] = java_path

#nltk.internals.config_java("C:/Program Files/Java/jdk1.8.0_05/bin/java.exe")
path_package = "D:/000_RESEARCH/PythonProjects/stanford-ner-2014-08-27/"
st = NERTagger(path_package + 'classifiers/english.all.3class.distsim.crf.ser.gz',
               path_package + 'stanford-ner.jar')





keyword = ["restricted cash"]


def all_occurences(file, str):
    initial = 0
    while True:
        initial = file.find(str, initial)
        if initial == -1:
            return
        yield initial
        initial += len(str)


def TextCleanHTML(f):
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

        lines = strip_between('<table','</table>',lines)
        lines = strip_between('<TABLE','</TABLE>',lines)
        lines = re.sub(r"<.?s[^>]*>", "", lines)
        lines = re.sub(r"<.?c[^>]*>", "", lines)
        lines = re.sub(r"<.?S[^>]*>", "", lines)
        lines = re.sub(r"<.?C[^>]*>", "", lines)


        lines = plaintext(lines[:item1]).encode('ascii', 'ignore')
        insensitive_hippo = re.compile(re.escape('table of contents'), re.IGNORECASE)
        lines = insensitive_hippo.sub(' ', lines)
        paras = BlanklineTokenizer().tokenize(lines)
        #for i in range(0, len(paras)):
        #    paras[i] = paras[i].replace("\n", " ")
        #    paras[i] = re.sub(' +',' ', paras[i]).lstrip()
    return paras


def TextCleanTXT(f):
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

        lines = strip_between('<table','</table>',lines)
        lines = strip_between('<TABLE','</TABLE>',lines)
        lines = re.sub(r"<.?s[^>]*>", "", lines)
        lines = re.sub(r"<.?c[^>]*>", "", lines)
        lines = re.sub(r"<.?S[^>]*>", "", lines)
        lines = re.sub(r"<.?C[^>]*>", "", lines)

        lines = lines[:item1].encode('ascii', 'ignore')
        insensitive_hippo = re.compile(re.escape('table of contents'), re.IGNORECASE)
        lines = insensitive_hippo.sub(' ', lines)
        paras = BlanklineTokenizer().tokenize(lines)

    return paras


def Alpha(string):
    ret = 0
    for char in string:
        if char.isalpha():
            ret = 1
            break
    return ret


def Paras(file):
    ret = []
    if TypeHTML(file)==1:
        paras = TextCleanHTML(file)
    else:
        paras = TextCleanTXT(file)
    for i in range(0, len(paras)):
        found = 0
        for word in keyword:
            if word in paras[i].lower():
                found += 1
        if found > 0:
            ret.append(paras[i])
    return ret




path = "H:/Projects/RestrictedCash/"
path_data = "H:/SECfilings/10-K/Form10K/"
path_target = path + "10Kparas/"

try:
    shutil.rmtree(path_target, ignore_errors=True)
except IOError:
    pass


if not os.path.exists(path_target):
    os.makedirs(path_target)


files = os.listdir(path_data)
os.chdir(path_data)

for file in files:
    print file
    try:
        getparas = []
        f = path_data + file
        getparas = Paras(f)

        s = "\n\n".join(getparas)

        with open(path_target + file, "w") as text_file:
            text_file.write(s)
            text_file.close()

        sf = path_target + file
        if os.path.getsize(sf) == 0:
            os.remove(sf)
    except:
        pass



print "Done!"















