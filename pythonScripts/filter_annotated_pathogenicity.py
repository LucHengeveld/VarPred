from matplotlib.pyplot import get_current_fig_manager
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import os
from chrom_dict import chromosome_length


def open_tsv(location):
    return pd.read_csv(location, sep="\t")


def filter_data(data):
    # return data[((data.CLNREVSTAT == "reviewed by expert panel") |
    #              (data.CLNREVSTAT == "practice guideline") |
    #              (data.CHROM == "Y")) &
    #             (data.CLNSIG != "Uncertain significance") &
    #             (data.AF_ESP.isnan())]
    bad = [976754, 974718, 983388, 978267, 977757, 974724, 974730, 974732,
           974737, 974740, 974741, 983494, 974742, 974714, 974715]

    return data[~data.ID.isin(bad)]


def write_tsv(data, name):
    data.to_csv(name, sep="\t", index=False)


def scale_pos(data):
    pos_list = data['POS'].tolist()
    chrom_list = data['CHROM'].tolist()
    scaled_pos_list = []
    for i in range(len(pos_list)):
        chrom_length = chromosome_length[str(chrom_list[i])]
        scaled_pos = pos_list[i] / chrom_length
        scaled_pos_list.append(round(scaled_pos, 8))
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
    mutation_types = list(set(data[column].tolist()))
    mutation_types.sort()
    ohe = pd.get_dummies(data[column], prefix=column)
    for mutation_type in mutation_types:
        col = column + "_" + str(mutation_type)
        data[col] = ohe[col]
    return data


def clin_sig(data):
    types = ["Benign", "Likely benign", "Likely pathogenic", "Pathogenic"]
    data.reset_index()
    # data = data.loc[data["CLNSIG"].isin(types)]
    sig_list = data['CLNSIG']
    numerical_sig_list = []
    for sig in sig_list:
        try:
            sig = str(sig)
            if sig.lower().endswith("pathogenic"):
                sig_num = 1
            elif sig.lower().endswith("benign"):
                sig_num = 0
            else:
                sig_num = ""
            numerical_sig_list.append(sig_num)
        except ValueError:
            numerical_sig_list.append("")
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
    dataset = scale_pos(dataset)
    dataset = clin_sig(dataset)
    dataset = getGenes(dataset)
    dataset = get_first_value(dataset, "MC")
    dataset = data_aanpassen(dataset)
    dataset = one_hot_encoding(dataset, "CLNVC")
    dataset = one_hot_encoding(dataset, "MC")
    dataset = one_hot_encoding(dataset, "CHROM")

    # dataset = one_hot_encoding(dataset, "GENECODE")
    dataset = filter_data(dataset)
    write_tsv(dataset, "testbestand.tsv")
