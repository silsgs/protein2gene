import sys

#Definitions
sample_filename = sys.argv[1]
Ecutoff = float(sys.argv[2])
output_filename = sample_filename.replace('.txt', '_filtergene.txt')


f = open(sample_filename, 'r')
output_file = open(output_filename, 'w')

genes = []
for line in f:
	items = line.split('\t')
	TAIR_id = items[3]
	if TAIR_id == 'TAIR_gene' or ('n/a' in line):
		continue
	e_blast = float(items[6])	
	if not 'n/a' in line and e_blast <= Ecutoff:
		if TAIR_id not in genes:
			genes.append(TAIR_id)
			output_file.write(TAIR_id + '\n')

f.close()
output_file.close()
