import pandas as pd
print(pd.__version__)
pd.Series(['San Francisco', 'San Jose', 'Sacramento'])
california_housing_dataframe = pd.read_csv("https://storage.googleapis.com/mledu-datasets/california_housing_train.csv", sep=",")
california_housing_dataframe.describe()