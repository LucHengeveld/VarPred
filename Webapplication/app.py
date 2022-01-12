"""
Description:

Authors: Furkan Sengül, Inge van Vugt, Mark de Korte, Teun van Dorp, Erik Ma
    and Luc Hengeveld

Last updated: 11-01-2022
"""

# Imports the required packages for app.py
import ast
from flask import Flask, render_template, request
import pymongo

# Imports the python functions from other .py files
import file_checker as fc
import vcf_reader as vr
import compare_data as cd
import visualisation_bar as vb
import pathogenicity_table as pt
import heatmap as hm


"""
======================================================================================================================================================

Nog doen:
    Docstrings en commentaar voor:
        - app.py functies
        - app.py description bovenaan het bestand
    Bovenaan app.py description toevoegen
    Try / excepts toevoegen in app.py voor de error msgs (bv bij het niet
        invoeren van een bestand)


======================================================================================================================================================
"""
app = Flask(__name__)


@app.route('/')
@app.route('/home.html', methods=["POST", "GET"])
def main():
    """
    This function retrieves the entered file from the webapplication, calls
    all other functions and renders the results page.

    :return render template: results.html
    """
    # If calculator results button is pressed:
    if request.method == 'POST':
        correct_extension, vcf_file_name = fc.check_file_extension()

        if correct_extension:
            correct_format = fc.check_file_format(vcf_file_name)

            if correct_format:

                vcf_list = vr.vcf_to_list(vcf_file_name)

                # Calls the function create_compare_list
                compare_list = cd.create_compare_list(vcf_list)

                global results
                # Calls the function compare_dataset
                results, reference_build = cd.compare_dataset(compare_list)

                variant_dict = vb.variants(results)
                CLNSIG_dict = vb.clnsig_category(results)
                chromosome_lengths_list = vb.chromosome_lengths(
                    reference_build)
                JSON_dict, disable_button_dict = vb.graphs(
                    chromosome_lengths_list, variant_dict, CLNSIG_dict)

                global results_table_dict
                results_table_dict = pt.results_table(results, variant_dict)

                global color_dict
                color_dict = hm.heatmap(results_table_dict)

                # Returns the results page
                return render_template('results.html',
                                       results=results,
                                       JSON_dict=JSON_dict,
                                       disable_button_dict=disable_button_dict,
                                       results_table_dict=results_table_dict,
                                       color_dict=color_dict)

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


@app.route('/calculator.html', methods=["POST", "GET"])
def calculator():
    return render_template('calculator.html')


@app.route('/results.html', methods=["POST"])
def select_chromosome():
    JSON_dict = ast.literal_eval(request.form['JSON_dict'])
    JSON_graph = JSON_dict[request.form["chromosome_button"]]
    disable_button_dict = ast.literal_eval(request.form['disable_button_dict'])

    return render_template("results.html", JSON_graph=JSON_graph,
                           JSON_dict=JSON_dict,
                           selected_chrom=request.form["chromosome_button"],
                           disable_button_dict=disable_button_dict,
                           results=results,
                           results_table_dict=results_table_dict,
                           color_dict=color_dict)


@app.route('/disclaimer.html', methods=["POST", "GET"])
def disclaimer():
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

        myclient = pymongo.MongoClient("mongodb")
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
    return render_template('aboutvarpred.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
