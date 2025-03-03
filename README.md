# MicroAA-Mapper: A Novel Bioinformatics Pipeline for Mapping Amino Acid Sequences Targeted by miRNAs in Breast Cancer
This is a pipeline for identifying amino acid sequences targeted by miRNA in *BRCA* using TarBase data and Interaction Clusters for miRNA and mRNA Pairs in The Cancer Genome Atlas Network.

## Overview

## Requirements
- python
- pandas
- selenium
- biopython
- math
- Excel
- DIANA-MicroT
- UCSC Genome Browser


## Usage
### Step 1: Supplementary files
We used both the `Homo_sapiens_TarBase_v9.tsv.gz` file from TarBase and the *BRCA* section of Supplementary File 3 from "Identifying Interaction Clusters for MiRNA and MRNA Pairs in TCGA Network" which contained clustering results for 15 cancers, including breast cancer (*BRCA*). You can access these files in the **References** section.

### Step 1: Verify Clusters
Using `Customized Script 1`, you can filter the interaction clusters by extracting experimentally verified genes that match in both files. This results in a file with this format/information:
| species | mirna_name | mirna_id | gene_name	| gene_id |	gene_location | transcript_name	| transcript_id	| chromosome | start | end | strand	| experimental_method	| regulation | tissue	| cell_line	| article_pubmed_id	| confidence | interaction_group | cell_type | microt_score | comment	is_in_node |
|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:------------:|:------------|
| Homo sapiens | hsa-mir-19a	| MIMAT0000073 | RANBP9	| ENSG00000010017	| CDS	| RANBP9-201 | ENST00000011619 | chr6	| 13639592 | 13639604	| -	| PAR-CLIP | Negative	| Kidney | HEK-293 | 20371350	| 1	| primary	| Epithelial cells | 0.53 | TRUE |

Using Excel, we filtered by tissue to include only breast tissue and used only the miRNA name, miRNA ID, and gene name from now on.

### Step 2: Search DIANA-MicroT Database
Using `Customized Script 2`, we automatically searched each verified gene with its miRNA in DIANA-MicroT. The script uses selenium to automatically conduct the searches, which gathers conservation score, genome position, transcript position, gene id, and binding area information, **specifically for CDS**. The input looks like this:
<div align="center">
<img src="https://github.com/user-attachments/assets/6ffdf333-e9b8-4831-953d-ddc538bc133a" width=60%>
</div>
The binding area on the webserver is in this format: 
<div align="center">
<img src="https://github.com/user-attachments/assets/63b69ae9-1161-4c1a-9ca6-7478ef1e3643" width=60%>
</div>

*example input: hsa-mir-424 and LRP8*

The script annotates the whole sequence and only the longest portion.

*Note: Inputs that generate multiple results create new rows for each result.*

The output will look like this:

| mirna_name | mirna_id | conservation score | gene_name | mrna binding area longest | Genome position | transcript position | gene id | mrna Binding Area full	| 
|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|
| hsa-let-7b | MIMAT0000063	| 1	| PPP4C | ACUACCUC | chr16:30082761-30082778 | ENST00000566749:216-233 | ENSG00000149923 | CC A GACC ACUACCUC |
| hsa-let-7b | MIMAT0000063 | |	SPATA2 | NA	| | | | | |			

### Step 3: Extract Amino Acids
Using `Customized Script 3`, the amino acid sequences are annotated using UCSC Genome browser. The script uses biopython and selenium to access amino acid data. Genome positions are used to generate dna sequences, which are translated in all forward and reverse frames for identifying the correct sequence in the result produced by the table browser. Genome positions with multiple areas in the format `chr15:41762350;41764886-41762362;41764896` are also able to be processed. You can input the same .xlsx file from before or one with a `genome positions` column. The table browser settings we used looked like this: 

<div align="center">
<img src="https://github.com/user-attachments/assets/39c9dee2-abea-4221-a4dc-aef103a47fa7" width=60%>
</div>
<div align="center">
<img src="https://github.com/user-attachments/assets/7ba932b8-da79-4a5a-94f6-b3972d9f7844" width=60%>
</div>
<div align="center">
<img src="https://github.com/user-attachments/assets/d7fac910-73d3-473a-95e1-192c8b28efd4" width=60%>
</div>

The genome positions will be entered in the `Position` field.

## Results
This process produces a spreadsheet containing miRNA and gene information for identifying mutations in coding regions of mRNAs targeted by miRNAs to elucidate candidate biomarkers with amino acid sequences. This can be used in combination with other softwares for further analysis, such as Alphafold. Our resulting spreadsheet looked like this:
| mirna_name | mirna_id | conservation score | gene_name | mrna binding area longest | Genome position | transcript position | gene id | mrna Binding Area full	| 
|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|:------------|:-----------:|
| hsa-let-7b | MIMAT0000063	| 1	| PPP4C | ACUACCUC | chr16:30082761-30082778 | ENST00000566749:216-233 | ENSG00000149923 | CC A GACC ACUACCUC |
| hsa-let-7b | MIMAT0000063 | |	SPATA2 | NA	| | | | | |

## References
- Dai, Xinqing, Lizhong Ding, Hannah Liu, Zesheng Xu, Hui Jiang, Samuel K Handelman, and Yongsheng Bai. 2019. "Identifying Interaction Clusters for MiRNA and MRNA Pairs in TCGA Network" Genes 10, no. 9: 702. https://doi.org/10.3390/genes1009070
- Nelson HD, Pappas M, Cantor A, Haney E, Holmes R. Risk Assessment, Genetic Counseling, and Genetic Testing for BRCA-Related Cancer in Women: Updated Evidence Report and Systematic Review for the US Preventive Services Task Force. JAMA. 2019;322(7):666–685. doi:10.1001/jama.2019.8430
- O'Brien J, Hayder H, Zayed Y, Peng C. Overview of MicroRNA Biogenesis, Mechanisms of Actions, and Circulation. Front Endocrinol (Lausanne). 2018 Aug 3;9:402. Doi:	10.3389/fendo.2018.00402. PMID: 30123182; PMCID: PMC6085463.
- Paraskevopoulou, M. D., Georgakilas, G., Kostoulas, N., Vlachos, I. S., Vergoulis, T., Reczko, M., Filippidis, C., Dalamagas, T., & Hatzigeorgiou, A. G. (2013). DIANA-microT web server v5.0: service integration into miRNA functional analysis workflows. Nucleic acid research, 41(Web Server issue), W169–W173. https://doi.org/10.1093/nar/gkt393
- Perez, G., Barber, G. P., Benet-Pages, A., Casper, J., Clawson, H., Diekhans, M., Fischer, C., Gonzalez, J. N., Hinrichs, A. S., Lee, C. M., Nassar, L. R., Raney, B. J., Speir, M. L., van Baren, M. J., Vaske, C. J., Haussler, D., Kent, W. J., & Haeussler, M. (2025). The UCSC Genome Browser database: 2025 update. Nucleic acids research, 53(D1), D1243–D1249. https://doi.org/10.1093/nar/gkae974
- Sethupathy, P., Corda, B., & Hatzigeorgiou, A. G. (2006). TarBase: A comprehensive database of experimentally supported animal microRNA targets. RNA (New York, N.Y.), 12(2), 192–197. https://doi.org/10.1261/rna.2239606
- Varadi, M. et al. “AlphaFold Protein Structure Database: massively expanding the structural coverage of protein-sequence space with high-accuracy models.” Nucleic Acids Research, 50(D1), pages D439–D444 (2021). DOI: 10.1093/nar/gkab1061
