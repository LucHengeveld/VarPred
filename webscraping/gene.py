import ast
from urllib.request import urlopen
import urllib


def gene_info(gene_id):
    """ Gets information for a specific gene of the NCBI gene page. The results are gene id, the ncbi link, symbol,
    full name, gene type, also known as, summary, tissue data, pubchem and the gene ontology functions.

    Args:
        gene_id: Gene id to access the NCBI gene page.

    Returns:
        gene_result: Dictionary with information about the gene.
    """
    gene_result = {}
    name = False
    gene_type = False
    known_as = False
    summary = False
    publication = False
    ontology = False
    tissue = False
    tmp_list_gene_ontology = []

    link = f"https://www.ncbi.nlm.nih.gov/gene/?term={gene_id}"
    f = urllib.request.urlopen(link)

    gene_result['Gene_id'] = gene_id
    gene_result['NCBI link'] = link
    for information_string in f:
        information_string = str(information_string)
        if '<dd class="noline"' in information_string:
            gene_result['Symbol'] = split(information_string, 1, 0, gene_id)
        elif "Full Name" in information_string:     # Next line contains the full name
            name = True
        elif name:
            gene_result['Full name'] = split(information_string, 1, 0, gene_id)
            name = False
        elif "Gene type" in information_string:       # Next line contains the gene type
            gene_type = True
        elif gene_type:
            gene_result['Gene type'] = split(information_string, 1, 0, gene_id)
            gene_type = False
        elif 'Also known as' in information_string:       # Next line contains the 'Also known as' information
            known_as = True
        elif known_as:
            gene_result['Also known as'] = split(information_string, 1, 0, gene_id)
            known_as = False
        elif "<dt>Summary" in information_string:         # Next line contains the summary
            summary = True
        elif summary:
            gene_result['Summary'] = split(information_string, 1, 0, gene_id)
            summary = False
        elif "var tissues_data" in information_string:
            start_dict = information_string.find("{")
            if start_dict != -1:
                # from string to dictionary
                gene_result['Result tissue'] = \
                    tissue_data(ast.literal_eval(information_string[start_dict:].replace(';\\n"', "")))
                tissue = True
        elif "project-summary-title" in information_string and tissue:
            gene_result['Project title tissue'] = split_variable(information_string, 1, ':', 0, '<', gene_id).lstrip()
        elif "project-summary-desc" in information_string and tissue:
            gene_result['Project description tissue'] = \
                split_variable(information_string, 1, ':', 0, '<', gene_id).lstrip()
        elif "Publication:" in information_string and tissue:
            publication = True
        elif publication and "span" in information_string and tissue:
            gene_result['Publication id tissue'] = split(information_string, 2, 0, gene_id)
            publication = False
            tissue = False
        elif "Pathways from PubChem" in information_string:
            gene_result['Pubchem'] = \
                f"https://pubchem.ncbi.nlm.nih.gov/gene/{gene_id}#section=Pathways&page_size=25&fullscreen=true"
        elif "Gene Ontology" in information_string:
            ontology = True
        elif ontology and information_string.startswith("b'                <a href"):  # gene ontology function location
            result_ontology = split(information_string, 1, 0, gene_id)
            if result_ontology not in tmp_list_gene_ontology:
                tmp_list_gene_ontology.append(result_ontology)
        elif "Process" in information_string:
            gene_result['Gene ontology functions'] = tmp_list_gene_ontology
            ontology = False

    return gene_result


def tissue_data(dict_results):
    """ Gets the 'full_rpkm' value for the tissue data in a new dictionary.

    Args:
        dict_results: Dictionary contains all tissue data.

    Returns:
        dict_results_tissue: Dictionary contains only the 'full_rpkm' value.
    """
    dict_results_tissue = {}

    for key, value in dict_results.items():
        dict_results_tissue[key] = value['full_rpkm']

    return dict_results_tissue


def split(item, number_1, number_2, gene_id):
    """ Split a string to get the information.

    Args:
        item: String containg information about the gene.
        number_1: A number (zero-based) for splitting the string.
        number_2: A number (zero-based) for splitting the string.
        gene_id: The Gene ID for the information.

    Returns:
        Value containing information about the gene.
    """
    try:
        return item.split(">")[number_1].split("<")[number_2]
    except IndexError:
        return f'Parsing went wrong, for more information see NCBI Gene {gene_id}'


def split_variable(item, number_1, split_1, number_2, split_2, gene_id):
    """ Split a string to get the information.

    Args:
        item: String containg information about the gene.
        number_1: A number (zero-based) for splitting the string.
        split_1: A value for splitting the string.
        number_2: A number (zero-based) for splitting the string.
        split_2: A value for splitting the string.
        gene_id: The Gene ID for the information.

    Returns:
        Value containing information about the gene.
    """
    try:
        return item.split(split_1)[number_1].split(split_2)[number_2]
    except IndexError:
        return f'Parsing went wrong, for more information see NCBI Gene {gene_id}'
