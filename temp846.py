import pandas as pd


ppmi_merge = pd.read_csv('/Users/areardon/Desktop/ppmi_merge/ppmi_merge_v0.0.41.csv')
ppmi_merge = ppmi_merge.filter(regex='mean|Subject.ID|Event.ID|Event.ID.Date|Image.Acquisition.Date|DTI.antspymm.Image.ID')
ppmi_merge.to_csv('/Users/areardon/Desktop/ppmi_merge_filtered.csv')

# kevin

temp = ppmi_merge['mean_fa-anterior_corona_radiata-left-jhu_icbm_labels_1mm'].dropna().tolist()
print(set(temp))
print(len(set(temp)))


