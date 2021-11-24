from matplotlib.pyplot import get_current_fig_manager
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import os
from chrom_dict import chromosome_length


def open_tsv(location):
    return pd.read_csv(location, sep="\t")


def filter_data(data):
    return data[((data.CLNREVSTAT == "reviewed by expert panel") |
                 (data.CLNREVSTAT == "practice guideline") |
                 (data.CHROM == "Y")) &
                (data.CLNSIG != "Uncertain significance")]


def write_tsv(data, name):
    data.to_csv(name, sep="\t", index=False)


def scale_pos(data):
    pos_list = data['POS'].tolist()
    chrom_list = data['CHROM'].tolist()
    scaled_pos_list = []
    for i in range(len(pos_list)):
        chrom_length = chromosome_length[str(chrom_list[i])]
        scaled_pos = chrom_length / pos_list[i]
        scaled_pos_list.append(round(scaled_pos, 4))
    data['SC_POS'] = scaled_pos_list
    return data


def getGenes(data):
    gene_list = data['GENEINFO']
    gene_code_list = []
    for gene in gene_list:
        gene_code = str(gene).split(':')[0]
        gene_code_list.append(gene_code)
    data['GENECODE'] = gene_code_list
    return data


def one_hot_encoding(data, column):
    data[column] = data[column].astype(str)
    mutation_types = set(data[column].tolist())
    ohe = pd.get_dummies(data[column], prefix=column)
    for mutation_type in mutation_types:
        col = column + "_" + str(mutation_type)
        data[col] = ohe[col]
    return data


def clin_sig(data):
    types = ["Benign", "Likely benign", "Likely pathogenic", "Pathogenic"]
    data.reset_index()
    data = data.loc[data["CLNSIG"].isin(types)]
    sig_list = data['CLNSIG']
    numerical_sig_list = []
    for sig in sig_list:
        sig_num = types.index(sig)
        if sig_num in [0,1]:
            sig_num = 0
        elif sig_num in [2,3]:
            sig_num = 1
        numerical_sig_list.append(sig_num)
    data['CLNSIG NUM'] = numerical_sig_list
    return data


def data_aanpassen(data):
    columns = ["AF_ESP", "AF_EXAC", "AF_TGP", "RS"]
    for column in columns:
        temp = list()
        col = data[column].isnull()
        for cell in col:
            if cell:
                temp.append(0)
            else:
                temp.append(1)
        data[column] = temp
    return data


def get_first_value(data, column):
    items = list()
    for item in data[column]:
        item = str(item)
        items.append(item.split(",")[0][(item.find("|") + 1):])
    data[column] = items
    return data


if __name__ == '__main__':
    dataset = open_tsv("results_new.tsv")

    # dataset = filter_data(dataset)
    # subset = open_tsv("pythonScripts/ML data.txt")
    subset = scale_pos(dataset)
    subset = clin_sig(subset)
    subset = getGenes(subset)
    subset = get_first_value(subset, "MC")
    subset = data_aanpassen(subset)
    subset = one_hot_encoding(subset, "CLNVC")
    subset = one_hot_encoding(subset, "MC")
    subset = one_hot_encoding(subset, "CHROM")
    #subset = one_hot_encoding(subset, "GENECODE")
    write_tsv(subset, "ML data.tsv")
