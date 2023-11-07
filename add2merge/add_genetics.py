import pandas as pd
import numpy as np
from typing import List


# Set up paths and load in data 
userdir = '/Users/areardon/Desktop/Projects/PPMI_Merge3_20230920/'
genetics_path = userdir + 'genetic_data/'
version = 'v0.1.1'
ppmi_merge = pd.read_csv(userdir + 'ppmi_merge_clinical_imaging_' + version + '.csv')


def main() :    
    add_genetics_info(ppmi_merge)
    
    

def add_genetics_info(ppmi_merge) : 
    # Format genetics info 
    lrrk2_formatted = format_genetics_df('lrrk2_geno_012_mac5_missing_geno.csv')
    scna_formatted = format_genetics_df('scna_geno_012_mac5_missing_geno.csv')
    apoe_formatted = format_genetics_df('apoe_geno_012_mac5_missing_geno.csv')
    tmem_formatted = format_genetics_df('tmem175_geno_012_mac5_missing_geno.csv')
    gba_formatted = format_genetics_df('gba_geno_012_mac5_missing_geno.csv')
    genetics_df = merge_multiple_dfs([lrrk2_formatted, scna_formatted, apoe_formatted, tmem_formatted, gba_formatted], on = ["Subject.ID"], how = "outer")

    # Merge genetics df with ppmi_merge clinical df 
    ppmi_merge = pd.merge(ppmi_merge, genetics_df, on = 'Subject.ID', how = "outer")
    ppmi_merge = add_snp_recode(ppmi_merge)## Add in Brian's snp_rs6265_recode.csv file sent on slack 6/29/22
    ppmi_merge.set_index('Subject.ID', inplace = True)
    ppmi_merge.to_csv(userdir + 'ppmi_merge_clinical_imaging_genetics_' + version + '.csv')
    return ppmi_merge



def format_genetics_df(csv_filename) :
    """
    Format genetics_df to make merge-able with ppmi_merge
    """
    genetics_df = read_and_transform_data(csv_filename, ['COUNTED', 'ALT', 'SNP', '(C)M'] , drop=True)
    
    # Change column names to be just subid
    for col in genetics_df:
        if '_' in col :
            subid = int(col.split('_')[-1])
            genetics_df.rename(columns = {col : subid}, inplace = True)
            
    # Combine CHR and POS columns
    genetics_df['CHR'] = 'CHR' + genetics_df['CHR'].astype(str) # Need to be strings before you use merge_columns function
    genetics_df['POS'] = 'POS' + genetics_df['POS'].astype(str) # Need to be strings before you use merge_columns function
    genetics_df = merge_columns(genetics_df, ['CHR', 'POS'], 'Chromosome.Position', '.')
    
    # Pivot df so position is column name and subid is row
    genetics_df = genetics_df.T # Transpose df so that rows are subid
    genetics_df.rename(columns = genetics_df.iloc[-1], inplace = True) # Move Chr.Pos to column names
    genetics_df.index.names = ['Subject.ID'] # Rename index to 'Subject.ID'
    genetics_df = genetics_df.drop(['Chromosome.Position'], axis = 0) # Drop last row (repeat of col names)
    genetics_df = genetics_df.reset_index(drop = False)
    
    # Change int to float 
    for col_name in genetics_df :
        if col_name.startswith('CHR'):
            genetics_df[col_name] = genetics_df[col_name].fillna(-9999.0)
            genetics_df[col_name] = genetics_df[col_name].astype(int)
    genetics_df.replace({-9999.0 : 'NA'}, inplace = True)
    return genetics_df



def merge_columns(df : pd.DataFrame , old_df_columns : list, new_df_column_name : str, separator = str) :
    """
    Takes entries in each of old_df_columns and joins them together with a sepator of choice.  Removes
    empty/nan column entries.
    """
    df = df.replace(r'^\s*$', np.NaN, regex=True) # Fill in empty cells with nan
    df[new_df_column_name] = df[old_df_columns].agg(lambda x: x.dropna().str.cat(sep= separator), axis=1) # Combine columns
    df.drop(old_df_columns, axis = 1, inplace = True)
    return df



def read_and_transform_data(csv_filename : str, list_cols : List, drop=False) :
    df = pd.read_csv(genetics_path + csv_filename, skipinitialspace = True)  ## Read in csv
    if drop == False :
        df = df[list_cols] # keep columns in list_cols
    else :
        df.drop(list_cols, axis = 1, inplace = True) # drop columns in list_cols
    return df



def add_snp_recode(df : pd.DataFrame) :
    ## Add in Brian's snp_rs6265_recode.csv file sent on slack 6/29/22
    snp_recode = read_and_transform_data('snp_rs6265_recode.csv',['CHR', 'POS', 'COUNTED', 'ALT', 'SNP', '(C)M'], drop = True)

    # Change column names to be just subid
    for col in snp_recode:
        if '_' in col :
            subid = int(col.split('_')[-1])
            snp_recode.rename(columns = {col : subid}, inplace = True)

    snp_recode = snp_recode.T # Transpose df so that rows are subid
    snp_recode.index.name = 'Subject.ID'
    snp_recode.columns = ['snp_rs6265']
    snp_recode['snp_rs6265'] = snp_recode['snp_rs6265'].fillna(-9999.0)
    snp_recode['snp_rs6265'] = snp_recode['snp_rs6265'].astype(int)
    snp_recode.fillna('NA', inplace = True)
    df = pd.merge(df, snp_recode, on = ['Subject.ID'], how = "outer")
    return df



def merge_multiple_dfs(df_list, on, how):
    df0 = df_list[0] # first df
    df1 = df_list[1] # second df
    merged_df = pd.merge(df0, df1, on = on, how = how) # merge first and second df
    num_dfs = len(df_list) # get total number of dfs in df_list
    for i in range(2, num_dfs) :
        merged_df = pd.merge(merged_df, df_list[i], on = on , how = how) # merge the rest of dfs into merged_df
    return merged_df



if __name__=="__main__":
    main()          
