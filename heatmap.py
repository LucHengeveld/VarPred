"""

"""


def heatmap(results_table_dict):
    chromosomes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
                   "12", "13", "14", "15", "16", "17", "18", "19", "20", "21",
                   "22", "X", "Y", "MT"]

    color_dict = {}
    for chrom in chromosomes:
        color_dict[chrom] = [0, 0, 0, 0, 0, 0, 0]

    for chrom in results_table_dict:
        total_variants = results_table_dict[chrom][0]
        color_list = []
        for i in range(len(results_table_dict[chrom])):
            if i == 0:
                color = 255
            elif total_variants != 0:
                color = 255 - (255 / total_variants) * \
                        results_table_dict[chrom][i]
            else:
                color = 255
            color_list.append(int(color))
        color_dict[chrom] = color_list

    return color_dict