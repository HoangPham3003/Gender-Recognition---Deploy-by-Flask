from flask import Flask, render_template, url_for, request, jsonify
import os
os.environ["R_HOME"] = "C:\\PROGRA~1\\R\\R-40~1.5"  # Your R version here 'R-4.0.3'
os.environ["R_USER"] = "C:\\Users\\Hoang\\Documents"
os.environ["R_LIBS_USER"] = "C:\\Users\\Hoang\\Documents\\R\\win-library\\4.0"
import pandas as pd
from rpy2 import robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri
pandas2ri.activate()
import pickle
import numpy as np


app = Flask(__name__)
wb = importr('warbleR')
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# test = ro.r('''
#
# test <- gsub("to", "",''' + app.config['UPLOAD_FOLDER'] + ''')
#
# ''')

print('=================== load model')
loaded_model = pickle.load(open('.\\Notebooks\\myModelFile', 'rb'))


def feature_extract(input_path):
    # print(os.getcwd())
    x = {
        "sound.files": ['input.wav'],
        "selec": 1000,
        "start": 0,
        "end": 5,  # Duration = 20
        "bottom.freq": 3.,
        "top.freq": 10.
    }

    X = pd.DataFrame(data=x)
    print(X.head())
    print('='*20)

    # Dataframe in python to R
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     r_from_pd = ro.conversion.py2rpy(X)

    with localconverter(ro.default_converter + pandas2ri.converter):
        r_from_pd = ro.conversion.py2rpy(X)

    # wb = importr('warbleR')
    print(wb)
    # spec = wb.specan(X=r_from_pd, harmonicity=True, path=app.config['UPLOAD_FOLDER'])
    spec = wb.spectro_analysis(X=r_from_pd, harmonicity=ro.vectors.BoolVector([True]))
    print(spec)

    # Dataframe from R to python
    with localconverter(ro.default_converter + pandas2ri.converter):
        pd_from_r = ro.conversion.rpy2py(spec)

    myData = pd_from_r[['meanfreq', 'sd', 'freq.median', 'freq.Q25', 'freq.IQR', 'sp.ent', 'sfm', 'meanfun', 'minfun', 'maxfun',
         'meandom', 'mindom', 'maxdom', 'dfrange']]
    myData.insert(7, 'mode', [0.165248])
    myData.insert(8, 'centroid', [0.180886])


    X_test = np.asanyarray(myData.values, dtype='object')
    X_test = X_test.reshape((1, 16))
    return X_test


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # file_path = os.path.join(app.config['UPLOAD_FOLDER'], "input.wav")
            file_path = os.path.join("", "input.wav")
            file.save(file_path)
            abs_path = os.path.abspath(file_path)
            feature = feature_extract(abs_path)
            result = loaded_model.predict(feature).tolist()
            # print(result)
            return jsonify(data=[result[0]])

    return render_template("layout_2.html")


if __name__ == '__main__':
    app.run(debug=True)