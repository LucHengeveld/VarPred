"""
This module creates the different components that are needed for the
visualisation bar.
"""

import plotly
import plotly.express as px
import json
import pandas as pd


def variants(results):
    """
    Creates a dictionary per chromosome with all the position, ref, alt,
        ref_short and alt_short variables.
    :param results: List with data of the found variants from the database.
    :return variant_dict: Dictionary with the structure {Chromosome: {"POS":
        pos_list, "REF": ref_list, "ALT": alt_list, "REF_short": ref_short,
        "ALT_short": alt_short}.
    """

    # Creates an empty dictionary
    variant_dict = {}

    # Creates empty lists
    pos_list = []
    ref_list = []
    ref_short = []
    alt_list = []
    alt_short = []

    # Loops through all variants in results
    for i in range(len(results)):

        # If its the first variant in the results list it adds the pos,
        # ref, alt, ref_short and alt_short to a list
        if i == 0:
            pos_list.append(int(results[i]["POS"]))
            ref_list.append(results[i]["REF"])
            alt_list.append(results[i]["ALT"])

            # Checks if the length of the ref and alt is longer than 5.
            # If it is it cuts it off at 5 letters and adds dots to the
            # end
            if len(results[i]["REF"]) > 5:
                ref_short.append(results[i]["REF"][:5] + "...")
            else:
                ref_short.append(results[i]["REF"])
            if len(results[i]["ALT"]) > 5:
                alt_short.append(results[i]["ALT"][:5] + "...")
            else:
                alt_short.append(results[i]["ALT"])

        # Checks if the next result has the same chromosome number as
        # the previous result.
        elif results[i]["CHROM"] == results[i - 1]["CHROM"]:
            pos_list.append(int(results[i]["POS"]))
            ref_list.append(results[i]["REF"])
            alt_list.append(results[i]["ALT"])

            # Checks if the length of the ref and alt is longer than 5.
            # If it is it cuts it off at 5 letters and adds dots to the
            # end
            if len(results[i]["REF"]) > 5:
                ref_short.append(results[i]["REF"][:5] + "...")
            else:
                ref_short.append(results[i]["REF"])
            if len(results[i]["ALT"]) > 5:
                alt_short.append(results[i]["ALT"][:5] + "...")
            else:
                alt_short.append(results[i]["ALT"])

            # Checks if the variant is the last one in results. If it is
            # it saves the variant information to the variant_dict
            if results[i] == results[-1]:
                variant_dict[results[i]["CHROM"]] = {"POS": pos_list,
                                                     "REF": ref_list,
                                                     "ALT": alt_list,
                                                     "REF_short": ref_short,
                                                     "ALT_short": alt_short}

        # If the next result has a new chromosome number it adds the
        # lists to the variant dictionary
        elif results[i]["CHROM"] != results[i - 1]["CHROM"]:
            variant_dict[results[i - 1]["CHROM"]] = {"POS": pos_list,
                                                     "REF": ref_list,
                                                     "ALT": alt_list,
                                                     "REF_short": ref_short,
                                                     "ALT_short": alt_short}
            # Saves the pos, ref and alt to a list
            pos_list = [int(results[i]["POS"])]
            ref_list = [results[i]["REF"]]
            alt_list = [results[i]["ALT"]]

            # Checks if the length of the ref and alt is longer than 5.
            # If it is it cuts it off at 5 letters and adds dots to the
            # end
            if len(results[i]["REF"]) > 5:
                ref_short = [results[i]["REF"][:5] + "..."]
            else:
                ref_short = [results[i]["REF"]]
            if len(results[i]["ALT"]) > 5:
                alt_short = [results[i]["ALT"][:5] + "..."]
            else:
                alt_short = [results[i]["ALT"]]

            # Checks if the variant is the last one in results. If it is
            # it saves the variant information to the variant_dict
            if results[i] == results[-1]:
                variant_dict[results[i]["CHROM"]] = {"POS": pos_list,
                                                     "REF": ref_list,
                                                     "ALT": alt_list,
                                                     "REF_short": ref_short,
                                                     "ALT_short": alt_short}

    # Returns the variant dictionary
    return variant_dict


def clnsig_category(results):
    """
    Adds the clinical significance of a variant to a dictionary
    :param results: List with data of the found variants from the database.
    :return CLNSIG_dict: Dictionary with the structure {Chromosome: [clinical
        significances].
    """
    # Creates an empty dictionary
    CLNSIG_dict = {}

    # Creates a list with all the chromosomes
    chromosomes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
                   "12", "13", "14", "15", "16", "17", "18", "19", "20", "21",
                   "22", "X", "Y", "MT"]

    # Loops through the chromosomes list
    for chrom in chromosomes:

        # Adds an empty list to the value of every chromosome key
        CLNSIG_dict[chrom] = []

    # Loops through the results
    for result in results:

        # Categorizes the results based on the clinical significance in
        # the following groups: Benign, Likely benign, Likely
        # pathogenic, Pathogenic and Other
        if "Benign" in result["CLNSIG"] and "Likely" not in result["CLNSIG"]:
            CLNSIG_dict[result["CHROM"]].append("Benign")

        elif "Likely benign" in result["CLNSIG"]:
            CLNSIG_dict[result["CHROM"]].append("Likely benign")

        elif "Likely pathogenic" in result["CLNSIG"]:
            CLNSIG_dict[result["CHROM"]].append("Likely pathogenic")

        elif "Pathogenic" in result["CLNSIG"] and "Likely" not in result[
            "CLNSIG"] and "Conflicting interpretations" not in result[
            "CLNSIG"]:
            CLNSIG_dict[result["CHROM"]].append("Pathogenic")

        else:
            CLNSIG_dict[result["CHROM"]].append("Other")

    # Returns the clinical significance dictionary
    return CLNSIG_dict


def chromosome_lengths(reference_build):
    """
    Returns the chromosome lengths of the selected chromosome build.
    :param reference_build: The selected reference build from the
        webapplication.
    :return chromosome_lengths_list: A 2D list containing the chromosomes and
        the lengths of every chromosome in the selected reference build.
    """

    # Checks if the selected reference build is 37
    if reference_build == "37":
        # If the selected reference build is 37 it returns the
        # chromosome_lengths_list below
        chromosome_lengths_list = [["1", 249250621], ["2", 243199373],
                                   ["3", 198022430], ["4", 191154276],
                                   ["5", 180915260], ["6", 171115067],
                                   ["7", 159138663], ["8", 146364022],
                                   ["9", 141213431], ["10", 135534747],
                                   ["11", 135006516], ["12", 133851895],
                                   ["13", 115169878], ["14", 107349540],
                                   ["15", 102531392], ["16", 90354753],
                                   ["17", 81195210], ["18", 78077248],
                                   ["19", 59128983], ["20", 63025520],
                                   ["21", 48129895], ["22", 51304566],
                                   ["X", 155270560], ["Y", 59373566],
                                   ["MT", 16569]]

    # If the selected reference build is 38 it returns the
    # chromosome_lengths_list below
    else:
        chromosome_lengths_list = [["1", 248956422], ["2", 242193529],
                                   ["3", 198295559], ["4", 190214555],
                                   ["5", 181538259], ["6", 170805979],
                                   ["7", 159345973], ["8", 145138636],
                                   ["9", 138394717], ["10", 133797422],
                                   ["11", 135086622], ["12", 133275309],
                                   ["13", 114364328], ["14", 107043718],
                                   ["15", 101991189], ["16", 90338345],
                                   ["17", 83257441], ["18", 80373285],
                                   ["19", 58617616], ["20", 64444167],
                                   ["21", 46709983], ["22", 50818468],
                                   ["X", 156040895], ["Y", 57227415],
                                   ["MT", 16569]]

    # Returns the chromosome lengths list
    return chromosome_lengths_list


def graphs(chromosome_lengths_list, variant_dict, CLNSIG_dict):
    """
    Creates a graph for every chromosome and a disable button dict to
        deactivate chromosome buttons without results.
    :param chromosome_lengths_list: A 2D list containing the chromosomes and
        the lengths of every chromosome in the selected reference build.
    :param variant_dict: Dictionary with the structure {Chromosome: {"POS":
        pos_list, "REF": ref_list, "ALT": alt_list, "REF_short": ref_short,
        "ALT_short": alt_short}.
    :param CLNSIG_dict: Dictionary with the structure {Chromosome: [clinical
        significances].
    :return JSON_dict: Dictionary with the structure {Chromosome: graph in JSON
        format}.
    :return disable_button_dict: Dictionary with the structure {Chromosome:
    True/False}.
    """

    # Creates empty dictionaries
    JSON_dict = {}
    disable_button_dict = {}

    # Loops through the chromosome lengths list
    for i in range(len(chromosome_lengths_list)):

        # If there have been results found for a specific chromosome it
        # passes this try
        try:

            # Creates an empty list
            y_list = []

            # Retrieves all variant positions from a chromosome
            positions = variant_dict[chromosome_lengths_list[i][0]]["POS"]

            # Loops through the positions list and adds the value 0 for
            # every position to the y-axis list
            for j in range(len(positions)):
                y_list.append(0)

            # If there are results found for a specific chromosome it
            # sets a boolean in the disable button dict to False
            disable_button_dict[chromosome_lengths_list[i][0]] = False

            # Creates a pandas dataframe and adds the following columns:
            # POS, REF, ALT, REF_short, ALT_short, CLNSIG
            df = pd.DataFrame(
                data=variant_dict[chromosome_lengths_list[i][0]])
            df["CLNSIG"] = CLNSIG_dict[chromosome_lengths_list[i][0]]

            # Makes a scatter plot out of the variant positions and
            # pandas dataframe
            fig = px.scatter(df, x=positions, y=y_list,

                             # Adds a label to the axes and legend
                             labels={"x": "Position",
                                     "y": "",
                                     "CLNSIG": "Clinical significance"},

                             # Retrieves the dataframe columns
                             custom_data=["REF", "ALT", "REF_short",
                                          "ALT_short", "CLNSIG"],

                             # Categorises the variants based on the
                             # clinical significance column
                             color="CLNSIG",

                             # Adds a specific color to the different
                             # clinical significance categories
                             color_discrete_map={"Benign": "darkgreen",
                                                 "Likely benign": "darkgreen",
                                                 "Pathogenic": "red",
                                                 "Likely pathogenic": "red",
                                                 "Other": "yellow"},

                             # Shows the legend in a specific order
                             category_orders={"CLNSIG": ["Benign",
                                                         "Likely benign",
                                                         "Likely pathogenic",
                                                         "Pathogenic",
                                                         "Other"]})

            # Adds the markers and hover text to the graph
            fig.update_traces(

                # Gives the markers a specific height, symbol and width
                marker=dict(size=42.5,
                            symbol='line-ns-open',
                            line=dict(width=2)),

                # Adds the hovertext when you hover over a variant
                hovertemplate='<b>Position: %{x}' +
                              '<br>REF > ALT: %{customdata[2]} > %{'
                              'customdata[3]}</b> <extra></extra>',

                # Adds the markers to the graph
                selector=dict(mode='markers'))

            # Updates some parameters of the x axis, including the
            # range, font and tick format
            fig.update_xaxes(showgrid=False, fixedrange=False,
                             range=[0, chromosome_lengths_list[i][1]],
                             tickfont_family="sans-serif", tickformat=',d')

            # Updates some parameters of the y axis, including the
            # range and the zeroline at y=0
            fig.update_yaxes(showgrid=False, fixedrange=True,
                             zeroline=True, zerolinecolor='#1c9434',
                             zerolinewidth=60,
                             showticklabels=False)

            # Updates the layout parameters of the graph
            fig.update_layout(height=300, plot_bgcolor='white',
                              font_size=16,
                              font_family="sans-serif",
                              font_color="black",
                              margin=dict(l=0, r=40, t=100, b=20),
                              hoverlabel=dict(
                                  bgcolor='#38b553',
                                  font_size=22,
                                  font_family="sans-serif",
                                  font_color="black"
                              ))

            # Dumps the graphs in a JSON so it can be shown on the
            # webapplication using javascript
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            # Saves the JSON graphs of every chromosome to a dictionary
            JSON_dict[chromosome_lengths_list[i][0]] = graphJSON

        # If there are no results found for a specific chromosome it
        # sets a boolean in the disable button dict to True
        except KeyError:
            disable_button_dict[chromosome_lengths_list[i][0]] = True

    # Returns the JSON graph and the disable buttons dictionaries
    return JSON_dict, disable_button_dict
