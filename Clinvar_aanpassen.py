import os
import pickle
import pandas as pd
import vcf


def read_file():
    column_list = ["AF_ESP", "AF_EXAC", "AF_TGP", "ALLELEID", "CLNDN",
                   "CLNDNINCL", "CLNDISDB", "CLNDISDBINCL", "CLNHGVS",
                   "CLNREVSTAT", "CLNSIG", "CLNSIGCONF", "CLNSIGINCL", "CLNVC",
                   "CLNVCSO", "CLNVI", "DBVARID", "GENEINFO", "MC", "ORIGIN",
                   "RS", "SSR", "OMIM"]
    file_dictionary = dict()
    file = vcf.Reader(open("clinvar.vcf"))

    for entry in file:
        file_dictionary[int(entry.ID)] = list()
        file_dictionary[int(entry.ID)].extend([entry.CHROM, entry.POS, entry.REF, entry.ALT])
        for column in column_list:
            try:
                file_dictionary[int(entry.ID)].append(entry.INFO[column])
            except KeyError:
                file_dictionary[int(entry.ID)].append("N/A")

    pickle.dump(file_dictionary, open("file_dictionary.p", "wb"))
    return file_dictionary


def change_dict(file_dictionary):
    for key, value in file_dictionary.items():
        clinical = ""
        clinical2 = ""
        disease = ""
        medgen = ""
        so = ""
        value[3] = value[3][0]
        for item in value[8]:
            disease = disease + "," + item.replace("_", " ")
            disease = disease.lstrip()
            disease = disease.lstrip(",")
        value[8] = disease
        for item in value[10]:
            medgen = medgen + "," + str(item)
            medgen = medgen.lstrip()
            medgen = medgen.lstrip(",")
        value[10] = medgen
        value[12] = value[12][0]
        for item in value[13]:
            clinical = clinical + item.replace("_", " ")
            clinical = clinical.lstrip()
        value[13] = clinical
        for item in value[14]:
            clinical2 = clinical2 + "," + item.replace("_", " ")
            clinical2 = clinical2.lstrip()
            clinical2 = clinical2.lstrip(",")
        value[14] = clinical2
        for item in value[22]:
            so = so + "," + item
            so = so.lstrip()
            so = so.lstrip(",")
        value[22] = so
        if len(value[23]) == 1:
            value[23] = value[23][0]
        if len(value[24]) == 1:
            value[24] = value[24][0]

        file_dictionary[key] = value

    return file_dictionary


def write_file(file_dictionary):
    with open("results_new.tsv", "w") as file:
        column_list = ["ID", "CHROM", "POS", "REF", "ALT", "AF_ESP", "AF_EXAC",
                       "AF_TGP", "ALLELEID", "CLNDN", "CLNDNINCL", "CLNDISDB",
                       "CLNDISDBINCL", "CLNHGVS", "CLNREVSTAT", "CLNSIG",
                       "CLNSIGCONF", "CLNSIGINCL", "CLNVC", "CLNVCSO", "CLNVI",
                       "DBVARID", "GENEINFO", "MC", "ORIGIN", "RS", "SSR", "OMIM"]
        for value in column_list:
            file.write(f"{value}\t")
        file.write("\n")
        for key in file_dictionary.keys():
            file.write(f"{key}\t")
            for value in file_dictionary[key]:
                file.write(f"{value}\t")
            file.write("\n")
    file.close()


if __name__ == '__main__':
    if os.path.isfile("file_dictionary.p"):
        print("Pickle found, loading pickle...")
        fd = pickle.load(open("file_dictionary.p", "rb"))
        print("Pickle parsed and loaded...")
    else:
        print("No pickle found, parsing data...")
        fd = read_file()
    file_dictionary = change_dict(fd)
    print(file_dictionary.get(899438))
    # write_file(file_dictionary)
