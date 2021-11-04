import vcf
import matplotlib.pyplot as plt
from textwrap import wrap


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
        file_dictionary[int(entry.ID)].extend([entry.CHROM, entry.POS, entry.REF, entry.ALT])
        for column in column_list:
            try:
                file_dictionary[int(entry.ID)].append(entry.INFO[column])
            except KeyError:
                file_dictionary[int(entry.ID)].append("N/A")

    return file_dictionary


def chromosomes(file_dictionary):
    dict_chromosomes = {}
    for value in file_dictionary.values():
        # print(value)
        if value[0] in dict_chromosomes:
            value_ = dict_chromosomes.get(value[0])
            dict_chromosomes[value[0]] = value_ + 1
        else:
            dict_chromosomes[value[0]] = 1

    fig = plt.figure(figsize=[10, 10])
    plt.bar(dict_chromosomes.keys(), dict_chromosomes.values())
    plt.ylabel('Aantal')
    plt.title('Aantal varianten per allel frequencies')
    plt.xlabel("allel frequencies per database")
    plt.xticks(rotation=90)
    plt.show()


def af_colums(file_dictionary):
    dict_af = {"AF_ESP": 0, "AF_EXAC": 0, "AF_TGP": 0}
    for value in file_dictionary.values():
        if value[4] != "N/A":
            value_esp = dict_af.get("AF_ESP")
            dict_af["AF_ESP"] = value_esp + 1
        if value[5] != "N/A":
            value_exac = dict_af.get("AF_EXAC")
            dict_af["AF_EXAC"] = value_exac + 1
        if value[6] != "N/A":
            value_tgp = dict_af.get("AF_TGP")
            dict_af["AF_TGP"] = value_tgp + 1

    fig = plt.figure(figsize=[10, 10])
    plt.bar(dict_af.keys(), dict_af.values())
    plt.ylabel('Aantal')
    plt.title('Aantal varianten per chromosomes')
    plt.xlabel("Chromosoom nummer")
    plt.show()


def variant_type(file_dictionary):
    dict_variants = {"copy_number_gain": 0, "copy_number_loss": 0, "Deletion": 0, "Duplication": 0, "Indel": 0,
                     "Insertion": 0, "Inversion": 0, "Microsatellite": 0, "single_nucleotide_variant": 0, "Variation": 0}

    list_variants = ["copy_number_gain", "copy_number_loss", "Deletion", "Duplication", "Indel", "Insertion", "Inversion", "Microsatellite",
                     "single_nucleotide_variant", "Variation"]

    for value in file_dictionary.values():
        for item in list_variants:
            if value[17] == item:
                value_ = dict_variants.get(value[17])
                dict_variants[value[17]] = value_ + 1

    fig = plt.figure(figsize=[10, 10])
    wrapped_label = []
    value_variant = []
    for key, value in dict_variants.items():
        label = '\n'.join(wrap(key.replace("_", " "), 20))
        wrapped_label.append(label)
        value_variant.append(value)
    plt.bar(wrapped_label, value_variant)
    plt.ylabel('Aantal')
    plt.title('Aantal varianten per variant type')
    plt.xlabel("Variant types")
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.15)
    plt.show()

    return list_variants


def clinical_significance(variant_type, file_dictionary):
    list_clinical_significance = ["Benign", "Likely benign", "Uncertain significance", "Likely pathogenic", "Pathogenic"
                                  , "drug response", "association", "risk factor", "protective", "Affects",
                                  "conflicting data from submitters", "other", "not provided", "association not found",
                                  "confers sensitivity", "Benign/Likely benign",
                                  "Conflicting interpretations of pathogenicity", "N/A"]

    dict_clinical_significance = {"Benign": 0, "Likely benign": 0, "Uncertain significance": 0, "Likely pathogenic": 0,
                                  "Pathogenic": 0, "drug response": 0, "association": 0, "risk factor": 0,
                                  "protective": 0, "Affects": 0, "other": 0, "N/A": 0,
                                  "not provided": 0, "association not found": 0, "confers sensitivity": 0,
                                  "Benign/Likely benign": 0, "Conflicting interpretations of pathogenicity": 0}

    for value in file_dictionary.values():
        if value[17] == variant_type:
            for list_item in value[14]:
                clinical = list_item.replace("_", " ")
                clinical = clinical.lstrip()
                for item in list_clinical_significance:
                    if clinical == item:
                        value_ = dict_clinical_significance.get(clinical)
                        dict_clinical_significance[clinical] = value_ + 1

    wrapped_label = []
    value_variant = []
    for key, value in dict_clinical_significance.items():
        label = '\n'.join(wrap(key.replace("_", " "), 20))
        wrapped_label.append(label)
        value_variant.append(value)

    fig = plt.figure(figsize=[10, 10])
    plt.bar(wrapped_label, value_variant)
    plt.ylabel('Aantal')
    plt.title('Clinical significance voor ' + str(variant_type))
    plt.xlabel("Clinical significance")
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.15)
    plt.show()
    # plt.close()


def gene(file_dictionary):
    dict_genes = {}

    for item in file_dictionary.values():
        gene = item[21].split(":")[0]
        if gene in dict_genes:
            dict_genes[gene] = dict_genes.get(gene) + 1
        else:
            dict_genes[gene] = 1

    sorted_dict = {k: v for k, v in sorted(dict_genes.items(), key=lambda item: item[1], reverse=True)}

    key_list = []
    value_list = []
    count = 0
    for key, value in sorted_dict.items():
        if count < 20:
            key_list.append(key)
            value_list.append(value)
            count += 1

    fig = plt.figure(figsize=[10, 10])
    plt.bar(key_list, value_list)
    plt.ylabel('Aantal')
    plt.title("Top 20 genen")
    plt.xlabel("Gen naam")
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.15)
    plt.show()


def rs_ids(file_dictionary):
    dict_rsids = {"rs id beschikbaar": 0, "rs id niet beschikbaar": 0}

    for value in file_dictionary.values():
        if value[24] == "N/A":
            dict_rsids["rs id beschikbaar"] = dict_rsids.get("rs id beschikbaar") + 1
        else:
            dict_rsids["rs id niet beschikbaar"] = dict_rsids.get("rs id niet beschikbaar") + 1


    plt.pie(dict_rsids.values(), labels=dict_rsids.keys(), autopct='%1.1f%%',
        shadow=True, startangle=90)
    plt.axis('equal')
    plt.title("Beschikbaarheid van de rs id's")
    plt.show()


def review_status(file_dictionary):
    list_review_status = ["no assertion provided", "no assertion criteria provided",
                          "no assertion for the individual variant", "criteria provided single submitter",
                          "criteria provided conflicting interpretations",
                          "criteria provided multiple submitters no conflicts", "reviewed by expert panel",
                          "practice guideline"]

    dict_review_status = {"no assertion provided": 0, "no assertion criteria provided": 0,
                          "no assertion for the individual variant": 0, "criteria provided single submitter": 0,
                          "criteria provided conflicting interpretations": 0,
                          "criteria provided multiple submitters no conflicts": 0, "reviewed by expert panel": 0,
                          "practice guideline": 0}

    for value in file_dictionary.values():
        string_review = ""
        for item in value[13]:
            item = item.replace("_", " ")
            string_review = string_review + item
        for status in list_review_status:
            if string_review == status:
                value_ = dict_review_status.get(string_review)
                dict_review_status[string_review] = value_ + 1

    wrapped_label = []
    value_variant = []
    for key, value in dict_review_status.items():
        label = '\n'.join(wrap(key.replace("_", " "), 20))
        wrapped_label.append(label)
        value_variant.append(value)

    fig = plt.figure(figsize=[10, 10])
    plt.bar(wrapped_label, value_variant)
    plt.ylabel('Aantal')
    plt.title("Review status")
    plt.xlabel("Review status type")
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.15)
    plt.show()

    return list_review_status


def revieuw_status_clinical_significance(revieuw_status, file_dictionary):
    list_clinical_significance = ["Benign", "Likely benign", "Uncertain significance", "Likely pathogenic",
                                  "Pathogenic", "drug response", "association", "risk factor", "protective", "Affects",
                                  "conflicting data from submitters", "other", "not provided", "association not found",
                                  "confers sensitivity", "Benign/Likely benign",
                                  "Conflicting interpretations of pathogenicity", "N/A"]

    dict_clinical_significance = {"Benign": 0, "Likely benign": 0, "Uncertain significance": 0, "Likely pathogenic": 0,
                                  "Pathogenic": 0, "drug response": 0, "association": 0, "risk factor": 0,
                                  "protective": 0, "Affects": 0, "other": 0, "N/A": 0,
                                  "not provided": 0, "association not found": 0, "confers sensitivity": 0,
                                  "Benign/Likely benign": 0, "Conflicting interpretations of pathogenicity": 0}

    for value in file_dictionary.values():
            string_review = ""
            for item in value[13]:
                item = item.replace("_", " ")
                string_review = string_review + item
                if string_review == revieuw_status:
                    for clinical in value[14]:
                        clinical = clinical.replace("_", " ")
                        clinical = clinical.lstrip()
                        for list_item in list_clinical_significance:
                            if clinical == list_item:
                                value_ = dict_clinical_significance.get(clinical)
                                dict_clinical_significance[clinical] = value_ + 1

    wrapped_label = []
    value_variant = []
    for key, value in dict_clinical_significance.items():
        label = '\n'.join(wrap(key.replace("_", " "), 20))
        wrapped_label.append(label)
        value_variant.append(value)

    fig = plt.figure(figsize=[10, 10])
    plt.bar(wrapped_label, value_variant)
    plt.ylabel('Aantal')
    plt.title('Clinical significance voor ' + str(revieuw_status))
    plt.xlabel("Clinical significance")
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.15)
    plt.show()
    # plt.close()


def variant(file_dictionary):
    ## 22
    lijst = []

    for value in file_dictionary.values():
        type = value[22][0].split("|")[1]
        if type not in lijst:
            lijst.append(type)

    print(lijst)


def main():
    file_dictionary = read_file()
    chromosomes(file_dictionary)
    af_colums(file_dictionary)
    list_variants = variant_type(file_dictionary)
    for item in list_variants:
        clinical_significance(item, file_dictionary)
    gene(file_dictionary)
    rs_ids(file_dictionary)
    list_review_status = review_status(file_dictionary)
    for item in list_review_status:
        revieuw_status_clinical_significance(item, file_dictionary)
    # variant(file_dictionary)


main()
