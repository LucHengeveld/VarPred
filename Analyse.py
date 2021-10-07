import vcf


def read_file():
    column_list = ["AF_ESP", "AF_EXAC", "AF_TGP", "ALLELEID", "CLNDN",
                   "CLNDNINCL", "CLNDISDB", "CLNDISDBINCL", "CLNHGVS",
                   "CLNREVSTAT", "CLNSIG", "CLNSIGCONF", "CLNSIGINCL", "CLNVC",
                   "CLNVCSO", "CLNVI", "DBVARID", "GENEINFO", "MC", "ORIGIN",
                   "RS", "SSR"]
    file_dictionary = dict()
    file = vcf.Reader(open("clinvar.vcf"))
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


def main():
    file_dictionary = read_file()


main()
