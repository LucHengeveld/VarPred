import vcf
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
from textwrap import wrap


def read():
    """
    Parser for the clinvar vcf file
    :return: A dictoinary of the vcf file with the ID as key
    """

    # list with the column names
    column_list = ["AF_ESP", "AF_EXAC", "AF_TGP", "ALLELEID", "CLNDN",
                   "CLNDNINCL", "CLNDISDB", "CLNDISDBINCL", "CLNHGVS",
                   "CLNREVSTAT", "CLNSIG", "CLNSIGCONF", "CLNSIGINCL", "CLNVC",
                   "CLNVCSO", "CLNVI", "DBVARID", "GENEINFO", "MC", "ORIGIN",
                   "RS", "SSR"]

    # create dictionary
    file_dictionary = dict()

    # open file
    file = vcf.Reader(open("clinvar.vcf"))

    # add entries to dictionary
    for entry in file:
        file_dictionary[int(entry.ID)] = list()
        file_dictionary[int(entry.ID)].extend([entry.CHROM, entry.POS,
                                               entry.REF, entry.ALT])
        for column in column_list:
            try:
                file_dictionary[int(entry.ID)].append(entry.INFO[column])
            except KeyError:
                file_dictionary[int(entry.ID)].append("N/A")
    pickle.dump(file_dictionary, open("file_dictionary.p", "wb"))
    return file_dictionary


def write_csv(file_dictionary):
    with open("results.tsv", "w") as file:
        column_list = ["ID", "CHROM", "POS", "REF", "ALT", "AF_ESP", "AF_EXAC",
                       "AF_TGP", "ALLELEID", "CLNDN", "CLNDNINCL", "CLNDISDB",
                       "CLNDISDBINCL", "CLNHGVS", "CLNREVSTAT", "CLNSIG",
                       "CLNSIGCONF", "CLNSIGINCL", "CLNVC", "CLNVCSO", "CLNVI",
                       "DBVARID", "GENEINFO", "MC", "ORIGIN", "RS", "SSR"]
        for value in column_list:
            file.write(f"{value}\t")
        file.write("\n")
        for key in file_dictionary.keys():
            file.write(f"{key}\t")
            for value in file_dictionary[key]:
                file.write(f"{value}\t")
            file.write("\n")
    file.close()


def count_illness(data_dictionary):
    illnesses = dict()
    print("Counting illnesses...")
    for value in data_dictionary.values():
        for illness in value[8]:
            try:
                illnesses[illness.split("|")[0]] += 1
            except KeyError:
                illnesses[illness.split("|")[0]] = 1
    illnesses = sorted(illnesses.items(), key=lambda x: x[1], reverse=True)
    # print(illnesses)
    print("Writing ilnesses to file...")
    with open("illnesses.txt", "w") as file:
        for value in illnesses:
            file.write(f"{value[0]}\t{value[1]}\n")
    # print(illnesses)


def plot_illness(number_of_rows):
    values = [206882, 38576, 13209, 10619, 9489]
    labels = ["not_provided", "Hereditary_cancer-predisposing_syndrome",
              "Hereditary_breast_and_ovarian_cancer_syndrome",
              "Cardiomyopathy", "Fanconi_anemia"]
    percent = list()

    for value in values:
        percent.append(value / number_of_rows * 100)

    patches, text = plt.pie(values, startangle=90, counterclock=0,
                            center=(0, -5))

    extended_labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in
                       zip(labels, percent)]

    patches, extended_labels, dummy = zip(
        *sorted(zip(patches, extended_labels, values),
                key=lambda x: x[2], reverse=True))
    plt.legend(patches, extended_labels, loc='center left',
               bbox_to_anchor=(-0.1, 1.), fontsize=8)
    plt.show()


def get_omim_name(data_dictionary):
    df = pd.read_csv('OMIM_names.txt', sep='\t')

    print(df)
    # omim_dict = zip(df.)


def chrom_and_pathogenicity(data_dictionary):
    chromosomes = dict()
    for entry in data_dictionary.keys():
        chromosome = data_dictionary[entry][0]
        pathogenicity = data_dictionary[entry][14][0]
        try:
            dictionary = chromosomes[chromosome]
            try:
                dictionary[pathogenicity] += 1
            except KeyError:
                dictionary[pathogenicity] = 1
        except KeyError:
            chromosomes[chromosome] = dict()
            chromosomes[chromosome][pathogenicity] = 1
    for chromosome in chromosomes.keys():
        dictionary = chromosomes[chromosome]
        dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1],
                                 reverse=True))
        chromosomes[chromosome] = dictionary
        bar_chart(dictionary, chromosome)


def bar_chart(dictionary, chrom):
    dir_ = os.getcwd()
    os.chdir(f"{dir_}\\plots")
    plt.figure(figsize=[10, 15])
    x_values = list()
    for key in dictionary.keys():
        x_values.append("\n".join(wrap(key.replace("_", " "), 20)))
    y_values = list()
    for value in dictionary.values():
        y_values.append(value / sum(dictionary.values()) * 100)
    plt.bar(x_values, y_values)
    plt.xticks(rotation=90)
    plt.title(f"Chromosome {chrom}")
    plt.savefig(f"{chrom}.png", format="png")
    plt.close()
    os.chdir(dir_)


def analysis(data_dictionary):
    # count_illness(data_dictionary)
    plot_illness(len(data_dictionary.keys()))
    # get_omim_name(data_dictionary)
    chrom_and_pathogenicity(data_dictionary)


if __name__ == '__main__':
    if not os.path.exists(f"{os.getcwd()}/plots"):
        os.mkdir("plots")
    if os.path.isfile("file_dictionary.p"):
        print("Pickle found, loading pickle...")
        fd = pickle.load(open("file_dictionary.p", "rb"))
        print("Pickle parsed and loaded...")
    else:
        print("No pickle found, parsing data...")
        fd = read()
    #  write_csv(fd)
    analysis(fd)
