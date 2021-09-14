"""
Usage:

"""

import sys
import pandas as pd 
#Definitions
sample_filename = sys.argv[1]
#sample_filename = 'AlbertoCarbonell_sol401-41-21_AC-MS-2_09062021_filterprot_p2g.txt'
#Ecutoff = float(sys.argv[2])
output_filename = sample_filename.replace('.txt', '_filtergene.txt')
output_file = open(output_filename, 'w')

data = pd.read_table(sample_filename, )
genes = []

for i in range(len(data)):
    TAIR_id = data.iloc[i,3]
    genes.append(TAIR_id)
    output_file.write(TAIR_id + '\n')
    
output_file.close()

