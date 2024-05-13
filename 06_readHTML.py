
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

    with open("D:/test/tohtml.html", "w") as e:
        for line in lines:
            line = line.encode('ascii', 'ignore')
            insensitive_hippo = re.compile(re.escape('restricted cash'), re.IGNORECASE)
            line = insensitive_hippo.sub('<span style="background-color: #FFFF00">Restricted Cash</span>', line)
            e.write(line)
    return 1




f = "D:/test/test.txt"

ExtractTableHTML(f)


