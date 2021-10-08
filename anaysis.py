import vcf


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


def count_illness(data_dictionary):
    illnesses = dict()
    for value in data_dictionary.values():
        for illness in value[8]:
            try:
                illnesses[illness.split("|")[0]] += 1
            except KeyError:
                illnesses[illness.split("|")[0]] = 1
    illnesses = sorted(illnesses.items(), key=lambda x: x[1], reverse=True)
    print(illnesses)


def analysis(data_dictionary):
    count_illness(data_dictionary)


if __name__ == '__main__':
    fd = read()
    # write_csv(fd)
    analysis(fd)
