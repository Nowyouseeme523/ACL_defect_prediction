#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pandas as pd
import statistics as stats



def compute_HAM_MVM(afile):

    #will store the results
    HAM_values = {}
    MVM_values = {}    

    #read csv and drop LCOM metric
    repository = pd.read_csv(afile)
    repository.drop('LCOM', axis=1, inplace=True)

    columns = repository.columns

    #calculate HAM 
    for c in columns[1:]:
        HAM = repository[c].mean()/2
        HAM_values[c] = HAM

    #iterate over the rows to calculate de MVM
    for index, row in repository.iterrows():
        
        #results array
        results = []

        #gonna check the metric values for each column
        for c in columns:
            
            #First column is the name of the module. Avoid and store the name of the module analyzed 
            if c == "Type":
                module = str(row[c])
                continue
            
            #get the value of the metric
            value = row[c]
            
            #The value of the result with the HAM value of the metric
            if value > HAM_values[c]:
                results = results + [1]
            else:
                results = results + [0]

        MVM_values[module] = results
    
    return HAM_values, MVM_values


def compute_cutoff(HAM_values, MVM_values):
    
    number_of_metrics = len(list(HAM_values.keys()))
    number_of_instances = len(list(MVM_values.keys()))

    mivs_values = {}
    possible_defects = 0

    for key, values in MVM_values.items():    
        
        mivs = sum(values)
        mivs_values[key] = mivs

        if mivs > (number_of_metrics/2):
            possible_defects = possible_defects + 1
    
    #a list with the mivs results
    mivs_list   = mivs_values.values()

    amivs = stats.mean(mivs_list) #average of mivs
    amivs_plus  = stats.mean(set(mivs_list)) #average of disticts mivs  
    mivs_median = stats.median(mivs_list) #median of mivs

    hmivs_mean  = stats.harmonic_mean([amivs_plus,mivs_median]) #hamonic mean of amivs+ and mivs_median

    possible_defects_rate = possible_defects / number_of_instances

    if possible_defects_rate > 0.5:
        cutoff = hmivs_mean * possible_defects_rate + (number_of_metrics - amivs) * (1 - possible_defects_rate) 
    else:
        cutoff = 2 * number_of_metrics * (1-possible_defects_rate) * hmivs_mean / number_of_metrics * (1 - possible_defects_rate) + hmivs_mean 

    for instance, value in mivs_values.items():

        if value > cutoff:
            print("{} : buggy".format(instance))
        else:
            print("{} : clean".format(instance))


if __name__ == '__main__':
    
    base_dir = os.getcwd()

    #Verify the execution
    if len(sys.argv) < 2:
        print('Usage: python acl.py instance.csv')
        sys.exit(-1)

    target_file = str(sys.argv[1]) #csv with the instances and metrics
    target_dir  = base_dir + "/repositories/" + target_file

    #cumpute results
    HAM_values, MVM_values = compute_HAM_MVM(target_dir)
    compute_cutoff(HAM_values, MVM_values)