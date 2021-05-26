
# Protein2gene

***protein2gene*** is a Python code computational pipeline designed and implemented to process lists of proteins, mapping those genes of a model organism using BLAST. 
The scripts were developed to create a pipeline to analyze any list of proteins. 

## Introduction

Proteomics techniques allow the researchers to generate lists of proteins involved in a given biological condition. With this programe we aimed at performing the computational analysis of proteomics data generated from different experimental techniques. 

Proteomics experimental techniques produce large lists of proteins, represented by an identifier code, and *some calculated values*.

The limitations of 

The pipeline is composed by three independent but interelated Python scripts. 

# Utility

1. proteinfilter.py

```python proteinfilter.py [samplefilname] [control_filename] [AIcutoff]```

2. protein2gene.py

```python protein2gene.py [protein_filter_out_file]```

3. genefilter.py

```python genefilter.py [genefilter_out_filename] [threshold]```

## About the program...
Simplified workflows of the algorithm implemented in each script:

- Proteinfilter (script I)
![Proteinfilter](proteinfilter.png)

- ***protein2gene*** (script II)
![protein2gene](protein2gene.png)

- Genefilter (script III)
![Genefilter](genefilter.png)

# Dependencies
- Python 2.7.x
- Biopython
