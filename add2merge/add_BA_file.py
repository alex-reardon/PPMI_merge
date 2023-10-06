import pandas as pd


def main() :
    
    # Set up paths
    userdir = '/Users/areardon/Desktop/Projects/PPMI_Merge3_20230920/'
    ppmi_merge = pd.read_csv(userdir + 'ppmi_merge_v0.1.1.csv')
    new_file = pd.read_csv(userdir + 'ppmi_matched_qc_mm_srfirst.csv')

    ## Create new col to merge on 
    new_file['fn2'] = new_file['fn'].str.split('-').str[1:3].str.join('-')
    new_file['fn2'] = new_file['fn2'].str[:-2]


    # Fix Event.ID.Date order
    ppmi_merge['Event.ID.Date2'] = pd.to_datetime(ppmi_merge['Event.ID.Date'])
    ppmi_merge = ppmi_merge.sort_values(by=['Subject.ID', 'Event.ID.Date2'])
    ppmi_merge.drop(['Event.ID.Date2'], axis = 1, inplace = True) # drop columns in list_cols
    ppmi_merge = ppmi_merge.reset_index(drop=True)


    ## Create new col to merge on
    ppmi_merge['fn2'] = ppmi_merge['Subject.ID'].astype(str) + ppmi_merge['Event.ID.Date'].str[2:] + ppmi_merge['Event.ID.Date'].str[0:2]
    ppmi_merge['fn2'] = ppmi_merge['fn2'].str.replace('/','-')
    
    
    ## Merge
    ppmi_merge = pd.merge(ppmi_merge, new_file, on = ['fn2'], how = "left") # Merge - keep only from ImageIDs we already have
    ppmi_merge.drop(['fn2'], axis = 1, inplace = True)
    ppmi_merge.fillna('NA', inplace = True)
    ppmi_merge = ppmi_merge.drop_duplicates()
    ppmi_merge.to_csv('/Users/areardon/Desktop/ppmi_merge_addition.csv')
    
    jaentl


    

if __name__=="__main__":
    main()
              
