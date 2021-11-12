from matplotlib.pyplot import get_current_fig_manager
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
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


def one_hot_encoding(data, column):
    mutation_types = set(data[column].tolist())
    ohe = pd.get_dummies(data[column], prefix=column)
    for mutation_type in mutation_types:
        col = column + "_" + mutation_type
        data[col] = ohe[col]
    return data


def data_aanpassen(data):
    print(data.AF_ESP)
    columns = ["AF_ESP", "AF_EXAC", "AF_TGP", "RS"]
    for column in columns:
        temp = list()
        col = data[column].isnull()
        print(col)
        for cell in col:
            if cell:
                temp.append(0)
            else:
                temp.append(1)
        data[column] = temp
    return data


if __name__ == '__main__':
    subset = filter_data(open_tsv("results_new.tsv"))
    # subset = open_tsv("pythonScripts/ML data.txt")
    subset = getGenes(subset)
    subset = data_aanpassen(subset)
    subset = one_hot_encoding(subset, "CLNVC")
    write_tsv(subset, "ML data.tsv")
