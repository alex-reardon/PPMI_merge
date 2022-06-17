
from faulthandler import dump_traceback_later
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

## Merge in FA results 
def merge_dti_results(ppmi_merge, bucket, prefix, search_string, merge_on) : 
    print(f"Merge in {search_string}")
    dti = search_s3(bucket, prefix, search_string)
    client = boto3.client('s3', region_name="us-east-1")
    appended_data = []
    for key in dti : 
        subid = key.split('/')[2]
        subid = np.int64(subid)  
        date = key.split('/') [3]
        month_date = date[4:6] + '/' + date[0:4] 
        image_id = key.split('/')[5]
        csv_obj = client.get_object(Bucket='ppmi-dti', Key = key)
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_string))
        df.drop(['u_hier_id','u_hier_id.1'], axis = 1, inplace = True)
        df['Subject.ID'] = subid
        df['Event.ID.Date'] = month_date
        df['DTI.antspymm.Image.ID'] = image_id
        if 'md' in search_string : # FIXME- if you fix md labels you can get rid of this 
            df.columns = df.columns.str.replace("fa", "md") # FIXME - if you fix md labels you can get rid of this 
        appended_data.append(df)
    appended_data_dti = pd.concat(appended_data)


    ppmi_merge = pd.merge(ppmi_merge, appended_data_dti, on = merge_on, how = "outer")

    return ppmi_merge

ppmi_merge = merge_dti_results(ppmi_merge, 'ppmi-dti', 'antspymm/PPMI/', 'mean_fa_summary', ['Subject.ID', 'Event.ID.Date'])
ppmi_merge = merge_dti_results(ppmi_merge, 'ppmi-dti', 'antspymm/PPMI/', 'mean_md_summary', ['Subject.ID','Event.ID.Date', 'DTI.antspymm.Image.ID'])
ppmi_merge.to_csv('/Users/areardon/Desktop/ppmi_merge_test.csv')
eking

ppmi_merge['Event.ID.Date'] = ppmi_merge['Event.ID.Date'].astype(str)
ppmi_merge['Event.ID.Date'] = pd.to_datetime(ppmi_merge['Event.ID.Date'], errors = "ignore") # Change event.ID.Date column to date time so we can sort according to this
ppmi_merge = ppmi_merge.sort_values(by = ['Subject.ID','Event.ID.Date']) # Sort values by subject and event id date
ppmi_merge['Event.ID.Date'] = ppmi_merge['Event.ID.Date'].astype(str) # Change Event.ID.Date back to string so we can reformat
ppmi_merge.fillna('NA', inplace = True)

# Reformat Event.ID.Date from pd.to_datetime to month/year
for row_num in range(len(ppmi_merge['Event.ID.Date'])):
    if ppmi_merge['Event.ID.Date'].iloc[row_num] != 'NaT':
        split = ppmi_merge['Event.ID.Date'].iloc[row_num].split('-')
        new_date = split[1] +'/' + split[0] # month/year format
        ppmi_merge['Event.ID.Date'].iloc[row_num] = new_date
ppmi_merge['Event.ID.Date'] = ppmi_merge['Event.ID.Date'].replace('NaT','NA')

# Temp 
ppmi_merge.to_csv('/Users/areardon/Desktop/ppmi_merge_full.csv')
ppmi_merge = ppmi_merge.filter(regex='mean|Subject.ID|Image.Acquisition.Date|DTI.antspymm.Image.ID')
ppmi_merge.to_csv('/Users/areardon/Desktop/ppmi_merge_filtered.csv')

