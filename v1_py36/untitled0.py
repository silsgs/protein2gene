#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 20:05:26 2021

@author: silvia
"""

# In[]
import time
from Bio import SeqIO
from Bio import Entrez
import xml.etree.ElementTree as ET
import xml.etree.cElementTree as ElementTree
Entrez.email = 'silvia.santam@gmail.com'
# In[]

infilen = 'AlbertoCarbonell_sol401-41-21_AC-MS-2_09062021_filterprot.txt'
infile = open(infilen, 'r')
protein_list = [line for line in infile.read().splitlines() if line]

infile.close()

# In[]

infilen = 'AlbertoCarbonell_sol401-41-21_AC-MS-2_09062021_filterprot.gene_gis.txt'
infile = open(infilen, 'r')
gene_list = [line for line in infile.read().splitlines() if line]

infile.close()

# In[]
term = 'Q9C5Z3'
handle = Entrez.esearch(db='protein', term=term, retmax=1)
root = ElementTree.fromstring(handle.read())
handle.close()
id_number = root.find("IdList/Id")#.text
print(term, '->', id_number.text)

# In[]
htxt = Entrez.efetch(db='gene', id='818859', retmax=1, rettype='xml')
rtxt = htxt.read()

tmpfile_xml = open('tmp.xml', 'w')
tmpfile_xml.write(str(rtxt, 'utf-8'))
tmpfile_xml.close()

# In[]

####
####
####
#gi = 'A0A1P8B9L6'
for gi in gene_list:
    handle = Entrez.esearch(db='Gene', term=gi, retmax=1)
    root = ElementTree.fromstring(handle.read())
    id_number = root.find("IdList/Id").text
    print(gi, '->', id_number)
    
    handle = Entrez.efetch(db='gene', id=id_number, rettype='xml', retmax=1) # or gi instead of id_number
    record = Entrez.read(handle)
    handle.close()
    if 'Gene-ref_syn' in record[0]['Entrezgene_gene']['Gene-ref'].keys():
        definition = record[0]['Entrezgene_gene']['Gene-ref']['Gene-ref_syn']
    else:
        definition = 'n/a'
    if 'Arabidopsis' in record[0]['Entrezgene_source']['BioSource']['BioSource_org']['Org-ref']['Org-ref_taxname']:
        org = record[0]['Entrezgene_source']['BioSource']['BioSource_org']['Org-ref']['Org-ref_taxname']
        print(org)
    print(record[0]['Entrezgene_gene']['Gene-ref']['Gene-ref_db'][0]['Dbtag_tag']['Object-id']['Object-id_str'])
    print(definition)