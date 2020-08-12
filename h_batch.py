from hcheck import hcheck
import csv
# from datetime import date as dt
import subprocess as sp

a = hcheck()
reslog = ''
errorlist = list()

# read data from csv and execute them all
with open('hcheck.csv', 'r', newline='', encoding='utf-8') as f:
    csvr = csv.reader(f)
    next(csvr)
    for row in csvr:
        res = a.check(row[1], row[2])
        if res:
            print(row[1], end='success\n')
            reslog += (row[1] + '\n')
        else:
            print(row[1], end='fail\n')
            errorlist.append(row[1], row[2])

# re-execute
while errorlist:
    for i in range(len(errorlist)):
        row = errorlist[i]
        res = a.check(row[0], row[1])
        if res:
            print(row[0], end='success\n')
            reslog += (row[0] + '\n')
            del errorlist[i]
        else:
            print(row[0], end='fail\n')

with open(a.yymmdd+'.log', 'w', encoding='utf-8') as f:
    f.write(reslog)

a.checkend
a = None

sp.call(["pkill", "chrome"])
# chromedriver never dies
