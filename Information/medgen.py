from urllib.request import urlopen
import urllib


def medgen_info(medgen_id):
    """ With a MedGen ID it gets all the information of the MedGen NCBI page and filters the medgen id, NCBI link,
    title, description, external databases links, synonyms, inheritance, clinical features and conditions with this
    feature. For a few rare cases, the MedGen ID is not right connected with the NCBI MedGen database. Then the MedGen
    UID will be used for extracting the information.

    Args:
        medgen_id: MedGen ID of the NCBI MedGen database.

    Returns:
        medgen_result: A dictionary contains all available information of the MedGen ID.
    """

    medgen_result = {}
    snomed = False
    synonym = False
    clinical = False
    description_clinical = False
    inheritance = False
    tlline = False
    wrong_id = False
    tmp_list = []
    tmp_list_category = []
    tmp_dict_category = {}
    tmp_inheritance = []
    tmp_source = []

    link = f"https://www.ncbi.nlm.nih.gov/medgen/?term={medgen_id}"
    f = urllib.request.urlopen(link)

    medgen_result['medgen_id'] = medgen_id
    medgen_result['NCBI Link'] = link
    for information_string in f:
        information_string = str(information_string)
        if "description" in information_string:
            result = information_string.split("=")
            for entry in result:
                if 'description" content' in entry:
                    description = result[result.index(entry) + 1].split("/>")[0].replace('"', "")
                    if len(description) != 1:               # sometimes the description is on a different place
                        medgen_result["description"] = description.replace("\\", "").rstrip()
        if "<title>" in information_string:
            title = split_variable(information_string, 1, ">", 0, "(", medgen_id).rstrip()  # location title value
            if 'MedGen - NCBI</title' in title:             # Link in NCBI MedGen databases is wrong
                wrong_id = True
            else:
                medgen_result['title'] = title
        if "<td>" in str(information_string):
            if "//omim.org" in information_string:
                medgen_result['omim_id'] = split(information_string, 2, 0, medgen_id)
            elif "www.orpha.net" in information_string:
                medgen_result['orpha_id'] = split(information_string, 2, 0, medgen_id)
            elif "MONDO" in information_string:
                medgen_result['mondo_id'] = split_variable(information_string, 2, ">", 0, "<", medgen_id)
            elif "strong" in information_string:
                medgen_result['inheritance'] = split(information_string, 2, 0, medgen_id)
            elif "SNOMED CT" in information_string:
                snomed = True
            elif snomed:
                medgen_result['snomed'] = snomed_value_results(information_string.split(";"))
                snomed = False
            elif "Synonym:" in information_string or "Synonyms:" in information_string:
                synonym = True
            elif synonym:
                medgen_result['synonym'] = synonyms_value_results(information_string.split(";"))
                synonym = False
            elif "https://hpo" in information_string:
                medgen_result['hpo'] = split(information_string, 2, 0, medgen_id)
        if "Modes of inheritance:" in information_string:
            inheritance = True
        if inheritance:
            if "strong" in information_string:              # first value for the inheritance
                tmp_inheritance.append(split(information_string, 3, 0, medgen_id))
            if "Sources" in information_string or "Source" in information_string:
                tmp_source.append(split_variable(information_string, 1, ":", 0, "<", medgen_id).lstrip())
            if '"jig-ncbipopper"' in information_string:        # end of the results of the inheritance
                medgen_result['name inheritance'] = tmp_inheritance
                medgen_result['source inheritance'] = tmp_source
                inheritance = False
        if 'title="Show/hide content"' in information_string and "Clinical features" in information_string:
            clinical = True             # the clinical information starts after this line
        elif clinical:
            if "<strong>" in information_string and "HPO" not in information_string:            # begin feature value
                try:
                    feature = split(information_string, 3, 0, medgen_id)
                except IndexError:                      # sometimes lcoation value is different
                    feature = split(information_string, 1, 0, medgen_id)
                description_clinical = True             # Next line is the description of the feature
            elif description_clinical:
                if "nowrap" in information_string:      # No description for the feature
                    feature_with_description = feature + ";" + "no description"
                    if feature_with_description not in tmp_list:
                        tmp_list.append(feature_with_description)
                    if "TLline" in information_string:
                        try:
                            name = split(information_string, 17, 0, medgen_id)              # gets feature category
                        except IndexError:
                            name = split(information_string, 11, 0, medgen_id)              # gets feature category
                    description_clinical = False
                else:
                    try:                # feature description
                        description_feature = information_string.split(">")[1].replace("</div", "").replace("\\", "")
                    except IndexError:
                        description_feature = ""
                    feature_with_description = feature + ";" + description_feature
                    if feature_with_description not in tmp_list:
                        tmp_list.append(feature_with_description)
                    description_clinical = False
            elif '"TLline"' in information_string:
                tlline = True
                count = information_string.count("span class")
                if "jig-ncbipopper" not in information_string:
                    try:
                        name = split(information_string, 17, 0, medgen_id)
                    except IndexError:
                        name = split(information_string, 11, 0, medgen_id)
                elif count == 1:
                    tmp_list_category.append(split(information_string, 2, 0, medgen_id))       # name first clinical
                elif count == 2:
                    tmp_list_category.append(split(information_string, 2, 0, medgen_id))       # name second clinical
                    tmp_dict_category[name] = tmp_list_category
                    tmp_list_category = []
                    name = split(information_string, 9, 0, medgen_id)
            elif tlline and information_string == "b'</div>\\n'":                   # end of the clinical values
                tmp_dict_category[name] = tmp_list_category
                medgen_result['Clinical significance'] = clinical_significance_results(tmp_list, tmp_dict_category)
                tlline = False
                clinical = False
            elif '"TLline"' not in information_string and "jig-ncbipopper" in information_string:
                medgen_result['Clinical significance'] = change_tmp_list(tmp_list)
                clinical = False
        elif "Conditions with this feature" in information_string:
            medgen_result['Conditions with this feature'] = f'For more information: {link}'
        elif wrong_id and 'rprtnum nohighlight' in information_string and medgen_id in information_string:
            # gets new MedGen ID if link with NCBI MedGen database is not correct
            new_medgen_id = split_variable(information_string, 1, 'Select item', 0, '<', medgen_id).lstrip()

    if wrong_id:
        return medgen_info(new_medgen_id)
    else:
        return medgen_result


def change_tmp_list(tmp_list):
    """ Change a list for putting spaces between the ';'.

    Args:
        tmp_list: A temporary list with structure and values: key;value.

    Returns:
        new_tmp_list: A temporary list with structure and values: key ; value.
    """
    new_tmp_list = []
    for item in tmp_list:
        result = item.replace(";", " ; ")
        new_tmp_list.append(result)

    return new_tmp_list


def snomed_value_results(snomed_values):
    """ Gets a list of snomed values and removes all characters around the snomed values.

    Args:
        snomed_values: A list containing all snomed values with unnecessary characters.

    Returns:
        snomed_value: A list containing all snomed values without unnecessary characters.
    """
    snomed_value = ""
    for value in snomed_values:
        if snomed_value == "":                 # get the first snomed value
            # all possible characters
            snomed_value = value.replace("\\xc2\\xa0", " ").replace("b'<td>", "").replace("</td></tr>\\n'", "") \
                .replace('b"<td>', "").replace('</td></tr>\\n"', "").lstrip()
        else:                               # all possible characters
            snomed_value = snomed_value + "; " + value.replace("\\xc2\\xa0", " ").replace("b'<td>", ""). \
                replace("</td></tr>\\n'", "").replace('b"<td>', "").replace('</td></tr>\\n"', "").lstrip()

    return snomed_value


def synonyms_value_results(synonym_values):
    """ Gets a list of synonym values and removes all characters around the synonym values.

    Args:
        synonym_values: A list containing all synonym values with unnecessary characters.

    Returns:
        synonym_values: A list containing all synonym values with unnecessary characters.
    """
    synonym_value = ""
    for value in synonym_values:
        if synonym_value == "":                 # get the first synonym value
            # all possible characters
            synonym_value = value.replace("b'<td>", "").replace("</td></tr>\\n'", "").replace('b"<td>', "") \
                .replace('</td></tr>\\n"', "").lstrip()
        else:
            # all possible characters
            synonym_value = synonym_value + "; " + value.replace("b'<td>", "").replace("</td></tr>\\n'", "") \
                .replace('b"<td>', "").replace('</td></tr>\\n"', "").lstrip()

    return synonym_value


def clinical_significance_results(tmp_list_description, tmp_dict_category):
    """ Gets a list with all descriptions and a dictionary with all categories of the clinical significance and combines
    these 2 toghether in a dictionary.

    Args:
        tmp_list_description: A temporary list with structure and values: feature;description_feature.
        tmp_dict_category: A temporary dictionary with structure and values: category feature;description_feature.

    Returns:
        results: A dictionary containing categorys with features and descriptions.
    """
    tmp_list = []
    results = {}

    for key, value in tmp_dict_category.items():
        for item in value:
            for description in tmp_list_description:
                description = description.split(";")
                if description[0] == item:
                    description_value = item + " ; " + description[1]
                    tmp_list.append(description_value)
        results[key] = tmp_list
        tmp_list = []

    return results


def split(item, number_1, number_2, medgen_id):
    """ Split a string to get information.

    Args:
        item: String containg information about the medgen entry.
        number_1: A number (zero-based) for splitting the string.
        number_2: A number (zero-based) for splitting the string.
        medgen_id: The MedGen ID for the information.

    Returns:
        Value containing information about the medgen entry.
    """
    try:
        return item.split(">")[number_1].split("<")[number_2]
    except IndexError:
        return f'Parsing went wrong, for more information see NCBI MedGen {medgen_id}'


def split_variable(item, number_1, split_1, number_2, split_2, medgen_id):
    """ Split a string to get the information.

    Args:
        item: String containg information about the medgen id.
        number_1: A number (zero-based) for splitting the string.
        split_1: A value for splitting the string.
        number_2: A number (zero-based) for splitting the string.
        split_2: A value for splitting the string.
        medgen_id: The MedGen ID for the information.

    Returns:
        Value containing information about the medgen entry.
    """

    try:
        return item.split(split_1)[number_1].split(split_2)[number_2]
    except IndexError:
        return f'Parsing went wrong, for more information see NCBI MedGen {medgen_id}'
