"""
This module creates a 2D list with all the chromosomes, positions, ref and alt
variants and compares it to the Mongo database. The simularities are saved to
a list.
"""

import pymongo
from flask import request


def create_compare_list(vcf_list):
    """
    This functions retrieves all chromosome numbers and positions from the
    entered vcf file and adds it to a list.
    :param vcf_list: List with the structure [CHROM, POS, ID, REF, ALT],
        Might have extra columns added like QUAL, FILTER, INFO depending on the
        entered vcf file.
    :return: compare_list: List with the structure [chrom_list, pos_list,
    ref_list, alt_list]
    """
    # Creates empty lists
    chrom_list = []
    pos_list = []
    ref_list = []
    alt_list = []

    # Loops through the vcf_list and saves the chromosome numbers and
    # positions to a 2D list with the structure [chrom_list, pos_list,
    # ref_list, alt_list]
    for i in vcf_list:
        chrom_list.append(i[0])
        pos_list.append(i[1])
        ref_list.append(i[3])
        alt_list.append(i[4])
    compare_list = [chrom_list, pos_list, ref_list, alt_list]

    # Returns the compare_list
    return compare_list


def compare_dataset(compare_list):
    """
    Compares the compare_list to the variants in the database.
    :param compare_list: List with all the chromosome numbers and positions out
        of the vcf_list
    :return results: List with data of the found variants
    :return reference_build: The selected reference build from the
        webapplication
    """

    # Retrieves the selected reference build from the webapplication
    reference_build = request.form.get("reference_selector")

    # Connects to the local database
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["varpred"]

    # Uses the selected reference build as collection
    if reference_build == "37":
        col = db["variants-37"]
    else:
        col = db["variants-38"]

    # Create an empty list
    results = []

    # Loops through all the variants
    for i in range(len(compare_list[0])):

        # Adds the found simularities to the results list
        for simularity in col.find({"$and": [{"CHROM": compare_list[0][i]},
                                             {"POS": compare_list[1][i]},
                                             {"REF": compare_list[2][i]},
                                             {"ALT": compare_list[3][i]}]},
                                   {"_id": 0}):
            results.append(simularity)

    # Returns the results list and the selected reference build
    return results, reference_build
