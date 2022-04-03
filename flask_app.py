from flask import Flask, make_response, request
import pandas as pd
import numpy as np
from processing import instant_runoff, single_transfer

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def file_summer_page():
    errors = ""
    if request.method == "POST":
        number = None
        try:
            number = int(request.form["number"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number"])
        input_file = request.files["input_file"]
        df = pd.read_csv(input_file)
        if number == 1:
            output_data = instant_runoff(df)
        else:
            output_data = single_transfer(number,df)
        response = make_response(output_data)
        response.headers["Content-Disposition"] = "attachment; filename=result.csv"
        return response

    return '''
        <html>
            <body>
                {errors}

                <p>Select the file you want to use (.csv):</p>
                <form method="post" action="." enctype="multipart/form-data">
                    <p><input type="file" name="input_file" /></p>
                    <p>Enter the number of seats available for the position:<p>
                    <p><input name="number" /></p>
                    <p><input type="submit" value="Get Results" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)
