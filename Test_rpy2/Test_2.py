import os

os.environ["R_HOME"] = "C:\\Program Files\\R\\R-4.0.5"  # Your R version here 'R-4.0.3'
os.environ["R_USER"] = "C:\\Users\\Hoang\\Documents\\R\\win-library\\4.0"
os.environ["R_LIBS_USER"] = "C:\\Users\\Hoang\\Documents\\R\\win-library\\4.0"


# os.environ["R_LIBS_USER"] = "C:\\Program Files\\R\\R-4.0.5\\library"
# import rpy2.rinterface as rinterface
# rinterface.initr()
import rpy2
from rpy2 import situation
from rpy2.robjects.packages import importr
from rpy2 import robjects

if __name__ == '__main__':
    print("Hello")
    for row in rpy2.situation.iter_info():
        print(row)

    wb = importr('warbleR')
    # wb.
    print(wb)