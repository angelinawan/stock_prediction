import csv
import json
import time
import datetime

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


csvfile = open('table_aapl.csv', 'r')
jsonfile = open('table_aapl.json', 'w')

fieldnames = ("timestamp","a","open","high","low","close","volume")
reader = csv.DictReader(csvfile, fieldnames)
jsonfile.write('[')
ISFIRST=True
for row in reader:
    x=row['timestamp']
    y=row['open']
    if(not ISFIRST):
        jsonfile.write(',\n')
    if(is_number(y) and is_number(x)):
        x0 = int(datetime.datetime.strptime(x, '%Y%m%d').strftime("%s"))*1000
        jsonfile.write("[%s,%s]"%(x0,y))
        ISFIRST=False
jsonfile.write(']')
