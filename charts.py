#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import the pyplot library
import matplotlib.pyplot as plt
import numpy as np

def pie_chart():

    #data-vr
    total_vr, buggy_vr = 19832, 2226 
    clean_vr = total_vr - buggy_vr
    values_vr = [clean_vr, buggy_vr]

    #data-non-vr
    total_nvr, buggy_nvr = 20418, 1903
    clean_nvr = total_nvr - buggy_nvr
    values_nvr = [clean_nvr, buggy_nvr]

    #colors = ['b', 'g', 'r', 'c', 'm', 'y']
    colors = ['b', 'r']
    labels = ['Clean Classes', 'Fault pronner classes']
    explode = (0, 0)
    plt.pie(values_vr, colors=colors, labels= values_vr,explode=explode,counterclock=False, shadow=True)
    plt.axis('equal')

    #plt.title('Classification of the analyzed instances according to ACL')
    
    plt.legend(labels,loc=3)
    plt.show()

def stacked_histogram():

    N = 4
    clean = (47.44, 150.62, 287.20, 792.66)
    fault = (6.25, 15.11, 35.31,71.5)
    
    #colors = ['b', 'g', 'r', 'c', 'm', 'y']
    colors = ['b', 'r']    
        
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, clean, width)
    
    p2 = plt.bar(ind, fault, width, bottom=clean)


    #plt.title('Distribution of defects by size of the repositories')
    plt.ylabel('Classes')
    plt.xlabel('Grouping of repositories by number of classes')
    
    plt.xticks(ind, ('1~100', '101~200', '201~500', '500+'))
    plt.yticks(np.arange(0, 1100, 100))
    plt.legend((p1[0], p2[0]), ('Clean', 'Fault'))


    plt.show()    

if __name__ == "__main__":
    
    pie_chart()
    #stacked_histogram()