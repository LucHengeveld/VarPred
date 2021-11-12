from matplotlib.pyplot import get_current_fig_manager
import pandas as pd
import os


def open_tsv(location):
    return pd.read_csv(location, sep="\t")


def filter_data(data):
    return data[((data.CLNREVSTAT == "reviewed by expert panel") |
                (data.CLNREVSTAT == "practice guideline")) &
                (data.CLNSIG != "Uncertain significance")]


def write_tsv(data, name):
    data.to_csv(name, sep="\t", index=False)

def getGenes(data):
    gene_list = data['GENEINFO']
    gene_code_list = []
    for gene in gene_list:
        gene_code = str(gene).split(':')[0]
        gene_code_list.append(gene_code)
    print(len(gene_code_list))
    print(len(set(gene_code_list)))
    data['GENECODE'] = gene_code_list
    return data



if __name__ == '__main__':
    #subset = filter_data(open_tsv("results_new.tsv"))
    print(os.getcwd())
    subset = open_tsv("pythonScripts/ML data.txt")
    subset = getGenes(subset)
    write_tsv(subset, 'ML data fgenes.tsv')
