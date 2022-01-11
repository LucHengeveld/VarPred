"""
This module creates the variables in the pathogenicity table for the
webapplication.
"""


def results_table(results, variant_dict):
    """
    Saves lists with the amount of variants per chromosome to a dictionary for
        the pathogenicity table.
    :param results: List with data of the found variants from the database
    :param variant_dict: Dictionary with the structure {Chromosome: {"POS":
        pos_list, "REF": ref_list, "ALT": alt_list, "REF_short": ref_short,
        "ALT_short": alt_short}.
    :return results_table_dict: Dictionary with the structure {Chromosome:
        [Total Benign variants, Total Likely benign variants, Total Likely
        pathogenic variants, Total Pathogenic variants, Total Predicted benign
        variants, Total Predicted Pathogenic variants, Total Other variants,
        Total predicted variants]}
    """

    # Creates a list with all the chromosomes
    chromosomes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
                   "12", "13", "14", "15", "16", "17", "18", "19", "20", "21",
                   "22", "X", "Y", "MT"]

    # Creates an empty dictionary
    variant_length_dict = {}

    # Loops through the chromosome list
    for i in chromosomes:
        # Counts the amount of variants per chromosome and adds it to a
        # a dictionary. If a chromosome has no variants it sets the
        # variable to 0
        try:
            variant_length_dict[i] = len(variant_dict[i]["POS"])
        except KeyError:
            variant_length_dict[i] = 0

    # Creates an empty dictionary
    results_table_dict = {}

    # Loops through the chromosome list
    for chrom in chromosomes:

        # Sets all counts except the total variants
        # (variant_length_dict[chrom]) to 0 and adds the counts to a
        # dictionary
        results_table_dict[chrom] = [variant_length_dict[chrom], 0, 0, 0, 0,
                                     0, 0, 0, 0]

    # Loops through the results
    for result in results:

        # Check if the clinical significance from a result is Benign,
        # Likely benign, Likely pathogenic, Pathogenic or something else
        # and adds 1 to the correct counter
        if "Benign" in result["CLNSIG"] and "Likely" not in result["CLNSIG"]:
            results_table_dict[result["CHROM"]][1] += 1

        elif "Likely benign" in result["CLNSIG"]:
            results_table_dict[result["CHROM"]][2] += 1

        elif "Likely pathogenic" in result["CLNSIG"]:
            results_table_dict[result["CHROM"]][3] += 1

        elif "Pathogenic" in result["CLNSIG"] and "Likely" not in \
                result["CLNSIG"] and "Conflicting" not in result["CLNSIG"]:
            results_table_dict[result["CHROM"]][4] += 1

        else:
            results_table_dict[result["CHROM"]][7] += 1

            # If the clinical significance has the value uncertain
            # significance, not provided or nan it adds 1 to the machine
            # learning prediction counter
            if any(CLNSIG in result["CLNSIG"].lower() for CLNSIG in
                   ["uncertain significance", "not provided", "nan"]):
                results_table_dict[result["CHROM"]][8] += 1
                if result["ML prediction"] == "1":
                    results_table_dict[result["CHROM"]][5] += 1

                elif result["ML prediction"] == "0":
                    results_table_dict[result["CHROM"]][6] += 1

    # Returns the result table dictionary
    return results_table_dict
