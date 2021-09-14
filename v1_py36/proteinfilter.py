#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 11:20:12 2021

@author: silvia

Usage example:
python3 ~/Silvia/Repositories/protein2gene/v1_py36/proteinfilter_1.py AlbertoCarbonell_sol401-41-21_AC-MS-1_09062021_20210616230812.txt AlbertoCarbonell_sol401-41-21_AC-MS-2_09062021.txt

"""
import os
import sys
import pandas as pd

## Setting working dir & file names 
n_args = len(sys.argv)
path = os.getcwd() + '/'

data_file1 = sys.argv[1]
data_file2 = sys.argv[2]
output_f = path + data_file2.replace('.txt', '_filterprot.txt')

## This should be checked and changed as needed
d1 = pd.read_csv(data_file1,encoding='utf-16', sep='\t',)
d2 = pd.read_csv(data_file2,encoding='utf-16', sep='\t',)

d1 = d1.dropna()
d2 = d2.dropna()

if n_args >= 4:
    AIcutoff = sys.argv[3]
    d1sign = d1[~d1.Coverage >= AIcutoff]
    d2sign = d2[~d2.Coverage >= AIcutoff]
    duniq = d2sign[~d2sign.Accession.isin(d1sign.Accession)]

else:
    duniq = d2[~d2.Accession.isin(d1.Accession)]
    
        

with open(output_f, 'w') as f:
    for text in duniq['Accession'].tolist():
        f.write(text + '\n')
