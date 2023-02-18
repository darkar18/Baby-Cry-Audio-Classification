import DataLoader as dl

data = dl.DataFramer()
data= data.returnData()
print(data)
print(data.__getitem__(3))