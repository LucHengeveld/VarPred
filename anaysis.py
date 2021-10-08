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


if __name__ == '__main__':
    fd = read()
