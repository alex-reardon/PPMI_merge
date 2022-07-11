# Get stats/ numbers for tables DTI SR Report
# July 6th 2021

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pylab
import scipy.stats as stats
from scipy.stats import f_oneway
from scipy.stats import ttest_ind
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd
plt.rcParams["font.family"] = "Times New Roman"


## Read in ppmi_merge file
ppmi_merge = pd.read_csv('/Users/areardon/Desktop/ppmi_merge/ppmi_merge_v0.0.4.csv')



# Get all col names from OR_mean_fa_summary in order to go through them and find regions of sig change
mean_fa_summary = pd.read_csv('/Users/areardon/Downloads/PPMI-100005-20210127-antspymm-I1526372_I1526371-OR_mean_fa_summary.csv')
mean_fa_summary.drop(['u_hier_id'], axis = 1, inplace = True) # Drop

left_list = []
right_list = []
for column in mean_fa_summary : 
    if 'left' in column : 
        left_list.append(column)
    if 'right' in column : 
        right_list.append(column)


# #### Get numbers for tables  ####
# col_name = 'Enroll.Subtype' 
# cortico_spinal_df = ppmi_merge[['Subject.ID', col_name ,'Event.ID', 'mean_fa-corticospinal_tract-left-jhu_icbm_labels_1mm']] # Get condensed version of df of only cols we want 
# cortico_spinal_df['Event.ID'].fillna('NA', inplace = True) # fill Na
# cortico_spinal_df = cortico_spinal_df[cortico_spinal_df['mean_fa-corticospinal_tract-left-jhu_icbm_labels_1mm'].notna()] # Remove all rows where there is no mean_fa_cortico... value
# cortico_spinal_df.drop_duplicates(inplace= True) # Drop duplicates 

# images = cortico_spinal_df[cortico_spinal_df['mean_fa-corticospinal_tract-left-jhu_icbm_labels_1mm'] >= 0.1]
# subjects = images.drop_duplicates(subset=['Event.ID', 'Subject.ID'])

# im = images.groupby(["Event.ID",col_name]).size().reset_index(name='Image.Counts1')
# im = im.sort_values(by = [col_name ,'Event.ID']) # Sort values by subject and event id date
# im.to_csv('/Users/areardon/Desktop/im.csv')
# sub = subjects.groupby(["Event.ID",col_name]).size().reset_index(name='Image.Counts1')
# sub = sub.sort_values(by = [col_name ,'Event.ID']) # Sort values by subject and event id date
# sub.to_csv('/Users/areardon/Desktop/sub.csv')


# #### STATS ####

# col_name = 'Enroll.Diagnosis' 
# # fa_col_name_right = 'mean_fa-cerebral_peduncle-right-jhu_icbm_labels_1mm'
# # fa_col_name_left = 'mean_fa-cerebral_peduncle-left-jhu_icbm_labels_1mm'
# # fa_col_name_right = 'mean_fa-corticospinal_tract-right-jhu_icbm_labels_1mm'
# # fa_col_name_left = 'mean_fa-corticospinal_tract-left-jhu_icbm_labels_1mm'
# fa_col_name_right ='mean_fa-superior_cerebellar_peduncle-right-jhu_icbm_labels_1mm'
# fa_col_name_left = 'mean_fa-superior_cerebellar_peduncle-left-jhu_icbm_labels_1mm'

# # fa_col_name_right ='mean_fa-external_capsule-left-jhu_icbm_labels_1mm'
# # fa_col_name_left = 'mean_fa-external_capsule-right-jhu_icbm_labels_1mm'


# # for i in range(len(right_list)) : 
# #     fa_col_name_right = right_list[i]
# #     fa_col_name_left = left_list[i]
# domside_col_name = 'Dominant Side FA Cerebral Peduncle'

# cortico_spinal_df = ppmi_merge[['Subject.ID', col_name ,'Event.ID', fa_col_name_right, fa_col_name_left, 'Dominant.Side.Disease']] # Get condensed version of df of only cols we want 
# cortico_spinal_df.to_csv('/Users/areardon/Desktop/csd1.csv')

# cortico_spinal_df['Event.ID'].fillna('NA', inplace = True) # fill Na
# cortico_spinal_df = cortico_spinal_df[cortico_spinal_df[fa_col_name_right].notna()] # Remove all rows where there is no mean_fa_cortico... value
# cortico_spinal_df.to_csv('/Users/areardon/Desktop/csd2.csv')

# cortico_spinal_df.drop_duplicates(inplace= True) # Drop duplicates 
# images = cortico_spinal_df[cortico_spinal_df[fa_col_name_right] >= 0.1]
# images.to_csv('/Users/areardon/Desktop/csd3.csv')


# subjects = images.drop_duplicates(subset=['Event.ID', 'Subject.ID']) # Take only one dti image data from repeats 
# subjects['Dominant.Side.Disease'].fillna('Symmetric', inplace = True) # fill Na FIXME
# subjects.to_csv('/Users/areardon/Desktop/csd4.csv')



# subjects[domside_col_name] = ''
# subjects.loc[(subjects['Dominant.Side.Disease'] == 'Left') , domside_col_name] = subjects[fa_col_name_left]
# subjects.loc[(subjects['Dominant.Side.Disease'] == 'Right') , domside_col_name] = subjects[fa_col_name_right]
# subjects.loc[(subjects['Dominant.Side.Disease'] == 'Symmetric') , domside_col_name] = (subjects[fa_col_name_right] + subjects[fa_col_name_left])/2
# subjects.drop([fa_col_name_right, fa_col_name_left, 'Dominant.Side.Disease'], axis = 1, inplace = True) # Drop these from ppmi_merge so there aren't duplicates when we merge the diag_vis dfs

# parkinsons = subjects[(subjects[col_name] == 'Parkinson\'s Disease') & (subjects['Event.ID']=='Baseline')]
# hc = subjects[(subjects[col_name] == 'Healthy Control') & (subjects['Event.ID']=='Baseline')]
# prodromal = subjects[(subjects[col_name] == 'Prodromal') & (subjects['Event.ID']=='Baseline')]
# swedd = subjects[(subjects[col_name] == 'SWEDD') & (subjects['Event.ID']=='Baseline')]

# parkinsons_meanfa = parkinsons[domside_col_name].to_list()
# print("PD sample size :", len(parkinsons_meanfa))
# hc_meanfa = hc[domside_col_name].to_list()
# print("HC sample size:", len(hc_meanfa))
# prodromal_meanfa = prodromal[domside_col_name].to_list()
# print("Prodromal sample size:", len(prodromal_meanfa))
# swedd_meanfa = swedd[domside_col_name].to_list()
# print("SWEDD sample size:", len(swedd_meanfa))

# # Make df 
# parkinsons = parkinsons[[col_name, domside_col_name]]
# hc = hc[[col_name, domside_col_name]]
# prodromal = prodromal[[col_name, domside_col_name]]
# swedd = swedd[[col_name, domside_col_name]]
# # parkinsons.to_csv('/Users/areardon/Desktop/pd.csv')
# # swedd.to_csv('/Users/areardon/Desktop/swedd.csv')


# all_dfs = [parkinsons, hc, prodromal , swedd]
# dfs = pd.concat(all_dfs).reset_index(drop=True)
# dfs[col_name] = dfs[col_name].str.replace("Parkinson\'s Disease", "0") 
# dfs[col_name] = dfs[col_name].str.replace("Prodromal", "1") 
# dfs[col_name] = dfs[col_name].str.replace("Healthy Control", "2") 
# dfs[col_name] = dfs[col_name].str.replace("SWEDD", "3") 
# dfs = dfs.astype(float)

# dfs.to_csv('/Users/areardon/Desktop/dftoday.csv')

# ##Test for normality 
# # stats.probplot(dfs[fa_col_name], dist="norm", plot=pylab)
# # pylab.show()

# ##Test for homogeniety of variance 
# ax = sns.boxplot(x=col_name, y=domside_col_name, data=dfs, color='#99c2a2')
# ax = sns.swarmplot(x=col_name, y=domside_col_name,  data=dfs, color='#7d0013', size = 3)
# plt.show()

# # Conduct the one-way ANOVA
# res = f_oneway(parkinsons_meanfa, hc_meanfa, prodromal_meanfa, swedd_meanfa)
# print(fa_col_name_right)
# print(fa_col_name_left)
# print(res)

# tukey = pairwise_tukeyhsd(endog=dfs[domside_col_name],
#                         groups=dfs['Enroll.Diagnosis'],
#                         alpha=0.05)
# print(tukey)


# janet 

# #### TTTESTS btwn grps ####
# col_name = 'Enroll.Subtype' 
# # fa_col_name_right = 'mean_fa-cerebral_peduncle-right-jhu_icbm_labels_1mm'
# # fa_col_name_left = 'mean_fa-cerebral_peduncle-left-jhu_icbm_labels_1mm'
# fa_col_name_right = 'mean_fa-corticospinal_tract-right-jhu_icbm_labels_1mm'
# fa_col_name_left = 'mean_fa-corticospinal_tract-left-jhu_icbm_labels_1mm'
# domside_col_name = 'Dominant Side FA Cerebral Peduncle'

# cortico_spinal_df = ppmi_merge[['Subject.ID', col_name ,'Event.ID', fa_col_name_right, fa_col_name_left, 'Dominant.Side.Disease']] # Get condensed version of df of only cols we want 
# cortico_spinal_df['Event.ID'].fillna('NA', inplace = True) # fill Na
# cortico_spinal_df = cortico_spinal_df[cortico_spinal_df[fa_col_name_right].notna()] # Remove all rows where there is no mean_fa_cortico... value
# cortico_spinal_df.drop_duplicates(inplace= True) # Drop duplicates 
# images = cortico_spinal_df[cortico_spinal_df[fa_col_name_right] >= 0.1]
# subjects = images.drop_duplicates(subset=['Event.ID', 'Subject.ID']) # Take only one dti image data from repeats 
# subjects['Dominant.Side.Disease'].fillna('Symmetric', inplace = True) # fill Na FIXME

# subjects[domside_col_name] = ''
# subjects.loc[(subjects['Dominant.Side.Disease'] == 'Left') , domside_col_name] = subjects[fa_col_name_left]
# subjects.loc[(subjects['Dominant.Side.Disease'] == 'Right') , domside_col_name] = subjects[fa_col_name_right]
# subjects.loc[(subjects['Dominant.Side.Disease'] == 'Symmetric') , domside_col_name] = (subjects[fa_col_name_right] + subjects[fa_col_name_left])/2
# subjects.drop([fa_col_name_right, fa_col_name_left, 'Dominant.Side.Disease'], axis = 1, inplace = True) # Drop these from ppmi_merge so there aren't duplicates when we merge the diag_vis dfs
# subjects.to_csv('/Users/areardon/Desktop/subjects1.csv')
# sporadic_pd = subjects[(subjects[col_name] == 'Sporadic') & (subjects['Event.ID']=='Baseline')]
# lrrk2_pd = subjects[(subjects[col_name] == 'Genetic : LRRK2') & (subjects['Event.ID']=='Baseline')]
# gba_pd = subjects[(subjects[col_name] == 'Genetic : GBA') & (subjects['Event.ID']=='Baseline')]


# sporadicpd_meanfa = sporadic_pd[domside_col_name].to_list()
# lrrk2pd_meanfa = lrrk2_pd[domside_col_name].to_list()
# gbapd_meanfa = gba_pd[domside_col_name].to_list()

# ## Make df 
# sporadic_pd = sporadic_pd[[col_name, domside_col_name]]
# lrrk2_pd = lrrk2_pd[[col_name, domside_col_name]]
# gba_pd = gba_pd[[col_name, domside_col_name]]
# all_dfs = [sporadic_pd, lrrk2_pd, gba_pd]
# dfs = pd.concat(all_dfs).reset_index(drop=True)
# print(dfs)

# # Test for normality 
# #stats.probplot(dfs[fa_col_name], dist="norm", plot=pylab)
# #pylab.show()

# # Test for homogeniety of variance 
# ax = sns.boxplot(x=col_name, y=domside_col_name, data=dfs, color='#99c2a2')
# ax = sns.swarmplot(x=col_name, y=domside_col_name,  data=dfs, color='#7d0013', size = 3)
# plt.show()


# dfs[col_name] = dfs[col_name].str.replace("Sporadic", "0") 
# dfs[col_name] = dfs[col_name].str.replace('Genetic : LRRK2', "1") 
# dfs[col_name] = dfs[col_name].str.replace('Genetic : GBA', "2") 
# dfs = dfs.astype(float)


# # # Conduct the one-way ANOVA
# res = f_oneway(sporadicpd_meanfa, lrrk2pd_meanfa, gbapd_meanfa)
# print("Z anovas ", res)

# tukey = pairwise_tukeyhsd(endog=dfs[domside_col_name],
#                           groups=dfs[col_name],
#                           alpha=0.05)


# janet


####  Stats PD over time  ####
col_name = 'Enroll.Subtype' 
dx = 'Sporadic'

# fa_col_name_right = 'mean_fa-cerebral_peduncle-right-jhu_icbm_labels_1mm'
# fa_col_name_left = 'mean_fa-cerebral_peduncle-left-jhu_icbm_labels_1mm'
fa_col_name_right = 'mean_fa-corticospinal_tract-right-jhu_icbm_labels_1mm'
fa_col_name_left = 'mean_fa-corticospinal_tract-left-jhu_icbm_labels_1mm'
domside_col_name = 'Dominant Side FA Cerebral Peduncle'

cortico_spinal_df = ppmi_merge[['Subject.ID', col_name ,'Event.ID', fa_col_name_right, fa_col_name_left, 'Dominant.Side.Disease']] # Get condensed version of df of only cols we want 
cortico_spinal_df['Event.ID'].fillna('NA', inplace = True) # fill Na
cortico_spinal_df = cortico_spinal_df[cortico_spinal_df[fa_col_name_right].notna()] # Remove all rows where there is no mean_fa_cortico... value
cortico_spinal_df.drop_duplicates(inplace= True) # Drop duplicates 
images = cortico_spinal_df[cortico_spinal_df[fa_col_name_right] >= 0.1]
subjects = images.drop_duplicates(subset=['Event.ID', 'Subject.ID']) # Take only one dti image data from repeats 
subjects['Dominant.Side.Disease'].fillna('Symmetric', inplace = True) # fill Na FIXME

subjects[domside_col_name] = ''
subjects.loc[(subjects['Dominant.Side.Disease'] == 'Left') , domside_col_name] = subjects[fa_col_name_left]
subjects.loc[(subjects['Dominant.Side.Disease'] == 'Right') , domside_col_name] = subjects[fa_col_name_right]
subjects.loc[(subjects['Dominant.Side.Disease'] == 'Symmetric') , domside_col_name] = (subjects[fa_col_name_right] + subjects[fa_col_name_left])/2
subjects.drop([fa_col_name_right, fa_col_name_left, 'Dominant.Side.Disease'], axis = 1, inplace = True) # Drop these from ppmi_merge so there aren't duplicates when we merge the diag_vis dfs

# Separate subjects by event id 
parkinsons_SC = subjects[(subjects[col_name] == dx) & (subjects['Event.ID']=='Screening')]
parkinsons_BL = subjects[(subjects[col_name] == dx) & (subjects['Event.ID']=='Baseline')]
parkinsons_MO12 = subjects[(subjects[col_name] == dx) & (subjects['Event.ID']=='Visit Month 12')]
parkinsons_MO24 = subjects[(subjects[col_name] == dx) & (subjects['Event.ID']=='Visit Month 24')]
parkinsons_MO48 = subjects[(subjects[col_name] == dx) & (subjects['Event.ID']=='Visit Month 48')]

## Make lists
parkinsons_SC_meanfa = parkinsons_SC[domside_col_name].to_list()
parkinsons_BL_meanfa = parkinsons_BL[domside_col_name].to_list()
parkinsons_MO12_meanfa = parkinsons_MO12[domside_col_name].to_list()
parkinsons_MO24_meanfa = parkinsons_MO24[domside_col_name].to_list()
parkinsons_MO48_meanfa = parkinsons_MO48[domside_col_name].to_list()

## Make df 
parkinsons_SC = parkinsons_SC[['Event.ID', domside_col_name]]
parkinsons_BL = parkinsons_BL[['Event.ID', domside_col_name]]
parkinsons_MO12 = parkinsons_MO12[['Event.ID', domside_col_name]]
parkinsons_MO24 = parkinsons_MO24[['Event.ID', domside_col_name]]
parkinsons_MO48 = parkinsons_MO48[['Event.ID', domside_col_name]]
all_dfs = [ parkinsons_SC, parkinsons_BL, parkinsons_MO12, parkinsons_MO24, parkinsons_MO48 ]
dfs = pd.concat(all_dfs).reset_index(drop=True)

#Replace event ids with number for regression
dfs['Event.ID'] = dfs['Event.ID'].str.replace("Screening", "0") 
dfs['Event.ID'] = dfs['Event.ID'].str.replace("Baseline", "1") 
dfs['Event.ID'] = dfs['Event.ID'].str.replace("Visit Month 12", "2")
dfs['Event.ID'] = dfs['Event.ID'].str.replace("Visit Month 24", "3") 
dfs['Event.ID'] = dfs['Event.ID'].str.replace("Visit Month 48", "4") 
dfs = dfs.astype(float)

dfs.to_csv('/Users/areardon/Desktop/dfs.csv')
# Regression plot
g = sns.regplot(x='Event.ID', y=domside_col_name, data=dfs)
g.set_xticklabels(['', 'Screening', '', 'Baseline','', 'Visit Month 12','', 'Visit Month 24','','Visit Month 48'])

import statsmodels.api as sm


x = dfs['Event.ID'].to_list()
y = dfs[domside_col_name].to_list()
x = sm.add_constant(x)
 
# performing the regression
# and fitting the model
result = sm.OLS(y,x).fit()
 
# printing the summary table
print(result.summary())

res = f_oneway(parkinsons_SC_meanfa, parkinsons_BL_meanfa, parkinsons_MO12_meanfa, parkinsons_MO24_meanfa, parkinsons_MO48_meanfa)
print(res)

# janet

# ## CODE TO GET TABLE NUMBERS
# index_names = cortico_spinal_counts_df[ (cortico_spinal_counts_df['Event.ID'] == cortico_spinal_counts_df['Consensus.Diagnosis'])].index
# cortico_spinal_counts_df = cortico_spinal_counts_df.drop(index_names, inplace = True)
# cortico_spinal_counts_df.to_csv('/Users/areardon/Desktop/two.csv')

    

# cortico_spinal_df = cortico_spinal_df[cortico_spinal_df["Event.ID"] !=  cortico_spinal_df['Subject.ID']]
# cortico_spinal_counts_df = cortico_spinal_df.groupby(["Event.ID","Consensus.Diagnosis"]).size().reset_index(name='Image.Counts1')
# print(cortico_spinal_counts_df)


# cortico_spinal_counts_df = cortico_spinal_counts_df.drop(['Subject.ID'],axis = 1)
# final_counts = cortico_spinal_counts_df.groupby(["Event.ID"]).value_counts().reset_index(name='Subject.Images')
# final_counts['Subject Images * Image Counts'] = final_counts["Image.Counts1"] * final_counts["Subject.Images"]


# # Get number of subjects only with dti images at each event id 
# temp = final_counts[['Event.ID','Subject.Images']]
# temp = temp.groupby('Event.ID',as_index=False)['Subject.Images'].sum()
# print(temp)

# # Get total number of dti images at each event id 
# temp = final_counts[['Event.ID','Subject Images * Image Counts']]
# temp = temp.groupby('Event.ID',as_index=False)['Subject Images * Image Counts'].sum()
# print(temp)



