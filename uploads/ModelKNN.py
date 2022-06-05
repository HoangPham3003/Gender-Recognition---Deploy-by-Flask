import pandas as pd
from rpy2 import robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri
from rpy2.robjects import numpy2ri
from rpy2.robjects import r
import anndata2ri
import rpy2
from sklearn import preprocessing
import pickle
import numpy as np


anndata2ri.activate()
pandas2ri.activate()

def Predict():
    x = {
        "sound.files": ["input.wav"],
        "selec": 1000,
        "start": 0,
        "end": 5,      # Duration = 20
        "bottom.freq": 3.,
        "top.freq": 10.
    }

    X = pd.DataFrame(data=x)
    # print(X)
    # print()

    # Dataframe in python to R
    with localconverter(ro.default_converter + pandas2ri.converter):
        r_from_pd = ro.conversion.py2rpy(X)


    wb = importr('warbleR')
    # at = wb.autodetec(X=r_from_pd)

    # print(at)
    # print()
    spec = wb.specan(X=r_from_pd, harmonicity=True)
    # print(spec)


    with localconverter(ro.default_converter + pandas2ri.converter):
        pd_from_r = ro.conversion.rpy2py(spec)


    # print(pd_from_r)
    # print(pd_from_r['duration'].values)
    # print(pd_from_r.columns)
    # print()
    # print(pd_from_r.iloc[0].values)
    # print()
    # print()


    # meanfreq = pd_from_r[['meanfreq']].values
    # print(meanfreq)
    myData = pd_from_r[['meanfreq', 'sd', 'freq.median', 'freq.Q25', 'freq.IQR', 'sp.ent', 'sfm', 'meanfun', 'minfun', 'maxfun', 'meandom', 'mindom', 'maxdom', 'dfrange']]
    myData.insert(7, 'mode', [0.165248])
    myData.insert(8, 'centroid', [0.180886])
    # print(myData)
    # print(myData.keys())
    # print()


    X_test = np.asanyarray(myData.values, dtype='object')
    X_test = X_test.reshape((1, 16))
    # print(X_test)
    # print(X_test.shape)
    # print(type(X_test))


    # Load model
    loaded_model = pickle.load(open('..\\Notebooks\\myModelFile', 'rb'))
    result = loaded_model.predict(X_test)
    return result
    # print(result)
    # print()

if __name__ == '__main__':
    Predict()



