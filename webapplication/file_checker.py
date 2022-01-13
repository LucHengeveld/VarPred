"""
This module retrieves the entered file, checks if the file extension is correct
and checks if the file is in the correct format
"""

from flask import request


def check_file_extension():
    """
    Retrieves the entered file, saves the name of the file as a string and
    checks if the file extension is correct.
    :return True: The boolean True if the file extension is correct.
    :return False: The boolean False if the file extension is incorrect.
    :return vcf_file_name: The name of the entered vcf file, only returns this
        variable if the entered file extension is correct.
    """
    # Retrieves the entered file from the webapplication
    vcf_file = request.files["vcf_file"]
    # Saves the file name to a string
    vcf_file_name = request.files["vcf_file"].filename

    # Checks if the filename ends with .vcf
    if vcf_file_name.endswith(".vcf"):

        # Saves the file if the file extension is correct
        vcf_file.save(vcf_file_name)

        # Returns the boolean True and the filename if the file
        # extension is correct
        return True, vcf_file_name
    else:
        # Returns false if the file extension is incorrect
        return False, vcf_file_name


def check_file_format(vcf_file_name):
    """
    Checks if the entered file has the correct format.
    :param vcf_file_name: Name of the entered vcf file from the webapplication.
    :return correct_vcf: Boolean which is True if the entered file format is
    correct.
    """
    # Creates a boolean with the value False
    correct_vcf = False

    # Reads the entered file line by line
    with open(vcf_file_name) as file:
        for line in file:

            # Checks if the file has the correct format
            if line.startswith("#CHROM\tPOS\tID\tREF\tALT"):

                # Changes the boolean to True if the format is correct
                # and stops the for loop
                correct_vcf = True
                break

            # Checks if the new line does not start with a #. Occurs
            # when the correct format has not been found
            if not line.startswith("#"):
                # Stops the for loop
                break

    # Closes the entered file
    file.close()

    # Returns the boolean
    return correct_vcf
