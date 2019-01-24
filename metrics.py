#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pandas as pd

def compute_metrics(afile):

    results = []

    repo = pd.read_csv(afile,sep=',')

    #get general information of each repositorie
    num_classes = repo['Type'].count()
    lines_code = repo['LOC'].sum()

    try:
    	repo.drop('LCOM', axis=1, inplace=True)
    except Exception as e:
    	print("Error file: {}".format(afile))    
    
    #sum of all values of each column
    new_df = repo.sum()

    #get the name of the columns
    columns = list(repo.columns.values)

    try:
        columns.remove('Type') #name isn't important
    except:
        print("E: Can't do operation in: {}".format(afile))


    #get the total of each column and place inside a index of a list
    for c in columns:
        r =  new_df[c]
        results = results + [r]

    #return a list with the total of each column 
    return results, num_classes, lines_code
    

if __name__ == '__main__':
    
    #base dir
    base_dir = os.getcwd()

    repositories_path  = base_dir + "/repositories/metrics/non-vr"

    os.chdir(repositories_path)

    #final results
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    classes, loc, total_classes, total_loc = 0, 0, 0, 0
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            
            if ".csv" not in name:
                continue

            #comput sum value for all columns
            result = []
            result, classes, loc = compute_metrics(name)
            total_loc += loc
            total_classes += classes
    
            #sum the values of all files in results
            for i in range(len(result)):
                results[i] += result[i]
    
    #name of the columns
    columns = ['NOF','NOM','NOP','NOPF','NOPM','LOC','WMC','NC','DIT','LCOM','Fan-Out', 'Fan-In']

    #print the values
    for column, value in zip(columns, results):
        print("{}: {}".format(column, value))

    #other information
    print('Lines of code: ', total_loc)    
    print('Number of classes: ', total_classes)