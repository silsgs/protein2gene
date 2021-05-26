
# Protein2gene

***protein2gene*** is a Python code computational pipeline designed and implemented to process lists of proteins, mapping those genes of a model organism using BLAST. 
The scripts were developed to create a pipeline to analyze any list of proteins. 

## Introduction

Proteomics techniques allow the researchers to generate lists of proteins involved in a given biological condition. With this programe we aimed at performing the computational analysis of proteomics data generated from different experimental techniques. 

Proteomics experimental techniques produce large lists of proteins, represented by an identifier code, and *some calculated values*.

The limitations of 

The pipeline is composed by three independent but interelated Python scripts. 

# Utility

```python proteinfilter.py [samplefilname] [control_filename] [AIcutoff]```
```python protein2gene.py [protein_filter_out_file]```
```python genefilter.py [genefilter_out_filename] [threshold]```

# Dependencies
- Python 2.7.x
- Biopython
