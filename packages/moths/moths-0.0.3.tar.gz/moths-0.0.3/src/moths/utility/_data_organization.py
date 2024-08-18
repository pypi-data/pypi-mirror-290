# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 19:07:15 2024

@author: richie bao
"""

def nestedListGrouping4(nested_lst):
    grouped=[]
    for m in range(len(nested_lst)-1):
        a=nested_lst[m]
        b=nested_lst[m+1]
        for i in range(len(a)-1):
            lst=[]
            lst.append(b[i])
            lst.append(a[i])
            lst.append(b[i+1])
            lst.append(a[i+1])
            grouped.append(lst)
    return grouped

