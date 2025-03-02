import csv
import pandas as pd
import re

path = "your tsv or csv file path"

data=pd.read_csv(path,sep='\t')
df=pd.DataFrame(data)
xls = pd.ExcelFile('xlsx file (originally supplementary file 3)')
BRCA = pd.read_excel(xls, 'your gene (originally BRCA)')
BRCA=pd.DataFrame(BRCA)
sig=BRCA.query('q_value<0.1') #adjustable

df['gene_name'] = df['gene_name'].astype(str)
sig['node'] = sig['node'].astype(str)

def remove_suffix(value):
    return re.sub(r'-\w+$', '', value.lower())

df['mirna_name'] = df['mirna_name'].apply(remove_suffix)
df['mirna_name'] = df['mirna_name'].astype(str)

def check_gene_in_node(row, nodes):
    gene_name = row['gene_name']
    mirna_name = row['mirna_name']
    return any(gene_name in node and mirna_name in node for node in nodes)

df['is_in_node'] = df.apply(lambda row: check_gene_in_node(row, sig['node']), axis=1)

filtered_df = df[df['is_in_node'] == True]
print(filtered_df)
