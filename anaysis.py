import vcf
import pandas as pd
import pickle
import os


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

def get_OMIM_name(data_dictionary):
    df = pd.read_csv('OMIM_names.txt')
    print(df["MIM Number"])
    keys_list = df["MIM Number"]
    values_list = df["Preferred Title; symbol"]
    zip_iterator = zip(keys_list, values_list)
    a_dictionary = dict(zip_iterator)
 
    for entry in data_dictionary:
        id_column = data_dictionary[entry][10]
        for id in id_column:
            if id is not None and "OMIM" in id:
                omim_str = id.split('|')[0]
                omim_id = omim_str.replace("OMIM:", "")
                try:
                    dname = a_dictionary[omim_id]
                except KeyError:
                    dname = 'N/A'
            else:
                dname = 'N/A'
        data_dictionary[entry].append(dname)
        
    return data_dictionary
            
            


def analysis(data_dictionary):
    count_illness(data_dictionary)
    #get_OMIM_name(data_dictionary)


if __name__ == '__main__':
    if os.path.isfile("file_dictionary.p"):
        print("yup")
        fd = pickle.load(open("file_dictionary.p", "rb"))
    else:
        fd = read()

    fd = get_OMIM_name(fd)
    
    #write_csv(fd)
    #analysis(fd)
