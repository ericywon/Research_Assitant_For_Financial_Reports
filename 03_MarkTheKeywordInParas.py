__author__ = 'Ye Wang'


import re
import shutil
import os

def MarkKeyword(f):
    with open(f) as datafile:
        s =datafile.readlines()
        datafile.close()
        s = " ".join(s)
    keywordsearch = re.compile(re.escape('restricted cash'), re.IGNORECASE)
    lines = keywordsearch.sub('  ******_RESTRICTED CASH_******  ', s)
    return lines


path = "F:/003_RestrictedCash_Giambona/"
path_data = path + "sample/"
path_target = path + "10KparasMarked/"

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
    f = path_data + file
    s = MarkKeyword(f)

    with open(path_target + file, "w") as text_file:
        text_file.write(s)
        text_file.close()




print "Done!"





