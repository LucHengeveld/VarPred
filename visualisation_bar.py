"""

"""

import plotly
import plotly.express as px
import json
import pandas as pd


def variants(results):
    variant_dict = {}
    pos_list = []
    ref_list = []
    ref_short = []
    alt_list = []
    alt_short = []

    for i in range(len(results)):
        if i == 0:
            pos_list.append(int(results[i]["POS"]))
            ref_list.append(results[i]["REF"])
            alt_list.append(results[i]["ALT"])

            if len(results[i]["REF"]) > 5:
                ref_short.append(results[i]["REF"][:5] + "...")
            else:
                ref_short.append(results[i]["REF"])

            if len(results[i]["ALT"]) > 5:
                alt_short.append(results[i]["ALT"][:5] + "...")
            else:
                alt_short.append(results[i]["ALT"])

        elif results[i]["CHROM"] == results[i - 1]["CHROM"]:
            pos_list.append(int(results[i]["POS"]))
            ref_list.append(results[i]["REF"])
            alt_list.append(results[i]["ALT"])

            if len(results[i]["REF"]) > 5:
                ref_short.append(results[i]["REF"][:5] + "...")
            else:
                ref_short.append(results[i]["REF"])

            if len(results[i]["ALT"]) > 5:
                alt_short.append(results[i]["ALT"][:5] + "...")
            else:
                alt_short.append(results[i]["ALT"])

            if results[i]["POS"] == results[-1]["POS"]:
                variant_dict[results[i]["CHROM"]] = {"POS": pos_list,
                                                     "REF": ref_list,
                                                      "ALT": alt_list,
                                                      "REF_short": ref_short,
                                                      "ALT_short": alt_short}

        elif results[i]["CHROM"] != results[i - 1]["CHROM"]:
            variant_dict[results[i - 1]["CHROM"]] = {"POS": pos_list,
                                                     "REF": ref_list,
                                                      "ALT": alt_list,
                                                      "REF_short": ref_short,
                                                      "ALT_short": alt_short}

            pos_list = [int(results[i]["POS"])]
            ref_list = [results[i]["REF"]]
            alt_list = [results[i]["ALT"]]

            if len(results[i]["REF"]) > 5:
                ref_short = [results[i]["REF"][:5] + "..."]
            else:
                ref_short = [results[i]["REF"]]

            if len(results[i]["ALT"]) > 5:
                alt_short = [results[i]["ALT"][:5] + "..."]
            else:
                alt_short = [results[i]["ALT"]]

            if results[i]["POS"] == results[-1]["POS"]:
                variant_dict[results[i]["CHROM"]] = {"POS": pos_list,
                                                     "REF": ref_list,
                                                      "ALT": alt_list,
                                                      "REF_short": ref_short,
                                                      "ALT_short": alt_short}

    return variant_dict


def CLNSIG_category(results):
    CLNSIG_dict = {}
    chromosomes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
                   "12", "13", "14", "15", "16", "17", "18", "19", "20", "21",
                   "22", "X", "Y", "MT"]

    for chrom in chromosomes:
        CLNSIG_dict[chrom] = []

    for result in results:
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

    return CLNSIG_dict


def chromosome_lengths(reference_build):
    if reference_build == "37":
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

    return chromosome_lengths_list


def graphs(chromosome_lengths_list, variant_dict, CLNSIG_dict):
    JSON_dict = {}
    disable_button_dict = {}
    for i in range(len(chromosome_lengths_list)):
        try:
            y_list = []
            positions = variant_dict[chromosome_lengths_list[i][0]]["POS"]
            print(i, positions)
            for j in range(len(positions)):
                y_list.append(0)
            disable_button_dict[chromosome_lengths_list[i][0]] = False
            df = pd.DataFrame(
                data=variant_dict[chromosome_lengths_list[i][0]])
            df["CLNSIG"] = CLNSIG_dict[chromosome_lengths_list[i][0]]
            fig = px.scatter(df, x=positions, y=y_list,
                             labels={"x": "Position",
                                     "y": "",
                                     "CLNSIG": "Clinical significance"},
                             custom_data=["REF", "ALT", "REF_short",
                                          "ALT_short", "CLNSIG"],
                             color="CLNSIG",
                             color_discrete_map={"Benign": "darkgreen",
                                                 "Likely benign": "darkgreen",
                                                 "Pathogenic": "red",
                                                 "Likely pathogenic": "red",
                                                 "Other": "yellow"},
                             category_orders={"CLNSIG": ["Benign",
                                                         "Likely benign",
                                                         "Likely pathogenic",
                                                         "Pathogenic",
                                                         "Other"]})

            fig.update_traces(
                marker=dict(size=42.5,
                            symbol='line-ns-open',
                            line=dict(width=2)),
                hovertemplate='<b>Position: %{x}' +
                              '<br>REF > ALT: %{customdata[2]} > %{'
                              'customdata[3]}</b> <extra></extra>',
                selector=dict(mode='markers'))

            fig.update_xaxes(showgrid=False, fixedrange=False,
                             range=[0, chromosome_lengths_list[i][1]],
                             tickfont_family="sans-serif", tickformat=',d')

            fig.update_yaxes(showgrid=False, fixedrange=True,
                             zeroline=True, zerolinecolor='#1c9434',
                             zerolinewidth=60,
                             showticklabels=False)

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
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            JSON_dict[chromosome_lengths_list[i][0]] = graphJSON

        except KeyError:
            disable_button_dict[chromosome_lengths_list[i][0]] = True

    return JSON_dict, disable_button_dict