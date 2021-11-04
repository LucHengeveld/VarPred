from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/home.html', methods=["POST", "GET"])
def get_input():
    if request.method == 'POST':

        try:
            vcf_file = request.files["vcf_file"]
            vcf_file_name = vcf_file.filename
            vcf_file.save(vcf_file_name)
        except:
            return render_template('home.html',
                                   vcf_file_name="No file selected.")

        return render_template('results.html',
                               vcf_file_name=vcf_file_name)

    else:
        return render_template('home.html',
                               vcf_file_name="")


@app.route('/info.html', methods=["POST", "GET"])
def info():
    return render_template('info.html')


if __name__ == '__main__':
    app.run()
