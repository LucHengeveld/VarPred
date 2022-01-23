import json
import gene
import medgen
import pandas as pd
import change_clinvar_file.clinvar_vcf_parser
import sys


def read_tsv(location):
    """ Parses a .tsv file into a pandas dataframe.

    Args:
        location: String with location/filename of the .tsv file.

    Returns:
        Dataframe of the .tsv file.
    """
    return pd.read_csv(location, sep="\t")


def clnvcso(data, dict_so_description):
    """ Gets all the unique clnvcso id's in the Clinvar file.

    Args:
        data: Dataframe containing all the ClinVar data.
        dict_so_description: Dictionary containing gene ontology data.

    Returns:
        results: List containing all unique gene ontology data of the clnvcso colomn.
    """
    unique_ids = []
    results = []
    tmp_dict = {}

    for item in data.CLNVCSO:
        if item not in unique_ids:
            unique_ids.append(item)
            tmp_dict['id'] = item
            tmp_dict['description'] = dict_so_description[item]
            results.append(tmp_dict)
            tmp_dict = {}

    return results


def so_description():
    """ Read a gene ontology file and creating a dictionary containing gene ontology data.

    Returns:
        dict_so_description: Dictionary containg all gene ontology data.
    """
    dict_so_description = {}

    file = open("so_beschrijvingen.txt")
    for line in file:
        line = line.split(":")
        dict_so_description[line[0] + ":" + line[1]] = line[2].replace("\n", "")

    return dict_so_description


def gene_results(data):
    """ Gets results of the NCBI gene page for all unique gene id's in the Clinvar file.

    Args:
        data: Dataframe containing all the ClinVar data.

    Returns:
        results: List containing all gene results.
    """
    unique_ids = []
    results = []

    for item in data.GENEINFO:
        if str(item) != 'nan':
            result = item.split("|")
            for result_variant in result:
                gene_id = result_variant.split(":")[1]  # Location of the gene id
                if gene_id not in unique_ids:
                    unique_ids.append(gene_id)
                    result = gene.gene_info(gene_id)
                    results.append(result)

    return results


def medgen_results(data):
    """ Gets results of the NCBI MedGen page for all unique medgen id's in the Clinvar file.

    Args:
        data: Dataframe containing all the ClinVar data.

    Returns:
        results: List containing all medgen results.
    """
    unique_ids = []
    results = []

    for item in data.CLNDISDB:
        if str(item) != 'nan':
            result = item.split("|")
            for result_variant in result:
                ids = result_variant.split(",")
                for id_variant in ids:      # One variant can contain multiple medgen id's
                    if "MedGen" in id_variant:
                        medgen_id = id_variant.split(":")[1]    # Location of the Medgen ID
                        if medgen_id not in unique_ids:
                            unique_ids.append(medgen_id)
                            result = medgen.medgen_info(medgen_id)
                            results.append(result)

    return results


def write_results_to_json(result, name_file):
    """ Writes a list into a JSON format.

    Args:
        result: List containg results.
        name_file: Name for the file without .json.

    """
    with open(f"{name_file}.json", "w") as outfile:
        json.dump(result, outfile, indent=4)


if __name__ == '__main__':
    file_location = sys.argv[1]                 # Location clinvar file
    print("Start ClinVar parsing")
    change_clinvar_file.clinvar_vcf_parser.clinvar_parser(file_location)
    data_clinvar = read_tsv("change_clinvar_file/results_new.tsv")
    print("End ClinVar parsing")
    print("Start clnvcso information")
    dict_so_description = so_description()
    results_clnvsco = clnvcso(data_clinvar, dict_so_description)
    write_results_to_json(results_clnvsco, 'clnvcso')
    print("End clnvcso information")

    print("Start scraping Gene ID's")
    results_genes = gene_results(data_clinvar)
    print("Scraping of Gene ID's successfully")
    write_results_to_json(results_genes, 'gene')
    print("Start scraping MedGen ID's")
    results_medgen = medgen_results(data_clinvar)
    print("Scraping of MedGen ID's successfully")
    write_results_to_json(results_medgen, 'medgen')

    print("Webscrapping successfully")



    # gene_result = test()
    # write_results_to_json(gene_result, 'gene_update')
    # print("Start gene id's ophalen")
    # result = gene_results(data)
    # print("Gene id's zijn opgehaald")
    # print("Wegschrijven naar json")
    # write_results_to_json(result, 'gene')
    # print("Weggeschreven naar json")
    # print("Deze id's zijn mis gegaan")
    # tmp.append("Test")
    # print(tmp)
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # print("Current Time =", current_time)
