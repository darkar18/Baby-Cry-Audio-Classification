import os
import pandas as pd
from my_code_lib import DataAugment as DA
DATA,DIR = DA.DATA,DA.DIR
dirs = DA.list_of_classes
class DataFramer():
    def returnData():
        data = pd.DataFrame(columns=["name","label"])
        # Adding data to dataframe
        for i in range(0,5) :
            label=i
            for _,_,f in os.walk(os.path.join(DATA,dirs[i])):
                for file in f:
                    tuple = pd.DataFrame([{"name":os.path.join(dirs[i],file),"label":label}])
                    data = pd.concat([data,tuple]) 
        return data