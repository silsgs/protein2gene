#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 12:43:41 2021

@author: silvia

Usage example:
python3 ~/Silvia/Repositories/protein2gene/v1_py36/protein2gene_1.py AlbertoCarbonell_sol401-41-21_AC-MS-2_09062021_filterprot.txt
"""
# In[]
import os
import sys
import xml.etree.cElementTree as ElementTree
from Bio import Entrez
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Blast import NCBIXML
Entrez.email = 'silvia.santam@gmail.com'


## Setting working dir  
n_args = len(sys.argv)
path = os.getcwd() + '/'
path_v1 = os.path.dirname(os.path.abspath(__file__))
path_source = path_v1.replace('v1_py36', '')

## file names
#infilen = 'AlbertoCarbonell_sol401-41-21_AC-MS-2_09062021_filterprot.txt'
#infilen = 'in_test_filterprot.txt'
infilen = sys.argv[1]
infilename = infilen.replace('.txt','')
outfilename = infilename + '_p2g.txt'
tmpfilename_xml = path + infilename + '.giseq.xml'
tmpfilename_faa = path + infilename + '.giseq.faa'
dbfilename = path_source + 'TAIRdb/TAIR10_pep_20101214_updated'
blastfilename = path + infilename + '.blast.xml'
genes_gisname = path + infilename + '.gene_gis.txt'



def ParseXML (file):
    tmpfile = open(file, 'r')
    data = {}
    data['org'] = 'n/a'
    data['def'] = 'n/a'
    for line in tmpfile:
        if '<TSeq_orgname>' in line:
            data['org'] = line.split('>')[1].split('<')[0]
        if '<TSeq_defline>' in line:
            data['def'] = line.split('>')[1].split('<')[0]
        if '<TSeq_sid>' in line:
            data['id'] = line.split('>')[1].split('<')[0]
    tmpfile.close()    
    return data    

def checkBlast (blastfilename):
    handle = open(blastfilename, 'r')
    for line in handle:
        if '<Iteration_message>No hits found</Iteration_message>' in line:
            handle.close()
            return 0
    handle.close()    
    return 1

infile = open(infilen, 'r')
outfile = open(outfilename, 'w')
genes_gis = open(genes_gisname, 'w')
outfile.write('#NCBI_protein\torganism\tprotein_description\tTAIR_gene\torganism\tgene_description\te_blast\n')


if __name__ == "__main__":
    
    #check BlankLines
    protein_list = [line for line in infile.read().splitlines() if line]

    for gi in protein_list: 
        #print(str(gi))
        # check if gi exists in ncbi protein db
        handle_chk = Entrez.esearch(db='Protein', term=gi, retmax=1)
        record_chk = str(handle_chk.read())
        handle_chk.close()
        
        # First check if prot or gene
        if 'No items found' in record_chk:
            handle_chk2 = Entrez.esearch(db='Gene', term=gi, retmax=1)
            record_chk2 = str(handle_chk2.read())
            handle_chk2.close()
            
            if 'No items found' in record_chk2:
                # Not prot nor gene
                genes_gis.write('This gi: '+str(gi)+' is not found\n')
                print('This gi: '+str(gi)+' is not found')
                
            else:
                # Is a gene
                genes_gis.write(str(gi) + '\n')
                handle = Entrez.esearch(db='Gene', term=gi, retmax=1)
                root = ElementTree.fromstring(handle.read())
                handle.close()
                id_number = root.find("IdList/Id").text
                print(gi, '->', id_number)
                
                handle = Entrez.efetch(db='gene', id=id_number, rettype='xml', retmax=1) # or gi instead of id_number
                record = Entrez.read(handle)
                handle.close()
                
                if 'Arabidopsis' in record[0]['Entrezgene_source']['BioSource']['BioSource_org']['Org-ref']['Org-ref_taxname']:
                    org = record[0]['Entrezgene_source']['BioSource']['BioSource_org']['Org-ref']['Org-ref_taxname']
                    defin = 'n/a'
                    tair_id = record[0]['Entrezgene_gene']['Gene-ref']['Gene-ref_db'][0]['Dbtag_tag']['Object-id']['Object-id_str']
                    organism = org
                    if 'Gene-ref_syn' in record[0]['Entrezgene_gene']['Gene-ref'].keys():
                        definition = record[0]['Entrezgene_gene']['Gene-ref']['Gene-ref_syn'][0]
                    else:
                        definition = 'n/a'
                    evalue = 'n/a'
                    #write output        
                    outfile.write(gi.rstrip() + '\t')
                    outfile.write(org + '\t')
                    outfile.write(defin + '\t')
                    outfile.write(tair_id + '\t')
                    outfile.write(organism + '\t')
                    outfile.write(definition + '\t')
                    outfile.write(str(evalue) + '\n')
                
                
        else:         
            #download fasta from ncbi with the id
            handle = Entrez.esearch(db='Protein', term=gi, retmax=1)
            root = ElementTree.fromstring(handle.read())
            handle.close()
            id_number = root.find("IdList/Id").text
            print(gi, '->', id_number)
            # writes tmp file xml
            handle = Entrez.efetch(db='protein', id=id_number, rettype='fasta', retmode='xml') # or gi instead of id_number
            record = handle.read()
            handle.close()
            tmpfile_xml = open(tmpfilename_xml, 'w')
            tmpfile_xml.write(str(record, 'utf-8'))
            tmpfile_xml.close()
            # writes tmp file faa
            handle = Entrez.efetch(db='protein', id=id_number, rettype='fasta', retmode='text')
            record = handle.read()
            handle.close()
            tmpfile_faa = open(tmpfilename_faa, 'w')
            tmpfile_faa.write(str(record))
            tmpfile_faa.close()
    
            #parse fasta file
            data = ParseXML(tmpfilename_xml)
            #print(data)
    
            if 'virus' in data['org']:
                #print('This is a virus protein')
                tair_id = 'n/a'
                organism = 'n/a'
                definition = 'n/a'
                evalue = 'n/a'
            else:
                #run blast and write xml file    
                #cmd = 'blastall -p blastp -m 7 ' + ' -d ' + dbfilename + ' -i ' + tmpfilename + ' > ' + blastfilename
                cmd = 'blastp -query ' + tmpfilename_faa + ' -db ' + dbfilename + ' -outfmt 5 -out ' + blastfilename
                #print(cmd)
                blast = os.system(cmd)
    
                #parse blast results
                if checkBlast (blastfilename) == 1:
                    result_handle = open(blastfilename, 'r')
                    blast_record = NCBIXML.read(result_handle)    
                    for hit in blast_record.alignments:
                        gene_info = (hit.hit_def).split('|')
                        tair_id = gene_info[0].split('.')[0]
                        organism = 'Arabidopsis thaliana'
                        definition = gene_info[2]
                        evalue = (hit.hsps[0].expect)            
                        #we keep the first item
                        result_handle.close()
                        break
                else:
                    #print('No item found in blast')
                    tair_id = 'n/a'
                    organism = 'n/a'
                    definition = 'No item found in blast'
                    evalue = 'n/a'
    
            #write output        
            outfile.write(gi.rstrip() + '\t')
            outfile.write(data['org'] + '\t')
            outfile.write(data['def'] + '\t')
            outfile.write(tair_id + '\t')
            outfile.write(organism + '\t')
            outfile.write(definition + '\t')
            outfile.write(str(evalue) + '\n')


    cmd = 'rm ' + tmpfilename_xml + ' ' + tmpfilename_faa + ' ' + blastfilename
    
    os.system(cmd)

infile.close()
outfile.close()
genes_gis.close()