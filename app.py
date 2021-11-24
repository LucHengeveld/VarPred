import ast

from flask import Flask, render_template, request
import pymongo
import dash
from dash import dcc
from dash import html
import plotly
import plotly.graph_objects as go
import json

app = Flask(__name__)


@app.route('/')
@app.route('/home.html', methods=["POST", "GET"])
def get_input():
    """
    This function retrieves the entered file from the webapplication, calls
    all other functions and renders the results page.

    :return render template: results.html
    """
    # If calculate results button is pressed:
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

                # Calls the function compare_dataset
                results = compare_dataset(compare_list)

                # Creates the visualisation bar
                JSON_dict, disable_button_dict = visualisation_bar(compare_list)
                # Returns the results page
                return render_template('results.html',
                                       results=results,
                                       JSON_dict=JSON_dict,
                                       disable_button_dict=disable_button_dict)

            else:
                # Returns an error if the file format is incorrect.
                return render_template('calculate.html',
                                       errormsg="Entered file has the wrong "
                                                "format")

        elif vcf_file_name != "":
            # Returns an error if a file with the wrong file extension
            # is entered on the webapplication.
            return render_template('calculate.html',
                                   errormsg="Entered file has the"
                                            " wrong file extension. Please enter a .vcf file")

        else:
            # Returns an error if no file is selected.
            return render_template('calculate.html', errormsg="No file "
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
            if line == "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n":
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


def compare_dataset(compare_list):
    """
    Compares the compare_list to the chromosome numbers and positions in the
    Mongo database.
    :param compare_list: List with all the chromosome numbers and positions out
     of the vcf_list
    :return results: List with data of the found mutations
    """
    # Connect to the local database
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["varpred"]
    mycol = mydb["variant"]

    # Create an empty list
    results = []

    # Saves the results in a list
    for simularity in mycol.find({"$and": [{"CHROM": {"$in": compare_list[0]}},
                                           {"POS": {"$in": compare_list[1]}},
                                           {"REF": {"$in": compare_list[2]}}, {
                                               "ALT": {
                                                   "$in": compare_list[3]}}]}):
        results.append(simularity)

    # for i in results:
    #     print(i)

    # Return the results list
    return results


def visualisation_bar(compare_list):
    # chromosome_dict = {"1": 248956422, "2": 242193529, "3": 198295559,
    #                    "4": 190214555, "5": 181538259, "6": 170805979,
    #                    "7": 159345973, "8": 145138636, "9": 138394717,
    #                    "10": 133797422, "11": 135086622, "12": 133275309,
    #                    "13": 114364328, "14": 107043718, "15": 101991189,
    #                    "16": 90338345, "17": 83257441, "18": 80373285,
    #                    "19": 58617616, "20": 64444167, "21": 46709983,
    #                    "22": 50818468, "X": 156040895, "Y": 57227415,
    #                    "MT": 16569}

    chromosome_list = [["1", 248956422], ["2", 242193529], ["3", 198295559],
                       ["4", 190214555], ["5", 181538259], ["6", 170805979],
                       ["7", 159345973], ["8", 145138636], ["9", 138394717],
                       ["10", 133797422], ["11", 135086622], ["12", 133275309],
                       ["13", 114364328], ["14", 107043718], ["15", 101991189],
                       ["16", 90338345], ["17", 83257441], ["18", 80373285],
                       ["19", 58617616], ["20", 64444167], ["21", 46709983],
                       ["22", 50818468], ["X", 156040895], ["Y", 57227415],
                       ["MT", 16569]]

    pos_list = []
    position_dict = {}

    for i in range(len(compare_list[0])):
        if i == 0:
            pos_list.append(int(compare_list[1][i]))

        elif compare_list[0][i] == compare_list[0][i - 1]:
            pos_list.append(int(compare_list[1][i]))
            if compare_list[1][i] == compare_list[1][-1]:
                position_dict[compare_list[0][i]] = pos_list

        elif compare_list[0][i] != compare_list[0][i - 1]:
            position_dict[compare_list[0][i - 1]] = pos_list
            pos_list = [int(compare_list[1][i])]
            if compare_list[1][i] == compare_list[1][-1]:
                position_dict[compare_list[0][i]] = pos_list

    JSON_dict = {}
    disable_button_dict = {}
    for i in range(len(chromosome_list)):
        try:
            y_list = []
            x_list = position_dict[chromosome_list[i][0]]
            for j in range(len(x_list)):
                y_list.append(0)
            disable_button_dict[chromosome_list[i][0]] = False
        except KeyError:
            x_list = []
            y_list = []
            disable_button_dict[chromosome_list[i][0]] = True

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_list, y=y_list,
            mode='markers', marker_size=42.5, marker_symbol='line-ns',
            marker_line_color="black", marker_line_width=2
        ))
        fig.update_xaxes(showgrid=False, fixedrange=False,
                         range=[0, chromosome_list[i][1]],
                         tickfont_family="Arial Black", tickformat=',d')
        fig.update_yaxes(showgrid=False, fixedrange=True,
                         zeroline=True, zerolinecolor='#04AA6D',
                         zerolinewidth=60,
                         showticklabels=False)
        fig.update_layout(height=260, plot_bgcolor='white', font_size=18)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        JSON_dict[chromosome_list[i][0]] = graphJSON

    return JSON_dict, disable_button_dict


@app.route('/calculate.html', methods=["POST", "GET"])
def calculate():
    """
    This function shows the info page when the user selects it in the
    menu bar on the webapplication. The info page contains information
    about the application

    :return render template: shows the calculate.html page to the user
    """
    # Returns the info page
    return render_template('calculate.html')


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
                           disable_button_dict=disable_button_dict)


@app.route('/disclaimer.html', methods=["POST", "GET"])
def disclaimer():
    """
    This function shows the info page when the user selects it in the
    menu bar on the webapplication. The info page contains information
    about the application

    :return render template: shows the calculate.html page to the user
    """
    # Returns the info page
    return render_template('disclaimer.html')


@app.route('/contact.html', methods=["POST", "GET"])
def submit_on_contact():
    """
    This function shows the info page when the user selects it in the
    menu bar on the webapplication. The info page contains information
    about the application

    :return render template: shows the calculate.html page to the user
    """
    # Returns the info page
    print("test")
    return render_template('contact.html')


@app.route('/aboutvarpred.html', methods=["POST", "GET"])
def whoarewe():
    """
    This function shows the info page when the user selects it in the
    menu bar on the webapplication. The info page contains information
    about the application

    :return render template: shows the calculate.html page to the user
    """
    # Returns the info page
    return render_template('aboutvarpred.html')


if __name__ == '__main__':
    app.run()
