import sys
import os

#definitions
path = '/home/silgisan/Desktop/Project/'
infilename = sys.argv[1]
outfilename = infilename.replace('.txt','_p2g.txt')
tmpfilename = path + infilename + '.gifasta.tmp'
dbfilename = path + 'TAIRdb/TAIR10_pep_20101214_updated'
blastfilename = path + infilename + '.blast.xml'

from Bio import Entrez
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Blast import NCBIXML
Entrez.email = 'silvia.santam@gmail.com'

def ParseXML (tmpfilename):
	tmpfile = open(tmpfilename, 'r')
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

infile = open(infilename, 'r')
outfile = open(outfilename, 'w')
outfile.write('#NCBI_protein\torganism\tprotein_description\tTAIR_gene\torganism\tgene_description\te_blast\n')

#check BlankLines
protein_list = [line for line in infile.read().splitlines() if line]

for gi in protein_list:	
	#download fasta from ncbi with the id
	handle = Entrez.efetch(db='protein', id=gi, rettype='fasta', retmode='xml')
  	record = handle.read()
	tmpfile = open(tmpfilename, 'w')
	tmpfile.write(record)
	tmpfile.close()
	
	#parse fasta file
	data = ParseXML(tmpfilename)

	if 'virus' in data['org']:
		#print('This is a virus protein')
		tair_id = 'n/a'
		organism = 'n/a'
		definition = 'n/a'
		evalue = 'n/a'
	else:
		#run blast and write xml file	
		cmd = 'blastall -p blastp -m 7 ' + ' -d ' + dbfilename + ' -i ' + tmpfilename + ' > ' + blastfilename
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
				#print('The gene is %s' % gene)
				#print('Definition: %s' % definition)
				#print('e-value: %f' % evalue)
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

	

cmd = 'rm ' + tmpfilename
os.system(cmd)
cmd = 'rm ' + blastfilename
os.system(cmd)
infile.close()
outfile.close()
