# MicroAA-Mapper: A Novel Bioinformatics Pipeline for Identifying Amino Acid Sequences Targeted by miRNA in Breast Cancer
This is a pipeline for identifying amino acid sequences targeted by miRNA in BRCA using TarBase data and Interaction Clusters for MiRNA and MRNA Pairs in TCGA Network.

## Overview

## Requirements
- python
- pandas
- selenium
- biopython
- math


## Usage
### Step 0: Supplementary files
We used both the `Homo_sapiens_TarBase_v9.tsv.gz` file from TarBase and the BRCA section of Supplementary File 3 from "Identifying Interaction Clusters for MiRNA and MRNA Pairs in TCGA Network" which contained clustering results for 15 cancers, including breast cancer (BRCA). You can access these files at tarbase paper citaiton osmentig

### Step 1: Verify Clusters
Using `Customized Script 1`, you can filter the interaction clusters by extracting experimentally verified genes that match in both files. This results in a file with this format/information:
| species | mirna_name | mirna_id | gene_name	| gene_id |	gene_location | transcript_name	| transcript_id	| chromosome	| start	| end	| strand	| experimental_method	| regulation	| tissue	| cell_line	| article_pubmed_id	| confidence	| interaction_group	| cell_type	| microt_score |	comment	is_in_node |
|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:------------:|:------------|
