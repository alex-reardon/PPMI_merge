from importlib.machinery import all_suffixes
import pandas as pd
import boto3
import numpy as np
from io import StringIO # Python 3.x

local_dir = '/Users/areardon/Desktop/ppmi_merge/'

def search_s3(bucket, prefix, search_string):
    client = boto3.client('s3', region_name="us-east-1")
    paginator = client.get_paginator('list_objects')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
    keys = []
    for page in pages:
        contents = page['Contents']
        for c in contents:
            keys.append(c['Key'])
    if search_string:
        keys = [key for key in keys if search_string in key]
    return keys

ppmi_merge = pd.read_csv(local_dir + 'ppmi_merge_v0.0.4.csv')

## Get FA and merge into ppmi_merge
fa = search_s3('ppmi-dti', 'antspymm/PPMI/', 'mean_fa_summary') # Search s3 for mean_fa_summary.csv
client = boto3.client('s3', region_name="us-east-1")
appended_data = []
for key in fa : 
    subid = key.split('/')[2]
    subid = np.int64(subid)  
    date = key.split('/') [3]
    month_date = date[4:6] + '/' + date[6:8] + '/' + date[0:4] 
    csv_obj = client.get_object(Bucket='ppmi-dti', Key = key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    df.drop(['u_hier_id','u_hier_id.1'], axis = 1, inplace = True)
    df['Subject.ID'] = subid
    df['Image.Acquisition.Date'] = month_date
    appended_data.append(df)
appended_data_fa = pd.concat(appended_data)

# Merge FA into ppmi_merge
ppmi_merge = pd.merge(ppmi_merge, appended_data_fa, on = ['Subject.ID', 'Image.Acquisition.Date'], how = "outer")
ppmi_merge_temp = ppmi_merge[['Subject.ID', 'Image.Acquisition.Date','mean_fa-anterior_corona_radiata-left-jhu_icbm_labels_1mm']]

    
## Get MD and merge into ppmi_merge
md = search_s3('ppmi-dti', 'antspymm/PPMI/', 'mean_md_summary') # Search s3 for mean_fa_summary.csv
client = boto3.client('s3', region_name="us-east-1")
appended_data = []
for key in md : 
    subid = key.split('/')[2]
    subid = np.int64(subid)  
    date = key.split('/') [3]
    month_date = date[4:6] + '/' + date[6:8] + '/' + date[0:4] 
    csv_obj = client.get_object(Bucket='ppmi-dti', Key = key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    df.drop(['u_hier_id','u_hier_id.1'], axis = 1, inplace = True)
    df['Subject.ID'] = subid
    df['Image.Acquisition.Date'] = month_date
    appended_data.append(df)
appended_data_md = pd.concat(appended_data)

# Merge FA into ppmi_merge
ppmi_merge = pd.merge(ppmi_merge, appended_data_md, on = ['Subject.ID', 'Image.Acquisition.Date'], how = "outer")
ppmi_merge.to_csv(local_dir + 'temp_ppmi_merge.csv')


