import os
import pickle
import vcf


def read_file():
    """Opens and parses a ClinVar .vcf file and converts it to a dictionary;
    this dictionary is pickled and returned.

    Returns:
        Dictionary of a ClinVar .vcf file
    """
    # read file
    column_list = ["AF_ESP", "AF_EXAC", "AF_TGP", "ALLELEID", "CLNDN",
                   "CLNDNINCL", "CLNDISDB", "CLNDISDBINCL", "CLNHGVS",
                   "CLNREVSTAT", "CLNSIG", "CLNSIGCONF", "CLNSIGINCL", "CLNVC",
                   "CLNVCSO", "CLNVI", "DBVARID", "GENEINFO", "MC", "ORIGIN",
                   "RS", "SSR"]
    file = vcf.Reader(open("clinvar.vcf"))

    # convert to dictionary
    file_dictionary = dict()
    for entry in file:
        file_dictionary[int(entry.ID)] = list()
        file_dictionary[int(entry.ID)].extend([entry.CHROM, entry.POS,
                                               entry.REF, entry.ALT])
        for column in column_list:
            try:
                file_dictionary[int(entry.ID)].append(entry.INFO[column])
            except KeyError:
                file_dictionary[int(entry.ID)].append("N/A")

    # pickle dictionary
    pickle.dump(file_dictionary, open("file_dictionary.p", "wb"))

    return file_dictionary


def change_dict(file_dictionary):
    """Iterates over the ClinVar dictionary and formats cells to a
    standard.

    Args:
        file_dictionary: Dictionary of the ClinVar file.

    Returns:
        Organised dictionary of the ClinVar file.
    """

    for key, value in file_dictionary.items():
        for i in range(len(value)):

            # if the value in the cell is a list, this list is removed.
            if isinstance(value[i], list):
                temp = ""
                for cell in value[i]:
                    temp = temp + "," + str(cell)
                    temp = temp.lstrip("_")
                    temp = temp.replace("_", " ")
                    temp = temp.rstrip("_")
                value[i] = temp.lstrip(",")

            # if the value in the cell is a string, it is manipulated
            # to a new standard.
            elif isinstance(value[i], str):

                value[i] = value[i].lstrip("_")
                value[i] = value[i].replace("_", " ")
                value[i] = value[i].rstrip("_")

        # ref length appended to the end
        reflen = len(value[2])
        value.append(reflen)

        # alt length appended to the end
        altlen = len(value[3])
        value.append(altlen)
        value.append((reflen - altlen))
        file_dictionary[key] = value

    return file_dictionary


def write_file(file_dictionary):
    """Writes the ClinVar dictionary to a .tsv file.

    Args:
        file_dictionary: Dictionary of the ClinVar file.
    """

    # write to temporary file
    with open("results.temp", "w") as file:
        column_list = ["ID", "CHROM", "POS", "REF", "ALT", "AF_ESP", "AF_EXAC",
                       "AF_TGP", "ALLELEID", "CLNDN", "CLNDNINCL", "CLNDISDB",
                       "CLNDISDBINCL", "CLNHGVS", "CLNREVSTAT", "CLNSIG",
                       "CLNSIGCONF", "CLNSIGINCL", "CLNVC", "CLNVCSO", "CLNVI",
                       "DBVARID", "GENEINFO", "MC", "ORIGIN", "RS", "SSR",
                       "REF LENGTH", "ALT LENGTH",
                       "DIFFERENCE REF AND ALT LENGTH"]
        for value in column_list:
            file.write(f"{value}\t")
        file.write("\n")
        for key in file_dictionary.keys():
            file.write(f"{key}\t")
            for value in file_dictionary[key]:
                file.write(f"{value}\t")
            file.write("\n")

    # convert temporary file to final file
    with open("results.temp", "r") as file1:
        with open("results_new.tsv", "w") as file2:
            for line in file1:
                file2.write(line.replace("\t\n", "\n"))
    os.remove("results.temp")


if __name__ == '__main__':
    if os.path.isfile("file_dictionary.p"):
        print("Pickle found, loading pickle...")
        fd = pickle.load(open("file_dictionary.p", "rb"))
        print("Pickle parsed and loaded...")
    else:
        print("No pickle found, parsing data...")
        fd = read_file()
    file_dictionary = change_dict(fd)
    os.remove('clinvar.vcf')
    write_file(file_dictionary)
