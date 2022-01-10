"""

"""

def results_table(results, variation_dict):
    chromosomes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
                   "12", "13", "14", "15", "16", "17", "18", "19", "20", "21",
                   "22", "X", "Y", "MT"]

    variation_length_dict = {}
    for i in chromosomes:
        try:
            variation_length_dict[i] = len(variation_dict[i]["POS"])
        except KeyError:
            variation_length_dict[i] = 0

    results_table_dict = {}
    for chrom in chromosomes:
        results_table_dict[chrom] = [variation_length_dict[chrom], 0, 0, 0, 0,
                                     0, 0, 0, 0]

    for result in results:
        if "Benign" in result["CLNSIG"] and "Likely" not in result["CLNSIG"]:
            results_table_dict[result["CHROM"]][1] += 1

        elif "Likely benign" in result["CLNSIG"]:
            results_table_dict[result["CHROM"]][2] += 1

        elif "Likely pathogenic" in result["CLNSIG"]:
            results_table_dict[result["CHROM"]][3] += 1

        elif "Pathogenic" in result["CLNSIG"] and "Likely" not in result[
            "CLNSIG"] and "Conflicting" not in result["CLNSIG"]:
            results_table_dict[result["CHROM"]][4] += 1

        else:
            results_table_dict[result["CHROM"]][7] += 1

            if any(CLNSIG in result["CLNSIG"].lower() for CLNSIG in
                   ["uncertain significance", "not provided", "nan"]):
                results_table_dict[result["CHROM"]][8] += 1
                if result["ML prediction"] == "1":
                    results_table_dict[result["CHROM"]][5] += 1

                elif result["ML prediction"] == "0":
                    results_table_dict[result["CHROM"]][6] += 1

    return results_table_dict