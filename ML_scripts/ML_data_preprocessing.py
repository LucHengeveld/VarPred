import pandas as pd
import os
import warnings


def open_tsv(location):
    """Parses a .tsv file into a pandas dataframe.

    Args:
        location: String with location/filename of the .tsv file.

    Returns:
        Dataframe of the .tsv file.
    """
    return pd.read_csv(location, sep="\t")


def filter_data(data):
    """Filters the best annotated ClinVar entries fror training the
     ML model.

    Args:
        data: Dataframe containing all the ClinVar data.

    Returns:
        Filtered dataframe.
    """
    types = ["Benign", "Likely benign", "Likely pathogenic", "Pathogenic"]
    data = data.loc[data["CLNSIG"].isin(types)]
    return data[((data.CLNREVSTAT == "reviewed by expert panel") |
                 (data.CLNREVSTAT == "practice guideline") |
                 (data.CHROM == "Y")) &
                (data.CLNSIG != "Uncertain significance")]


def write_tsv(data, name):
    """Creates a .tsv file from a dataframe.

    Args:
        data: Dataframe that gets written to file.
        name: String with the filename.
    """
    data.to_csv(name, sep="\t", index=False)


def scale_pos(data):
    """Adds a column containing the relative positions of the variant to
    the dataframe.

    Args:
        data: Dataframe without the realtive position of the variant
              added.

    Returns:
        Dataframe with the relative position of the variant added.
    """
    pos_list = data['POS'].tolist()
    chrom_list = data['CHROM'].tolist()
    scaled_pos_list = []
    for i in range(len(pos_list)):
        if str(chrom_list[i]) == 'NW 009646201.1':
            chrom_list[i] = 9
        chrom_length = chromosome_length[str(chrom_list[i])]
        scaled_pos = pos_list[i] / chrom_length
        scaled_pos_list.append(round(scaled_pos, 8))
    data['SC_POS'] = scaled_pos_list
    return data


def getGenes(data):
    """Gets the gene codes from the 'GENEINFO' column and adds them to
    the new 'GENECODE' column.

    Args:
        data: Dataframe containing all the ClinVar data.

    Returns:
        Dataframe containing all the ClinVar data with an extra column
        for the 'GENECODE'.
    """
    gene_list = data['GENEINFO']
    gene_code_list = []
    for gene in gene_list:
        gene_code = str(gene).split(':')[0]
        gene_code_list.append(gene_code)
    data['GENECODE'] = gene_code_list
    return data


def one_hot_encoding(data, column):
    """One hot encodes a specific column in a dataframe.

    Args:
        data: Dataframe object.
        column: String name of the column that gets one hot encoded.

    Returns:
        Dataframe object with extra columns for the one hot encoding.
    """
    data[column] = data[column].astype(str)
    mutation_types = list(set(data[column].tolist()))
    mutation_types.sort()
    ohe = pd.get_dummies(data[column], prefix=column)
    for mutation_type in mutation_types:
        col = column + "_" + str(mutation_type)
        data[col] = ohe[col]
    return data


def clin_sig(data):
    """Adds a column with to the dataframe with two groups;
    group 1: Benign and Likely benign variants,
    group 0: Pathogenic and Likely pathogenic variants.

    Args:
        data: Dataframe containing all the ClinVar data.

    Returns:
        Dataframe including classification in the two groups
    """

    data.reset_index()
    #
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


def clin_sig_pathogenic(data):
    """Adds a column with to the dataframe with two groups;
        group 1: Pathogenic variants,
        group 0: Likely pathogenic variants.

        Args:
            data: Dataframe containing all the ClinVar data.

        Returns:
            Dataframe including classification in the two groups
    """
    types = ["Likely pathogenic", "Pathogenic"]
    data.reset_index()
    data = data.loc[data["CLNSIG"].isin(types)]
    sig_list = data['CLNSIG']
    numerical_sig_list = []
    for sig in sig_list:
        try:
            sig = str(sig)
            if sig.lower() == "pathogenic":
                sig_num = 1
            elif sig.lower() == "likely pathogenic":
                sig_num = 0
            else:
                sig_num = ""
            numerical_sig_list.append(sig_num)
        except ValueError:
            numerical_sig_list.append("")
    data['CLNSIG NUM'] = numerical_sig_list
    return data


def clin_sig_benign(data):
    """Adds a column with to the dataframe with two groups;
        group 1: Benign variants,
        group 0: Likely benign variants.

        Args:
            data: Dataframe containing all the ClinVar data.

        Returns:
            Dataframe including classification in the two groups
    """
    types = ["Likely benign", "Benign"]
    data.reset_index()
    data = data.loc[data["CLNSIG"].isin(types)]
    sig_list = data['CLNSIG']
    numerical_sig_list = []
    for sig in sig_list:
        try:
            sig = str(sig)
            if sig.lower() == "benign":
                sig_num = 1
            elif sig.lower() == "likely benign":
                sig_num = 0
            else:
                sig_num = ""
            numerical_sig_list.append(sig_num)
        except ValueError:
            numerical_sig_list.append("")
    data['CLNSIG NUM'] = numerical_sig_list
    return data


def data_aanpassen(data):
    """Changes the data in the columns 'AF_ESP', 'AF_EXAC', 'AF_TGP' and
    'RS' by classifying them into 2 groups per column:
    group 0: data is null;
    group 1: data isn't null.

    Args:
        data: Dataframe containing all the ClinVar data.

    Returns:
        Dataframe with classifications into the two groups for columns
        'AF_ESP', 'AF_EXAC', 'AF_TGP' and 'RS'.
    """
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
    """Gets the first value from all the cells withing a column.

    Args:
        data: Dataframe containing all the ClinVar data.
        column: String with column name whose first values you want to
                select.

    Returns:
        Dataframe with just the first value in the cells for the
        selected column
    """
    items = list()
    for item in data[column]:
        item = str(item)
        items.append(item.split(",")[0][(item.find("|") + 1):])
    data[column] = items
    return data


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    warnings.simplefilter(action="ignore", category=FutureWarning)
    if str(os.environ["assembly"]) == "37":
        from chrom_dict_37 import chromosome_length
    else:
        from chrom_dict_38 import chromosome_length
    print("Preprocessing ML data...")
    dataset = open_tsv("results_new.tsv")
    dataset = scale_pos(dataset)
    dataset = clin_sig(dataset)
    dataset = getGenes(dataset)
    dataset = get_first_value(dataset, "MC")
    dataset = data_aanpassen(dataset)
    dataset = one_hot_encoding(dataset, "CLNVC")
    dataset = one_hot_encoding(dataset, "MC")
    dataset = one_hot_encoding(dataset, "CHROM")

    # dataset = one_hot_encoding(dataset, "GENECO  DE")
    os.remove("results_new.tsv")
    write_tsv(dataset, "OHE_ClinVar_data.tsv")
    dataset = filter_data(dataset)
    write_tsv(dataset, "ML_data.tsv")
    print("ML data preprocessed successfully!")
    print("-----------------------------------------------------------")
