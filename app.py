from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/home.html', methods=["POST", "GET"])
def get_input():
    if request.method == 'POST':

        vcf_file = request.files["vcf_file"]
        vcf_file_name = vcf_file.filename

        if vcf_file_name.endswith(".vcf"):
            vcf_file.save(vcf_file_name)
            return render_template('results.html',
                                   vcf_file_name=vcf_file_name)

        elif vcf_file_name != "":
            return render_template('home.html', errormsg="Entered file has the"
                            " wrong file extension. Please enter a .vcf file")

        else:
            return render_template('home.html', errormsg="No file "
                                                              "selected.")

    else:
        return render_template('home.html',
                               errormsg="")


@app.route('/info.html', methods=["POST", "GET"])
def info():
    return render_template('info.html')


if __name__ == '__main__':
    app.run()
