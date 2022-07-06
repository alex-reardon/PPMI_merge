# Get numbers for tables DTI SR Report
# July 6th 2021

import pandas as pd

ppmi_merge = pd.read_csv('/Users/areardon/Desktop/ppmi_merge/ppmi_merge_v0.0.4.csv')

cortico_spinal_df = ppmi_merge[['Subject.ID' ,'Event.ID', 'mean_fa-corticospinal_tract-left-jhu_icbm_labels_1mm']] # Get condensed version of df of only cols we want 
print(cortico_spinal_df)
janet

cortico_spinal_df['Event.ID'].fillna('NA', inplace = True) # fill Na
cortico_spinal_df = cortico_spinal_df[cortico_spinal_df['mean_fa-corticospinal_tract-left-jhu_icbm_labels_1mm'].notna()] # Remove all rows where there is no mean_fa_cortico... value
cortico_spinal_df.drop_duplicates(inplace= True) # Drop duplicates 
cortico_spinal_df = cortico_spinal_df[cortico_spinal_df['mean_fa-corticospinal_tract-left-jhu_icbm_labels_1mm'] >= 0.1]
print(len(cortico_spinal_df))


cortico_spinal_counts_df = cortico_spinal_df.groupby(["Subject.ID","Event.ID"]).size().reset_index(name='Image.Counts1')
cortico_spinal_counts_df = cortico_spinal_counts_df.drop(['Subject.ID'],axis = 1)
final_counts = cortico_spinal_counts_df.groupby(["Event.ID"]).value_counts().reset_index(name='Subject.Images')
final_counts['Subject Images * Image Counts'] = final_counts["Image.Counts1"] * final_counts["Subject.Images"]


# Get number of subjects only with dti images at each event id 
temp = final_counts[['Event.ID','Subject.Images']]
temp = temp.groupby('Event.ID',as_index=False)['Subject.Images'].sum()
print(temp)

# Get total number of dti images at each event id 
temp = final_counts[['Event.ID','Subject Images * Image Counts']]
temp = temp.groupby('Event.ID',as_index=False)['Subject Images * Image Counts'].sum()
print(temp)



