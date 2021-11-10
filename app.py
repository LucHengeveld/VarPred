from flask import Flask, render_template, request
import pymongo

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


@app.route('/info.html', methods=["POST", "GET"])
def info():
    """
    This function shows the info page when the user selects it in the
    menu bar on the webapplication. The info page contains information
    about the application

    :return render template: shows the info.html page to the user
    """
    # Returns the info page
    return render_template('info.html')

@app.route('/disclaimer.html', methods=["POST", "GET"])
def disclaimer():
    """
    This function shows the info page when the user selects it in the
    menu bar on the webapplication. The info page contains information
    about the application

    :return render template: shows the info.html page to the user
    """
    # Returns the info page
    return render_template('disclaimer.html')

@app.route('/contact.html', methods=["POST", "GET"])
def contact():
    """
    This function shows the info page when the user selects it in the
    menu bar on the webapplication. The info page contains information
    about the application

    :return render template: shows the info.html page to the user
    """
    # Returns the info page
    return render_template('contact.html')

@app.route('/aboutvarpred.html', methods=["POST", "GET"])
def whoarewe():
    """
    This function shows the info page when the user selects it in the
    menu bar on the webapplication. The info page contains information
    about the application

    :return render template: shows the info.html page to the user
    """
    # Returns the info page
    return render_template('aboutvarpred.html')

if __name__ == '__main__':
    app.run()
