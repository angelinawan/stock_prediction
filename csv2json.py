import csv
import json
import time
import datetime
import os
import sys
import pandas as pd
import math


import DATA_CONSTANT

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def csvfolder2json(indir,outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    files = os.listdir(indir)

    for f in files:
        if f.endswith(".csv"):
            csvfilepath="%s/%s"%(indir,f)
            symbol = os.path.splitext(f)[0]
            jsonfilepath="%s/%s.json"%(outdir,symbol)
            jsonfilepath_pred = "%s/%s_pred.json" % (outdir, symbol)
            csv2json(csvfilepath,jsonfilepath,'y')
            csv2json(csvfilepath, jsonfilepath_pred, 'y_pred')

def csvfolder2json2(indir,outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    files = os.listdir(indir)
    for f in files:
        if f.endswith(".csv"):
            csvfilepath="%s/%s"%(indir,f)
            symbol = os.path.splitext(f)[0]
            jsonfilepath="%s/%s.json"%(outdir,symbol)
            csv2json(csvfilepath, jsonfilepath.lower(), DATA_CONSTANT.COL_TARGET)
            for model in DATA_CONSTANT.ML_MODEL_LIST:
                jsonfilepath_pred = "%s/%s_%s.json" % (outdir, symbol, model)
                csv2json(csvfilepath, jsonfilepath_pred.lower(), model)

def csv2json(csvfilepath,jsonfilepath,y_col):
    csvfile = open(csvfilepath, 'r')
    jsonfile = open(jsonfilepath, 'w')

    df = pd.read_csv(csvfilepath, index_col=DATA_CONSTANT.IDX_DATE, parse_dates=[DATA_CONSTANT.IDX_DATE])
    ISFIRST = True
    jsonfile.write('[')
    for index, row in df.iterrows():
        x = index
        y = row[y_col]
        if (is_number(y) and not math.isnan(y)):
            if (not ISFIRST):
                jsonfile.write(',\n')
            #x0=datetime.fromtimestamp(x)
            x0 = int(x.strftime("%s")) * 1000
            jsonfile.write("[%s,%s]" % (x0, y))
            ISFIRST = False
    jsonfile.write(']')


if __name__ == '__main__':
    #indir=str(sys.argv[1])
    #outdir=str(sys.argv[2])
    indir='../../Data/ML_output/'
    outdir="../../Data/ML_output/json"
    csvfolder2json2(indir, outdir)
