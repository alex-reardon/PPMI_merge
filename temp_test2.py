from importlib.machinery import all_suffixes
from multiprocessing.dummy.connection import families
import pandas as pd
import boto3
import numpy as np
from io import StringIO # Python 3.x

local_dir = '/Users/areardon/Desktop/ppmi_merge/'
df = pd.read_csv(local_dir + 'temp_ppmi_merge.csv')
filter_col = [col for col in df if col.startswith('mean')]
new_df = df[filter_col]
new_df.to_csv('/Users/areardon/Desktop/fa616.csv')