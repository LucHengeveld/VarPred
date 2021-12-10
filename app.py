import ast
from flask import Flask, render_template, request
import pymongo
import dash
from dash import dcc
from dash import html
import plotly
import plotly.graph_objects as go
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

                # Calls the function create_ID_list
                ID_list = create_ID_list(vcf_list)

                # Calls the function compare_dataset
                results = compare_dataset(ID_list)

                # Returns the results page
                return render_template('results.html',
                                       vcf_file_name=vcf_file_name)
                results = compare_dataset(compare_list)

                # Creates the visualisation bar
                JSON_dict, disable_button_dict = visualisation_bar(results)
                # Returns the results page
                return render_template('results.html',
                                       results=results,
                                       JSON_dict=JSON_dict,
                                       disable_button_dict=disable_button_dict)

            else:
                # Returns an error if the file format is incorrect.
                return render_template('home.html',
                                       errormsg="Entered file has the wrong format")

        elif vcf_file_name != "":
            # Returns an error if a file with the wrong file extension
            # is entered on the webapplication.
            return render_template('home.html', errormsg="Entered file has the"
                                                         " wrong file extension. Please enter a .vcf file")

        else:
            # Returns an error if no file is selected.
            return render_template('home.html', errormsg="No file "
                                                         "selected.")

    else:
        # Returns the standard home page.
        return render_template('home.html',
                               errormsg="")


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


def create_ID_list(vcf_list):
    """
    This functions retrieves all ID's from the entered vcf file and adds it to
    a list.
    :param vcf_list: List with the structure [CHROM, POS, ID, REF, ALT, QUAL,
    FILTER, INFO]
    :return: ID_list: List with all the ID's out of the vcf_list
    """
    # Creates an empty list
    ID_list = []

    # Loops through the vcf list and saves the ID's to the ID_list
    for i in vcf_list:
        ID_list.append(int(i[2]))

    # Returns the ID_list
    return ID_list


def compare_dataset(ID_list):
    """
    Compares the ID_list to the ID's in the Mongo database.
    :param ID_list: List with all the ID's out of the vcf_list
    :return results: List with data of the found mutations
    """
    # Connect to the local database
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["varpred"]
    mycol = mydb["variant"]

    # Create an empty list
    results = []

    # Saves the results in a list
    for simularity in mycol.find({"ID": {"$in": ID_list}}):
        results.append(simularity)

    # Return the results list
    return results



@app.route('/calculator.html', methods=["POST", "GET"])
def visualisation_bar(results):
    chromosome_list = [["1", 248956422], ["2", 242193529], ["3", 198295559],
                       ["4", 190214555], ["5", 181538259], ["6", 170805979],
                       ["7", 159345973], ["8", 145138636], ["9", 138394717],
                       ["10", 133797422], ["11", 135086622], ["12", 133275309],
                       ["13", 114364328], ["14", 107043718], ["15", 101991189],
                       ["16", 90338345], ["17", 83257441], ["18", 80373285],
                       ["19", 58617616], ["20", 64444167], ["21", 46709983],
                       ["22", 50818468], ["X", 156040895], ["Y", 57227415],
                       ["MT", 16569]]

    position_dict = {}
    mutation_dict = {}
    pos_list = []
    ref_list = []
    alt_list = []

    for i in range(len(results)):
        if i == 0:
            pos_list.append(results[i]["POS"])
            ref_list.append(results[i]["REF"])
            alt_list.append(results[i]["ALT"])

        elif results[i]["CHROM"] == results[i - 1]["CHROM"]:
            pos_list.append(int(results[i]["POS"]))
            ref_list.append(results[i]["REF"])
            alt_list.append(results[i]["ALT"])

            if results[i]["POS"] == results[-1]["POS"]:
                position_dict[results[i]["CHROM"]] = pos_list
                mutation_dict[results[i]["CHROM"]] = {"REF": ref_list,
                                                      "ALT": alt_list}

        elif results[i]["CHROM"] != results[i - 1]["CHROM"]:
            position_dict[results[i - 1]["CHROM"]] = pos_list
            mutation_dict[results[i - 1]["CHROM"]] = {"REF": ref_list,
                                                      "ALT": alt_list}

            pos_list = [int(results[i]["POS"])]
            ref_list = [(results[i]["REF"])]
            alt_list = [(results[i]["ALT"])]

            if results[i]["POS"] == results[-1]["POS"]:
                position_dict[results[i]["CHROM"]] = pos_list
                mutation_dict[results[i - 1]["CHROM"]] = {"REF": ref_list,
                                                          "ALT": alt_list}

    # print(mutation_dict)
    # for key in mutation_dict.keys():
    #     print(str(key) + "\t\t" + str(mutation_dict[key]))

    JSON_dict = {}
    disable_button_dict = {}
    for i in range(len(chromosome_list)):
        try:
            y_list = []
            x_list = position_dict[chromosome_list[i][0]]
            for j in range(len(x_list)):
                y_list.append(0)
            disable_button_dict[chromosome_list[i][0]] = False

            df = pd.DataFrame(data=mutation_dict[chromosome_list[i][0]])
            fig = px.scatter(df, x=x_list, y=y_list,
                             labels={"x": "Position",
                                     "y": ""},
                             custom_data=["REF", "ALT"])
            fig.update_traces(marker=dict(size=42.5,
                                          symbol='line-ns',
                                          line=dict(width=2,
                                                    color='black')),
                              hovertemplate=
                              '<b>Positie: %{x}' +
                              '<br>REF > ALT: %{customdata[0]} > %{customdata[1]}</b>'
                              '<extra></extra>',
                              selector=dict(mode='markers'))

            fig.update_xaxes(showgrid=False, fixedrange=False,
                             range=[0, chromosome_list[i][1]],
                             tickfont_family="Arial Black", tickformat=',d')
            fig.update_yaxes(showgrid=False, fixedrange=True,
                             zeroline=True, zerolinecolor='#04AA6D',
                             zerolinewidth=60,
                             showticklabels=False)
            fig.update_layout(height=260, plot_bgcolor='white', font_size=18,
                              hoverlabel=dict(
                                  bgcolor='#e6ffe6',
                                  font_size=22,
                                  font_family="Courier",
                                  font_color="black"
                              ))
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            JSON_dict[chromosome_list[i][0]] = graphJSON

        except KeyError:
            disable_button_dict[chromosome_list[i][0]] = True

    return JSON_dict, disable_button_dict, render_template('calculator.html')


# @app.route('/calculate.html', methods=["POST", "GET"])
# def calculate():
#     """
#     This function shows the info page when the user selects it in the
#     menu bar on the webapplication. The info page contains information
#     about the application
#
#     :return render template: shows the calculator.html page to the user
#     """
#     # Returns the info page
#     return render_template('calculator.html')


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
    # Returns the info page
    return render_template('aboutvarpred.html')


if __name__ == '__main__':
    app.run()
