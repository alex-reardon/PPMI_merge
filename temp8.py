import pandas as pd


df = pd.read_csv('/Users/areardon/Desktop/ppmi_merge_full.csv')

df = df.filter(regex='mean|Subject.ID|Image.Acquisition.Date|DTI.antspymm.Image.ID')
df.to_csv('/Users/areardon/Desktop/dftoday3.csv')



alexandr


