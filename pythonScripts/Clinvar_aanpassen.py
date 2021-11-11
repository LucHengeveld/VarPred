import os
import pickle
import pandas as pd
import vcf


def read_file():
    column_list = ["AF_ESP", "AF_EXAC", "AF_TGP", "ALLELEID", "CLNDN",
                   "CLNDNINCL", "CLNDISDB", "CLNDISDBINCL", "CLNHGVS",
                   "CLNREVSTAT", "CLNSIG", "CLNSIGCONF", "CLNSIGINCL", "CLNVC",
                   "CLNVCSO", "CLNVI", "DBVARID", "GENEINFO", "MC", "ORIGIN",
                   "RS", "SSR"]
    file_dictionary = dict()
    file = vcf.Reader(open("../clinvar.vcf"))

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
        for i in range(len(value)):
            if isinstance(value[i], list):
                temp = ""
                for cell in value[i]:
                    temp = temp + "," + str(cell)
                    temp = temp.lstrip("_")
                    temp = temp.replace("_", " ")
                    temp = temp.rstrip("_")
                value[i] = temp.lstrip(",")
            elif isinstance(value[i], str):
                value[i] = value[i].lstrip("_")
                value[i] = value[i].replace("_", " ")
                value[i] = value[i].rstrip("_")

        # ref length appended to the end
        value.append(len(value[2]))

        # alt length appended to the end
        value.append(len(value[3]))
        file_dictionary[key] = value

    return file_dictionary


def write_file(file_dictionary):
    with open("results_temp.tsv", "w") as file:
        column_list = ["ID", "CHROM", "POS", "REF", "ALT", "AF_ESP", "AF_EXAC",
                       "AF_TGP", "ALLELEID", "CLNDN", "CLNDNINCL", "CLNDISDB",
                       "CLNDISDBINCL", "CLNHGVS", "CLNREVSTAT", "CLNSIG",
                       "CLNSIGCONF", "CLNSIGINCL", "CLNVC", "CLNVCSO", "CLNVI",
                       "DBVARID", "GENEINFO", "MC", "ORIGIN", "RS", "SSR",
                       "REF LENGTH", "ALT LENGTH"]
        for value in column_list:
            file.write(f"{value}\t")
        file.write("\n")
        for key in file_dictionary.keys():
            file.write(f"{key}\t")
            for value in file_dictionary[key]:
                file.write(f"{value}\t")
            file.write("\n")
    with open("results_temp.tsv", "r") as file1:
        with open("results_new.tsv", "w") as file2:
            for line in file1:
                file2.write(line.replace("\t\n", "\n"))
    os.remove("results_temp.tsv")
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
    write_file(file_dictionary)
