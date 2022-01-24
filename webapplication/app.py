"""
Description: The webapplication visualises and annotates variants from a
    vcf-file. This is done by comparing the entered vcf-file with a clinvar
    dataset. A machine learning algorithm will predict the variants with an
    uncertain clinical significance.

Authors: Furkan Sengül, Inge van Vugt, Mark de Korte, Teun van Dorp, Erik Ma
    and Luc Hengeveld.

Last updated: 24-01-2022
"""

# Imports the required packages for app.py
import ast
from flask import Flask, render_template, request
import pymongo

# Imports the python functions from other .py files
from lib import file_checker as fc
from lib import vcf_reader as vr
from lib import compare_data as cd
from lib import visualisation_bar as vb
from lib import pathogenicity_table as pt
from lib import heatmap as hm


app = Flask(__name__)


@app.route('/')
@app.route('/home.html', methods=["POST", "GET"])
def main():
    """
    Main function of the webapplication. It calls the different functions that
        are required to calculate the results and returns the different html
        templates.
    :return render_template: Returns a html template. Could contain some extra
        python variables for the results page or an string with an error
        message incase an error occurs.
    """
    # Checks if the calculate results button is pressed on the
    # calculator page
    if request.method == 'POST':

        # Calls the function check_file_extension from file_checker.py
        correct_extension, vcf_file_name = fc.check_file_extension()

        # If the file has the correct extension, it checks the format in
        # the entered file
        if correct_extension:
            # Calls the function check_file_format from file_checker.py
            correct_format = fc.check_file_format(vcf_file_name)

            # Checks if the file format is correct
            if correct_format:

                # Calls the function vcf_to_list from vcf_reader.py
                vcf_list = vr.vcf_to_list(vcf_file_name)

                # Calls the function create_compare_list from
                # compare_data.py
                compare_list = cd.create_compare_list(vcf_list)

                # Makes the results variable global, so it can be used
                # in @app.route('/results.html')
                global results

                # Calls the function compare_dataset from
                # compare_data.py
                results, reference_build = cd.compare_dataset(compare_list)

                # Calls the function variants from visualisation_bar.py
                variant_dict = vb.variants(results)

                # Calls the function clnsig_category from
                # visualisation_bar.py
                CLNSIG_dict = vb.clnsig_category(results)

                # Calls the function chromosome_lengths from
                # visualisation_bar.py
                chromosome_lengths_list = vb.chromosome_lengths(
                    reference_build)

                # Calls the function graphs from visualisation_bar.py
                JSON_dict, disable_button_dict = vb.graphs(
                    chromosome_lengths_list, variant_dict, CLNSIG_dict)

                # Makes the results_table_dict variable global, so it
                # can be used in @app.route('/results.html')
                global results_table_dict

                # Calls the function results_table from
                # pathogenicity_table.py
                results_table_dict = pt.results_table(results, variant_dict)

                # Makes the color_dict variable global, so it can be
                # used in @app.route('/results.html')
                global color_dict

                # Calls the function heatmap from heatmap.py
                color_dict = hm.heatmap(results_table_dict)

                # Returns the results page with some variables
                return render_template('results.html',
                                       results=results,
                                       JSON_dict=JSON_dict,
                                       disable_button_dict=disable_button_dict,
                                       results_table_dict=results_table_dict,
                                       color_dict=color_dict)

            else:
                # Returns an error if the file format is incorrect
                return render_template('calculator.html',
                                       errormsg="Entered file has the wrong "
                                                "format")

        elif vcf_file_name != "":
            # Returns an error if a file with the wrong file extension
            # has been entered on the webapplication
            return render_template('calculator.html',
                                   errormsg="Entered file has the "
                                            "wrong file extension. Please "
                                            "enter a .vcf file")

        else:
            # Returns an error if no file is selected
            return render_template('calculator.html', errormsg="No file "
                                                               "selected.")

    else:
        # Returns the standard home page
        return render_template('home.html')


@app.route('/calculator.html', methods=["POST", "GET"])
def calculator():
    """
    Function that returns the calculator html template when clicked in the menu
        bar.
    :return render_template: Returns the calculator html template.
    """

    # Returns the calculator.html page
    return render_template('calculator.html')


@app.route('/results.html', methods=["POST"])
def select_chromosome():
    """
    Retrieves and shows the correct graph when a different chromosome has been
        selected on the results page.
    :return render_template: Returns a html template and some extra
        python variables for the results page.
    """
    JSON_dict = ast.literal_eval(request.form['JSON_dict'])
    JSON_graph = JSON_dict[request.form["chromosome_button"]]
    disable_button_dict = ast.literal_eval(request.form['disable_button_dict'])

    # Returns the results page with some variables
    return render_template("results.html", JSON_graph=JSON_graph,
                           JSON_dict=JSON_dict,
                           selected_chrom=request.form["chromosome_button"],
                           disable_button_dict=disable_button_dict,
                           results=results,
                           results_table_dict=results_table_dict,
                           color_dict=color_dict)


@app.route('/disclaimer.html', methods=["POST", "GET"])
def disclaimer():
    """
    Function that returns the disclaimer html template when clicked in the menu
        bar.
    :return render_template: Returns the disclaimer html template.
    """

    # Returns the disclaimer.html page
    return render_template('disclaimer.html')


@app.route('/contact.html', methods=["POST", "GET"])
def submit_on_contact():
    """
    Retrieves and saves the entered contact form fields to the database.
    :return render_template: Returns the contact html template.
    """
    # Checks if the submit form button has been clicked
    if request.method == "POST":

        # Retrieves the entered contact form fields from the
        # contact.html page
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        message = request.form['message']
        email = request.form['email']
        gender = request.form['gender']
        phonenumber = request.form['phonenumber']

        # Connects to the Mongo database
        client = pymongo.MongoClient("mongodb")
        db = client["varpred"]
        col = db["contact"]

        # Inserts the retrieved data into the Mongo database
        col.insert_one(
            {
                "firstname": firstname,
                "lastname": lastname,
                "message": message,
                "email": email,
                "gender": gender,
                "phonenumber": phonenumber,
            }
        )

    # Returns the contact.html page
    return render_template('contact.html')


@app.route('/aboutvarpred.html', methods=["POST", "GET"])
def whoarewe():
    """
    Function that returns the aboutvarpred html template when clicked in the
        menu bar.
    :return render_template: Returns the aboutvarpred html template.
    """

    # Returns the aboutvarpred.html page
    return render_template('aboutvarpred.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
