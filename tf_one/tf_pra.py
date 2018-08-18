from __future__ import print_function
import math

from IPython import display
from matplotlib import cm
from matplotlib import gridspec
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn import metrics
import tensorflow as tf
from tensorflow.python.data import Dataset

tf.logging.set_verbosity(tf.logging.ERROR)
pd.options.display.max_rows =0
pd.options.display.float_format = '{:.1f}'.format

california_housing_dataframe = pd.read_csv("/home/alexhowe/Downloads/california_housing_train.csv",sep=',')

california_housing_dataframe = california_housing_dataframe.reindex(np.random.permutation(california_housing_dataframe.index))

california_housing_dataframe["median_house_value"]/=1000.0
california_housing_dataframe
california_housing_dataframe.describe()
