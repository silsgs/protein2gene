"""

"""

import sys

#Definitions
sample_filename = sys.argv[1]
control_filename = sys.argv[2]
AIcutoff = float(sys.argv[3])
output_filename = sample_filename.replace('.txt', '_filterprot.txt')


def select_proteins(filename):
    f = open(filename, 'r')
    proteins = {}
    for line in f:
        line_elements = line.split()
        if len(line_elements)==1:
            proteins[line_elements[0]] = -1
        else: 
            proteins[line_elements[0]] = line_elements[1]
    f.close()
    return proteins


if __name__ == "__main__":
    
    sample_proteins = select_proteins(sample_filename)
    control_proteins = select_proteins(control_filename)

    output_file = open(output_filename, 'w')
    for p in sample_proteins:
        if sample_proteins[p] < 0:
            if p not in control_proteins:
                output_file.write(p + '\n')
        else:
            if p in control_proteins:
                if float(sample_proteins[p]) - float(control_proteins[p]) >= AIcutoff:
                    output_file.write(p + '\n')
            else:
                if float(sample_proteins[p]) >= AIcutoff:
                    output_file.write(p + '\n')

output_file.close()
