import pandas as pd
import boto3
from io import StringIO 
import numpy as np


## Set up paths
userdir = '/Users/areardon/Desktop/Projects/PPMI_Merge3_20230920/'
version = 'v0.1.1'
datiq_path = userdir + 'datiq/'
invicro_data = userdir + 'invicro_data/'    
bucket = 'loni-data-curated-20230501'
prefix = 'ppmi_500_updated_cohort/processed/PPMI/'


 
def main() :
    ppmi_merge = pd.read_csv(userdir + 'ppmi_merge_clinical_' + version + '.csv')
    ppmi_merge = merge_mm(ppmi_merge, 'T1wHierarchical')
    ppmi_merge.to_csv(userdir + 'ppmi_merge_t1w_' + version + '.csv')
    ppmi_merge = merge_mm(ppmi_merge, 'DTI')
    ppmi_merge.to_csv(userdir + 'ppmi_merge_dti_' + version + '.csv')
    ppmi_merge.set_index('Subject.ID', inplace = True)
    ppmi_merge = ppmi_merge.loc[:, ~ppmi_merge.columns.str.startswith(tuple(['Unnamed']))]
    ppmi_merge.to_csv(userdir + 'ppmi_merge_clinical_imaging_' + version + '.csv')



def merge_mm(ppmi_merge, search_string) : 
    keys = search_s3(bucket, prefix, search_string, 'mmwide.csv')
    appended_data_df = process_s3_files(keys)
   
    ## Remove duplicate columns before merge 
    common_columns = appended_data_df.columns.intersection(ppmi_merge.columns)
    columns_to_exclude = ['Subject.ID', 'Event.ID.Date']    # Define columns to exclude from removal
    common_columns = common_columns.difference(columns_to_exclude) # Remove the excluded columns from the list of common columns
    appended_data_df = appended_data_df.drop(columns=common_columns)    # Drop the common columns from df1
    
    ## Merge 
    ppmi_merge_appended = pd.merge(ppmi_merge, appended_data_df, on = ['Subject.ID', 'Event.ID.Date'], how = "left")
    return ppmi_merge_appended



def process_s3_files(keys) : 
    client = boto3.client('s3', region_name="us-east-1")
    appended_data = []
    for key in keys :
        split = key.split('/')
        subid = np.int64(split[3])
        date = split[4]
        month_date = date[4:6] + '/' + date[0:4]
        csv_obj = client.get_object(Bucket=bucket, Key = key)
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_string))
        df.drop(['u_hier_id','u_hier_id.1'], axis = 1, inplace = True)
        df['Subject.ID'] = subid
        df['Event.ID.Date'] = month_date
        appended_data.append(df)
    appended_data_df = pd.concat(appended_data)
    return appended_data_df




def search_s3(bucket : str, prefix : str, search_string1 : str, search_string2 : str ):
    client = boto3.client('s3', region_name="us-east-1")
    paginator = client.get_paginator('list_objects')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
    keys = []
    for page in pages:
        contents = page['Contents']
        for c in contents:
            keys.append(c['Key'])
    if search_string1:
        keys = [key for key in keys if search_string1 in key]
    if search_string2:
        keys = [key for key in keys if search_string2 in key]
    return keys



### Haven't added yet 
def add_t1_mergewide(df, invicro_data) :
    #### T1 Info - Taylor's File ####
    ppmi_t1_df = pd.read_csv(invicro_data + 'ppmi_mergewide_t1.csv') # Read in Taylor's T1 results file
    ppmi_t1_df.rename(columns = {'u_hier_id_OR': 'Subject.ID'}, inplace = True) # Rename subject id column in Taylors df to match df

    # Create a column for object name to merge on with df
    ppmi_t1_df['Image_ID_merge'] = ''
    for row_num in range(len(ppmi_t1_df['ImageID'])) :
        image_id = ppmi_t1_df['ImageID'].iloc[row_num].split('-')[2]
        ppmi_t1_df['Image_ID_merge'].iloc[row_num] = image_id

    # Merge df_genetics  with t1 info
    df['Subject.ID'] = df['Subject.ID'].astype(float)
    ppmi_t1_df['Subject.ID'] = ppmi_t1_df['Subject.ID'].astype(float)
    df['Image_ID_merge'] = df['Image_ID_merge'].astype(str)
    ppmi_t1_df['Image_ID_merge'] = ppmi_t1_df['Image_ID_merge'].astype(str)
    df = pd.merge(df, ppmi_t1_df, on = ['Subject.ID','Image_ID_merge'], how = "left") # Merge
    df.drop(['Image_ID_merge'], axis = 1, inplace = True) # Drop
    return df



def get_full_ImageAcquisitionDate(df) :
    # Put full date in Image.Acquisition.Date column
    for row_num in range(len(df['T1.s3.Image.Name'])) :
        if isinstance(df['T1.s3.Image.Name'].iloc[row_num],str) :
            date = df['T1.s3.Image.Name'].iloc[row_num].split('-')[2]
            df['Image.Acquisition.Date'].iloc[row_num] = date[4:6] + '/' + date[6:8] +'/' + date[0:4]
    return df



def add_datiq(df, datiq_path):
    datiq = pd.ExcelFile(datiq_path + 'IQDAT_PPMI_PDHCproromalPD_12July2022_send.xlsx')

    # Read necessary sheets
    pd_datiq = pd.read_excel(datiq, 'PD').drop('#', axis=1)
    hc_datiq = pd.read_excel(datiq, 'HC').drop('#', axis=1)
    prodromal_datiq = pd.read_excel(datiq, 'prodromalPD').drop('#', axis=1)

    # Create 'Subject.ID' and 'INFODT' columns
    dfs = [pd_datiq, hc_datiq]
    for df in dfs:
        split_names = df['subjNames'].str.split('_', expand=True)
        df['Subject.ID'] = split_names[0]
        df['INFODT'] = split_names[1].str.split('-', expand=True)[0]

    # Fix prodromal dates
    prodromal_info = pd.read_csv(datiq_path + 'DATIQ_results_ver2_prodromalPD_IDsheets.csv')
    prodromal_info['INFODT'] = pd.to_datetime(prodromal_info['ScanDate'], format='%d-%b-%y').dt.strftime('%Y%m')
    prodromal_info.rename(columns={'FullFilename': 'subjNames'}, inplace=True)
    prodromal_datiq = pd.merge(prodromal_datiq, prodromal_info[['subjNames', 'INFODT']], how='outer', on='subjNames')
    prodromal_datiq['Subject.ID'] = prodromal_datiq['subjNames'].str.split('_').str[2]
    prodromal_datiq.drop('subjNames', axis=1, inplace=True)

    # Add Enroll.Diagnosis column
    prodromal_datiq['Enroll.Diagnosis'] = 'Prodromal'
    hc_datiq['Enroll.Diagnosis'] = 'Healthy Control'
    pd_datiq['Enroll.Diagnosis'] = "Parkinson's Disease"

    # Define column order and reindex
    column_order = ['Subject.ID', 'INFODT', 'Enroll.Diagnosis', 'DATLoad(%)', 'DATLoadLeft(%)' , 'DATLoadRight(%)']
    dfs = pd.concat([prodromal_datiq, hc_datiq, pd_datiq]).reindex(columns=column_order)
    dfs.rename(columns = {'DATLoad(%)' :'DATLoad.Percent', 'DATLoadLeft(%)':'DATLoadLeft.Percent' , 'DATLoadRight(%)':'DATLoadRight.Percent'}, inplace = True)
    
    dfs['INFODT'] = dfs['INFODT'].str[4:6] + '/' + dfs['INFODT'].str[0:4]
    dfs['Subject.ID'] = dfs['Subject.ID'].astype(int)

    df = pd.merge(df, dfs, how='outer', on=['Subject.ID', 'INFODT', 'Enroll.Diagnosis'])
    df.fillna('NA', inplace=True)
    return df



def add_BA_qc(invicro_data, df) : 
    ppmi_qc_BA = pd.read_csv(invicro_data + 'ppmi_qc_BA.csv')
    ppmi_qc_BA = ppmi_qc_BA.reset_index(drop = False) # Move index to first column so we can rename
    ppmi_qc_BA.rename(columns = {'ID' : 'ImageID'}, inplace = True) # Rename ImageID
    
    # Update ImageID column bc info from T1 file (where ImageID was created from) does not contain all the files from s3 (need this to merge in subs from QC csv)
    for row_num in range(len(df['ImageID'])) :
        if isinstance(df['T1.s3.Image.Name'].iloc[row_num], str):
            imageID = df['T1.s3.Image.Name'].iloc[row_num].split('.')[0] # take info before .nii.gz
            df['ImageID'].iloc[row_num] = imageID.split('-')[1] + '-' + imageID.split('-')[2] + '-' + imageID.split('-')[4]
            
    #ppmi_qc_BA['ImageID'] = ppmi_qc_BA['ImageID'].astype(float)
    df = pd.merge(df, ppmi_qc_BA, on = ['ImageID'], how = "left") # Merge - keep only from ImageIDs we already have
    return df



def isNaN(num):
    return num != num



def add_bestEventID_resnet(df) :
    ## Inlcude columns for bestEventID (bestScreening, bestBaseline, etc) and denote the highest resnetGrade with True (else = False)
    myevs = df['Event.ID'].unique() # Unique event ids
    uids = df['Subject.ID'].unique() # Unique subject ids
    for myev in myevs :
        if not isNaN(myev) :
            mybe = "best" + myev # Create best Visit column
            df[mybe] = False # Set all best visit to be False
            for u in uids :
                selu = df.loc[(df['Subject.ID'] == u) & (df['Event.ID'] == myev) & (df['resnetGrade'].notna())] # For one subject at one event id if resnetGrade not na
                if len(selu) == 1 : # If there is one event id for that subject
                    idx = selu.index # Ge the index
                    df.loc[idx, mybe] = True
                if len(selu) > 1 : # IF there is more than one event id for that subject and resnet grade is not na
                    maxidx = selu[['resnetGrade']].idxmax() # Get the higher resnetGrade for each visit if there are more than one
                    df.loc[maxidx, mybe] = True
    return df



def add_bestImageAcquisitionDate(df) :
    """
    Include a column for bestAtImage.Acquisition.Date - denote the one or highest resnetGrade with True (else = False)
    """
    df['bestAtImage.Acquisition.Date'] = False # Initialize bestAtImage.Acuqisition.Date col
    myevs = df['Event.ID'].unique() # Unique event ids
    uids = df['Subject.ID'].unique() # Unique subject ids
    for myev in myevs :
        for u in uids :
            selu = df.loc[(df['Subject.ID'] == u) & (df['Event.ID'] == myev) & (df['resnetGrade'].notna())]
            if len(selu) == 1 : # If there is one event id for that subject
                idx = selu.index # Get the index
                df.loc[idx, 'bestAtImage.Acquisition.Date'] = True
            if len(selu) > 1 : # IF there is more than one event id for that subject and resnet grade is not na
                maxidx = selu[['resnetGrade']].idxmax() # Get the higher resnetGrade for each visit if there are more than one
                df.loc[maxidx, 'bestAtImage.Acquisition.Date'] = True
    return df






if __name__=="__main__":
    main()          

