## Tests for n in ppmi_merge file 

import pandas as pd
userdir = '/Users/areardon/Desktop/ppmi_merge/versions/'
ppmi_merge = pd.read_csv(userdir + 'ppmi_merge_v0.csv', skipinitialspace = True)
ppmi_merge.fillna('NA', inplace = True)

def test_n(df, cohort, dx, subtype, expected_n) : 
    """
    Test if expected N from Consensus Committee Consensus_Committee_Analytic_Datasets_28OCT21.xlsx matches ppmi_merge N  

    Arguments
    ------------------
    df : pd.DataFrame ppmi_merge

    cohort : str - 'Consensus' or 'Enroll'

    dx : str - Diagnostic group 

    subtype : str -subtype of interest

    expected_n : int 

    """
    dx_col_name = cohort + '.Diagnosis'
    subtype_col_name = cohort + '.Subtype'
    subtype_df = df[(df[dx_col_name] == dx) & (df[subtype_col_name] == subtype)]
    unique_subids = subtype_df['Subject.ID'].unique()
    ppmi_merge_n = len(unique_subids)
    if ppmi_merge_n != expected_n : 
        raise Exception(f'NO MATCH : {cohort} : {dx} , {subtype} True N  == {expected_n} and ppmi_merge N == {ppmi_merge_n}')
    return ppmi_merge_n, expected_n

ppmi_merge_n, expected_n = test_n(ppmi_merge, cohort = 'Consensus', dx = 'Parkinson\'s Disease' , subtype = 'Sporadic' , expected_n = 450)


def test_n_event_id(df, event_id, expected_n):
    """
    Test function for the expected N at event_id 

    Arguments
    ------------------
    df : pd.DataFrame ppmi_merge

    event_id : str 

    expected_n : int 

    """

    subtype_df = df[df['Event.ID'] == event_id]
    unique_subids = subtype_df['Subject.ID'].unique()
    ppmi_merge_n = len(unique_subids)
    if ppmi_merge_n != expected_n : 
        raise Exception(f'NO MATCH : True N  == {expected_n} and ppmi_merge N == {ppmi_merge_n}')
    return ppmi_merge_n, expected_n

ppmi_merge_n, expected_n = test_n_event_id(ppmi_merge, event_id = 'Baseline', expected_n = 1672) # FIXME expected_n needed from MJFF


def test_n_event_id_DX(df, cohort, dx, subtype, event_id, expected_n):
    """
    ## Test function for expected N at event_id broken down by DX 

    Arguments
    ------------------
    df : pd.DataFrame ppmi_merge

    cohort : str - 'Consensus' or 'Enroll'

    dx : str - Diagnostic group 

    subtype : str subtype of interest

    event_id : str 

    expected_n : int 

    """

    dx_col_name = cohort + '.Diagnosis'
    subtype_col_name = cohort + '.Subtype'
    subtype_df = df[(df[dx_col_name] == dx) & (df[subtype_col_name] == subtype) & (df['Event.ID'] == event_id)]
    unique_subids = subtype_df['Subject.ID'].unique()
    ppmi_merge_n = len(unique_subids)
    if ppmi_merge_n != expected_n : 
        raise Exception(f'NO MATCH : {cohort} : {dx} , {subtype} True N  == {expected_n} and ppmi_merge N == {ppmi_merge_n}')
    return ppmi_merge_n, expected_n

ppmi_merge_n, expected_n = test_n_event_id_DX(ppmi_merge, cohort = 'Consensus', dx = 'Parkinson\'s Disease' , subtype = 'Sporadic', event_id = 'Baseline', expected_n = 396) # FIXME expected_n needed from MJFF


def test_n_variable(df, cohort, dx, subtype, event_id, variable) : 
    """
    # Test function for subjects that have variable (i.e. MOCA.Total) at given event_id date 

    Arguments
    ------------------
    df : pd.DataFrame ppmi_merge
    
    cohort : str - 'Consensus' or 'Enroll'

    dx : str - Diagnostic group 

    subtype : str subtype of interest

    event_id : str 

    variable : str (column name from ppmi_merge)

    """
    dx_col_name = cohort + '.Diagnosis'
    subtype_col_name = cohort + '.Subtype'
    subtype_df = df[(df[dx_col_name] == dx) & (df[subtype_col_name] == subtype) & (df['Event.ID'] == event_id) & (df[variable] != 'NA')]
    unique_subids = subtype_df['Subject.ID'].unique()
    variable_n = len(unique_subids)
    return(variable_n)

variable_n = test_n_variable(ppmi_merge, cohort = 'Consensus', dx = 'Parkinson\'s Disease' , subtype = 'Sporadic', event_id = 'Baseline', variable = 'T1.s3.Image.Name')



