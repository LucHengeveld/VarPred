import ast
from flask import Flask, render_template, request
import pymongo
import plotly
import plotly.express as px
import json
import pandas as pd

app = Flask(__name__)


@app.route('/')
@app.route('/home.html', methods=["POST", "GET"])
def get_input():
    """
    This function retrieves the entered file from the webapplication, calls
    all other functions and renders the results page.

    :return render template: results.html
    """
    # If calculator results button is pressed:
    if request.method == 'POST':

        # Retrieves the entered file from the webapplication and saves
        # its name.
        vcf_file = request.files["vcf_file"]
        vcf_file_name = vcf_file.filename

        # Check if the file extension is ".vcf"
        if vcf_file_name.endswith(".vcf"):

            # Saves the file and calls the function verify_vcf to verify
            # the format in the entered file.
            vcf_file.save(vcf_file_name)
            correct_vcf = verify_vcf(vcf_file_name)

            if correct_vcf:

                # Calls the function vcf_to_list
                vcf_list = vcf_to_list(vcf_file_name)

                # Calls the function create_compare_list
                compare_list = create_compare_list(vcf_list)

                # Retrieves the selected reference build
                reference_build = request.form.get("reference_selector")

                # Calls the function compare_dataset
                compare_dataset(compare_list, reference_build)

                # Creates the visualisation bar
                JSON_dict, disable_button_dict, chromosome_lengths_list, position_dict = visualisation_bar(
                    reference_build)

                results_table(position_dict)

                # Returns the results page
                return render_template('results.html',
                                       results=results,
                                       JSON_dict=JSON_dict,
                                       disable_button_dict=disable_button_dict,
                                       results_table_list=results_table_list)

            else:
                # Returns an error if the file format is incorrect.
                return render_template('calculator.html',
                                       errormsg="Entered file has the wrong "
                                                "format")

        elif vcf_file_name != "":
            # Returns an error if a file with the wrong file extension
            # is entered on the webapplication.
            return render_template('calculator.html',
                                   errormsg="Entered file has the"
                                            "wrong file extension. Please "
                                            "enter a .vcf file")

        else:
            # Returns an error if no file is selected.
            return render_template('calculator.html', errormsg="No file "
                                                               "selected.")

    else:
        # Returns the standard home page.
        return render_template('home.html')


def verify_vcf(vcf_file_name):
    """
    Checks if the entered file contains the correct columns.
    :param vcf_file_name: Name of the entered vcf file on the webapplication.
    :return correct_vcf: Boolean which is True if entered file format is
    correct.
    """
    # Creates a boolean
    correct_vcf = False
    # Checks if file has a line with all the vcf columns
    with open(vcf_file_name) as file:
        for line in file:
            if line.startswith("#CHROM\tPOS\tID\tREF\tALT"):
                correct_vcf = True
                break
    file.close()

    # Returns the boolean
    return correct_vcf


def vcf_to_list(vcf_file_name):
    """
    Saves the mutations in the vcf file to a list.
    :param vcf_file_name: Name of the entered vcf file
    :return vcf_list: List with the structure [CHROM, POS, ID, REF, ALT, QUAL,
    FILTER, INFO]
    """

    # Creates an empty list
    vcf_list = []

    # Saves the mutation information in a list
    with open(vcf_file_name) as file:
        for line in file:
            if not line.startswith("#"):
                vcf_list.append(line.split("\t"))
    file.close()

    vcf_list.sort()

    # Returns the list
    return vcf_list


def create_compare_list(vcf_list):
    """
    This functions retrieves all chromosome numbers and positions from the
    entered vcf file and adds it to a list.
    :param vcf_list: List with the structure [CHROM, POS, ID, REF, ALT, QUAL,
    FILTER, INFO]
    :return: compare_list: List with all the the chromosome numbers and
    # positions out of the vcf_list
    """
    # Creates empty lists
    chrom_list = []
    pos_list = []
    ref_list = []
    alt_list = []

    # Loops through the vcf_list and saves the chromosome numbers and
    # positions to a 2D list with the structure [chrom_list, pos_list]
    for i in vcf_list:
        chrom_list.append(i[0])
        pos_list.append(i[1])
        ref_list.append(i[3])
        alt_list.append(i[4])
    compare_list = [chrom_list, pos_list, ref_list, alt_list]

    # Returns the compare_list
    return compare_list


def compare_dataset(compare_list, reference_build):
    """
    Compares the compare_list to the chromosome numbers and positions in the
    Mongo database.
    :param reference_build:
    :param compare_list: List with all the chromosome numbers and positions out
     of the vcf_list
    :return results: List with data of the found mutations
    """
    # Connect to the local database
    myclient = pymongo.MongoClient("mongodb")
    mydb = myclient["varpred"]
    if reference_build == "37":
        mycol = mydb["variants37"]
    else:
        mycol = mydb["variants38"]

    # Create an empty list
    global results
    results = []
    # Saves the results in a list

    for i in range(len(compare_list[0])):

        for simularity in mycol.find({"$and": [{"CHROM": compare_list[0][i]},
                                               {"POS": compare_list[1][i]},
                                               {"REF": compare_list[2][i]},
                                               {"ALT": compare_list[3][i]}]},
                                     {"_id": 0}):
            results.append(simularity)


def visualisation_bar(reference_build):
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

    position_dict = {}
    mutation_dict = {}
    pos_list = []
    ref_list = []
    ref_short = []
    alt_list = []
    alt_short = []

    for i in range(len(results)):
        if i == 0:
            pos_list.append(int(results[i]["POS"]))
            ref_list.append(results[i]["REF"])

            if len(results[i]["REF"]) > 5:
                ref_short.append(results[i]["REF"][:5] + "...")
            else:
                ref_short.append(results[i]["REF"])

            alt_list.append(results[i]["ALT"])
            if len(results[i]["ALT"]) > 5:
                alt_short.append(results[i]["ALT"][:5] + "...")
            else:
                alt_short.append(results[i]["ALT"])

        elif results[i]["CHROM"] == results[i - 1]["CHROM"]:
            pos_list.append(int(results[i]["POS"]))
            ref_list.append(results[i]["REF"])

            if len(results[i]["REF"]) > 5:
                ref_short.append(results[i]["REF"][:5] + "...")
            else:
                ref_short.append(results[i]["REF"])

            alt_list.append(results[i]["ALT"])
            if len(results[i]["ALT"]) > 5:
                alt_short.append(results[i]["ALT"][:5] + "...")
            else:
                alt_short.append(results[i]["ALT"])

            if results[i]["POS"] == results[-1]["POS"]:
                position_dict[results[i]["CHROM"]] = pos_list
                mutation_dict[results[i]["CHROM"]] = {"REF": ref_list,
                                                      "ALT": alt_list,
                                                      "REF_short": ref_short,
                                                      "ALT_short": alt_short}

        elif results[i]["CHROM"] != results[i - 1]["CHROM"]:
            position_dict[results[i - 1]["CHROM"]] = pos_list
            mutation_dict[results[i - 1]["CHROM"]] = {"REF": ref_list,
                                                      "ALT": alt_list,
                                                      "REF_short": ref_short,
                                                      "ALT_short": alt_short}
            pos_list = [int(results[i]["POS"])]

            ref_list = [results[i]["REF"]]
            if len(results[i]["REF"]) > 5:
                ref_short = [results[i]["REF"][:5] + "..."]
            else:
                ref_short = [results[i]["REF"]]

            alt_list = [results[i]["ALT"]]
            if len(results[i]["ALT"]) > 5:
                alt_short = [results[i]["ALT"][:5] + "..."]
            else:
                alt_short = [results[i]["ALT"]]

            if results[i]["POS"] == results[-1]["POS"]:
                position_dict[results[i]["CHROM"]] = pos_list
                mutation_dict[results[i]["CHROM"]] = {"REF": ref_list,
                                                      "ALT": alt_list,
                                                      "REF_short": ref_short,
                                                      "ALT_short": alt_short}
    JSON_dict = {}
    disable_button_dict = {}
    for i in range(len(chromosome_lengths_list)):
        try:
            y_list = []
            x_list = position_dict[chromosome_lengths_list[i][0]]
            for j in range(len(x_list)):
                y_list.append(0)
            disable_button_dict[chromosome_lengths_list[i][0]] = False
            df = pd.DataFrame(
                data=mutation_dict[chromosome_lengths_list[i][0]])
            fig = px.scatter(df, x=x_list, y=y_list,
                             labels={"x": "Position",
                                     "y": ""},
                             custom_data=["REF", "ALT", "REF_short",
                                          "ALT_short"])
            fig.update_traces(marker=dict(size=42.5,
                                          symbol='line-ns',
                                          line=dict(width=2,
                                                    color='black')),
                              hovertemplate=
                              '<b>Positie: %{x}' +
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
            fig.update_layout(height=260, plot_bgcolor='white',
                              font_size=16,
                              font_family="sans-serif",
                              font_color="black",
                              margin=dict(l=0, r=40),
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

    return JSON_dict, disable_button_dict, chromosome_lengths_list, \
           position_dict


def results_table(position_dict):
    chromosomes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
                   "12", "13", "14", "15", "16", "17", "18", "19", "20", "21",
                   "22", "X", "Y", "MT"]

    variation_length_dict = {}
    for i in chromosomes:
        try:
            variation_length_dict[i] = len(position_dict[i])
        except KeyError:
            variation_length_dict[i] = 0

    empty_dict = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,
                  '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0,
                  '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0,
                  '21': 0, '22': 0, 'X': 0, 'Y': 0, 'MT': 0}
    benign_dict = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,
                  '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0,
                  '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0,
                  '21': 0, '22': 0, 'X': 0, 'Y': 0, 'MT': 0}
    likely_benign_dict = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,
                  '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0,
                  '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0,
                  '21': 0, '22': 0, 'X': 0, 'Y': 0, 'MT': 0}
    likely_pathogenic_dict = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,
                  '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0,
                  '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0,
                  '21': 0, '22': 0, 'X': 0, 'Y': 0, 'MT': 0}
    pathogenic_dict = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,
                  '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0,
                  '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0,
                  '21': 0, '22': 0, 'X': 0, 'Y': 0, 'MT': 0}
    predicted_benign_dict = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,
                  '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0,
                  '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0,
                  '21': 0, '22': 0, 'X': 0, 'Y': 0, 'MT': 0}
    predicted_pathogenic_dict = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,
                  '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0,
                  '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0,
                  '21': 0, '22': 0, 'X': 0, 'Y': 0, 'MT': 0}

    for i in results:
        if "Benign" in i["CLNSIG"] and "Likely" not in i["CLNSIG"]:
            benign_dict[i["CHROM"]] += 1

        elif "Likely benign" in i["CLNSIG"]:
            likely_benign_dict[i["CHROM"]] += 1

        elif "Likely pathogenic" in i["CLNSIG"]:
            likely_pathogenic_dict[i["CHROM"]] += 1

        elif "Pathogenic" in i["CLNSIG"] and "Likely" not in i["CLNSIG"] and \
                "Conflicting" not in i["CLNSIG"]:
            pathogenic_dict[i["CHROM"]] += 1

    for i in results:
        if i["ML prediction"] == "0":
            predicted_benign_dict[i["CHROM"]] += 1
        elif i["ML prediction"] == "1":
            predicted_pathogenic_dict[i["CHROM"]] += 1

    global results_table_list
    results_table_list = [variation_length_dict, benign_dict,
                          likely_benign_dict, likely_pathogenic_dict,
                          pathogenic_dict, predicted_benign_dict,
                          predicted_pathogenic_dict]


@app.route('/calculator.html', methods=["POST", "GET"])
def calculator():
    """
    This function shows the info page when the user selects it in the
    menu bar on the webapplication. The info page contains information
    about the application

    :return render template: shows the calculator.html page to the user
    """
    # Returns the info page
    return render_template('calculator.html')


@app.route('/results.html', methods=["POST"])
def select_chromosome():
    JSON_dict = request.form['JSON_dict']
    JSON_dict = ast.literal_eval(JSON_dict)
    selected_chrom = request.form["chromosome_button"]
    JSON_graph = JSON_dict[selected_chrom]

    disable_button_dict = request.form['disable_button_dict']
    disable_button_dict = ast.literal_eval(disable_button_dict)

    return render_template("results.html", JSON_graph=JSON_graph,
                           JSON_dict=JSON_dict, selected_chrom=selected_chrom,
                           disable_button_dict=disable_button_dict,
                           results=results,
                           results_table_list=results_table_list)


@app.route('/disclaimer.html', methods=["POST", "GET"])
def disclaimer():
    """
    This function shows the info page when the user selects it in the
    menu bar on the webapplication. The info page contains information
    about the application

    :return render template: shows the calculator.html page to the user
    """
    # Returns the info page
    return render_template('disclaimer.html')


@app.route('/contact.html', methods=["POST", "GET"])
def submit_on_contact():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        message = request.form['message']
        email = request.form['email']
        gender = request.form['gender']
        phonenumber = request.form['phonenumber']

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["varpred"]
        mycol = mydb["contact"]

        mycol.insert_one(
            {
                "firstname": firstname,
                "lastname": lastname,
                "message": message,
                "email": email,
                "gender": gender,
                "phonenumber": phonenumber,
            }
        )

    return render_template('contact.html')


@app.route('/aboutvarpred.html', methods=["POST", "GET"])
def whoarewe():
    """
    This function shows the info page when the user selects it in the
    menu bar on the webapplication. The info page contains information
    about the application

    :return render template: shows the calculator.html page to the user
    """
    # Returns the info page
    return render_template('aboutvarpred.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
