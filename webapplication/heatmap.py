"""
This module calculates the rgb colors for the background of the
pathogenicity table and saves the values in a dictionary.
"""


def heatmap(results_table_dict):
    """
    Saves the variants in the vcf file to a list.
    :param results_table_dict:
    :return color_dict: Dictionary with the structure {Chromosome: [rgb color]}
    """

    # Creates an empty dictionary
    color_dict = {}

    # Loops through the results_table_dict
    for chrom in results_table_dict:

        # Saves the total amount of variants of a chromosome to a
        # variable and creates an empty list
        total_variants = results_table_dict[chrom][0]
        color_list = []

        # Loops through the variation list in results_table_dict[chrom]
        # and calculates the rgb color for the heatmap
        for i in range(len(results_table_dict[chrom])):
            if i == 0:
                color = 255
            elif total_variants != 0:
                color = 255 - (255 / total_variants) * \
                        results_table_dict[chrom][i]
            else:
                color = 255

            # Appends the rgb color to a list
            color_list.append(int(color))

        # Adds the list of colors from a chromosome to a dictionary
        color_dict[chrom] = color_list

    # Returns the color dictionary
    return color_dict
