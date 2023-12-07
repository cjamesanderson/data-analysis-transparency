# Charts and analyses functions for military sales data

#import numpy as np
import pylab
#import sqlite3

def change_scatter(curs):
    """
    change_scatter: scatter plot of changes in military sales by country
    :param curs: sqlite3 cursor object
    :rtype None:
    """
    sums_08 = curs.execute('''SELECT country, sum(articles)+sum(services) 
                              FROM sales 
                                WHERE year >= 2006 
                                AND year <= 2008 
                              GROUP BY country''').fetchall()
    sums_12 = curs.execute('''SELECT country, sum(articles)+sum(services) 
                              FROM sales 
                                WHERE year >= 2010 
                                AND year <= 2012 
                              GROUP BY country''').fetchall()
    # Merge lists by country name
    sums_all = country_merge(sums_08, sums_12)
    pylab.scatter([i[1] for i in sums_all], [i[2] for i in sums_all])
    axes = pylab.gca()
    xmin, xmax = axes.get_xlim()
    ymin, ymax = axes.get_ylim()
    pylab.plot([xmin, xmax], [xmin, xmax])
    pylab.show()
    
def country_merge(before, after):
    sums_all = list()
    for item_before in before:
        for item_after in after:
            if item_before[0] == item_after[0]:
                sums_all += [(item_before[0], item_before[1], item_after[1])]
                break
    return sums_all