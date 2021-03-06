import pandas as pd


ppmi_merge = pd.read_csv('/Users/areardon/Desktop/ppmi_merge/ppmi_merge_v0.0.5.csv')

subtype_col = 'Consensus.Subtype'
event_id = 'Visit Month 48' 


## Sporadic PD subjects only
enroll_sporadic_pd = ppmi_merge[ppmi_merge[subtype_col]=='Sporadic']


## re: 1 - just T1 for now
enroll_sporadic_pd_t1 = enroll_sporadic_pd[enroll_sporadic_pd['T1.s3.Image.Name'].notna()]


## Restrict to subjects who have a minimum of two visits (...one of which is baseline - line 20)
enroll_sporadic_pd_t1_2_visits = enroll_sporadic_pd_t1[enroll_sporadic_pd_t1.groupby('Subject.ID')['Subject.ID'].transform('size') >= 2]
baseline = enroll_sporadic_pd_t1_2_visits[enroll_sporadic_pd_t1_2_visits['Event.ID'] == 'Baseline']
baseline_n = baseline['Subject.ID'].to_list()
baseline_n = set(baseline_n) # list of subject ids that have a baseline image 


# One of which is baseline
##also please carefully define the n for each table taking note of unique subjects not unique images at the given time point
enroll_sporadic_pd_t1_2_visits = enroll_sporadic_pd_t1_2_visits[enroll_sporadic_pd_t1_2_visits['Subject.ID'].isin(baseline_n)]


## From above table just take BASELINE for first table
## For each table, show summary stats for sex, education, age, UPDRS3, PIGD, Tremor, bradykinesia, UPDRS1 patient and rater, UPDRS2 and MOCA
baseline_only = enroll_sporadic_pd_t1_2_visits[enroll_sporadic_pd_t1_2_visits['Event.ID']==event_id]
temp = baseline_only['Subject.ID'].to_list()
temp = set(temp)
n = int(len(temp))


baseline_only = baseline_only.drop_duplicates()
baseline_only = baseline_only.reset_index(drop=True)
baseline_only = baseline_only.drop_duplicates()
baseline_no_dups = baseline_only.drop_duplicates(subset=['Subject.ID', 'Event.ID','Functional.State.UPDRS3.Cat', 'On.PD.Treatment.UPDRS3.Cat'], keep='first')



def get_mean_std(df, col_name) : 
    the_mean = df[col_name].mean()
    the_mean = round(the_mean,1)
    the_std = df[col_name].std()
    the_std = round(the_std, 1)
    mean_std = str(the_mean) + ' ± ' + str(the_std)
    
    return mean_std


## AGE STATS 
age_mean_std = get_mean_std(baseline_no_dups, 'Age')
print("Age", age_mean_std)


## SEX STATS
male_count = baseline_no_dups[baseline_no_dups['Sex'] == 'Male']
male_count = male_count['Sex'].to_list()
male_count = int(len(male_count))

female_count = baseline_no_dups[baseline_no_dups['Sex'] == 'Female']
female_count = female_count['Sex'].to_list()
female_count = int(len(female_count))
sex_count = str(male_count) +' (' + str(female_count) + ') '
print("Male N / Female N",  sex_count )


## Education Stats 
education_mean_std = get_mean_std(baseline_no_dups, 'Education.Years')
print("Education (years)", education_mean_std )


## UPDRS1 Patient Completed Total 
updrs1_patient_mean_std = get_mean_std(baseline_no_dups, 'Patient.Completed.Total.UPDRS1.Cat')
print("Mean UPDRS1 Patient Completed", updrs1_patient_mean_std)


## UPDRS Rater Total 
updrs1_rater_mean_std = get_mean_std(baseline_no_dups, 'Rater.Completed.Total.UPDRS1.Cat')
print("Mean UPDRS1 Rater Completed", updrs1_rater_mean_std)


# UPDRS2 Total 
updrs2_mean_std = get_mean_std(baseline_no_dups, 'Total.UPDRS2.Num')
print("Mean UPDRS2", updrs2_mean_std)


# UPDRS3 Total 
updrs3_mean_std = get_mean_std(baseline_no_dups, 'Total.UPDRS3.Num')
print("Mean UPDRS3", updrs3_mean_std)


# PIGD
pigd_mean_std = get_mean_std(baseline_no_dups, 'PIGD.Subscore.UPDRS3')
print("Mean PIGD Subscore", pigd_mean_std)


# Tremor
tremor_mean_std = get_mean_std(baseline_no_dups, 'Tremor.Subscore.UPDRS3')
print("Mean Tremor Subscore", tremor_mean_std)


## Bardy Rigidity 
brady_mean_std = get_mean_std(baseline_no_dups, 'Brady.Rigidity.Subscore.UPDRS3')
print("Mean Bradykinesia", brady_mean_std)


## MOCA Total 
moca_mean_std = get_mean_std(baseline_no_dups, 'MOCA.Total')
print("Mean MOCA", moca_mean_std)


#### add some summary of LEDD and On/Off status (am not sure how to do this latter one)
ledd_mean_std = get_mean_std(baseline_no_dups, 'LEDD.sum')
print("Mean LEDD", ledd_mean_std)


func_state_on = baseline_no_dups[baseline_no_dups['Functional.State.UPDRS3.Cat'] == 'On']
func_state_on = func_state_on['Functional.State.UPDRS3.Cat'].to_list()
print('Functional.State.UPDRS3.Cat ON', len(func_state_on))

func_state_off = baseline_no_dups[baseline_no_dups['Functional.State.UPDRS3.Cat'] == 'Off']
func_state_off = func_state_off['Functional.State.UPDRS3.Cat'].to_list()
print('Functional.State.UPDRS3.Cat OFF', len(func_state_off))

func_state_na = baseline_no_dups[baseline_no_dups['Functional.State.UPDRS3.Cat'].isna()]
func_state_na = func_state_na['Functional.State.UPDRS3.Cat'].to_list()
print('Functional.State.UPDRS3.Cat NA', len(func_state_na))




## please also summarize the number of subjects with 0,1,2 for CHR1.POS155197554 and snp_rs6265
## CHR

chr1pos1_count0 = baseline_no_dups[baseline_no_dups['CHR1.POS155197554'] == 0.0]
chr1pos1_count0 = chr1pos1_count0['CHR1.POS155197554'].to_list()
print("CHR1.POS155197554 = 0.0 ", len(chr1pos1_count0))

chr1pos1_count1 = baseline_no_dups[baseline_no_dups['CHR1.POS155197554'] == 1.0]
chr1pos1_count1 = chr1pos1_count1['CHR1.POS155197554'].to_list()
print("CHR1.POS155197554 = 1.0 ", len(chr1pos1_count1))

chr1pos1_count2 = baseline_no_dups[baseline_no_dups['CHR1.POS155197554'] == 2.0]
chr1pos1_count2 = chr1pos1_count2['CHR1.POS155197554'].to_list()
print("CHR1.POS155197554 = 2.0 ", len(chr1pos1_count2))

chr1pos1_countna = baseline_no_dups[baseline_no_dups['CHR1.POS155197554'].isna()]
chr1pos1_countna = chr1pos1_countna['CHR1.POS155197554'].to_list()
print("CHR1.POS155197554 = na", len(chr1pos1_countna))

"CHR1.POS155197554 (0 / 1 / 2 / NA)"
chr_pos = str(len(chr1pos1_count0)) + ' / ' + str(len(chr1pos1_count1)) +' / ' +  str(len(chr1pos1_count2)) +' / '+ str(len(chr1pos1_countna))



## SNP
snp_count0 = baseline_no_dups[baseline_no_dups['snp_rs6265'] == 0.0]
snp_count0 = snp_count0['snp_rs6265'].to_list()
print("snp_rs6265 = 0 ", len(snp_count0))

snp_count1 = baseline_no_dups[baseline_no_dups['snp_rs6265'] == 1.0]
snp_count1 = snp_count1['snp_rs6265'].to_list()
print("snp_rs6265 = 1.0 ", len(snp_count1))

snp_count2 = baseline_no_dups[baseline_no_dups['snp_rs6265'] == 2.0]
snp_count2 = snp_count2['snp_rs6265'].to_list()
print("snp_rs6265 = 2.0 ", len(snp_count2))

snp_countna = baseline_no_dups[baseline_no_dups['snp_rs6265'].isna()]
snp_countna = snp_countna['snp_rs6265'].to_list()
print("snp_rs6265 = na", len(snp_countna))

"snp_rs6265 (0 / 1 / 2 / NA)" 
snp_rs = str(len(snp_count0)) + ' / ' + str(len(snp_count1)) + ' / ' + str(len(snp_count2)) + ' / ' + str(len(snp_countna))



#### also summarize both number of possible subjects and number of subjects with a T1 image and/or a DATLoad score --- please also summarize DAT Load
datload_percent_mean_std = get_mean_std(baseline_no_dups, 'DATLoad.Percent')
print("Mean DATload Percent", datload_percent_mean_std)

count_dataload_percent = baseline_no_dups[baseline_no_dups['DATLoad.Percent'].isna()]
count_dataload_percent = count_dataload_percent['DATLoad.Percent'].to_list()
print("N DATload Percent " , len(count_dataload_percent))

datload_percent_left_std = get_mean_std(baseline_no_dups, 'DATLoadLeft.Percent')
print("Mean Left DATload  :", datload_percent_left_std)

datload_percent_right_mean_std = get_mean_std(baseline_no_dups, 'DATLoadRight.Percent')
print("Mean Right DATload  :", datload_percent_right_mean_std)


### TEMP START 
name_list = ["N", "Age", "Male N / Female N", "Education (years)", "Mean UPDRS1 Total : Patient Completed", "Mean UPDRS1 Total : Rater Completed", "Mean UPDRS2 Total", "Mean UPDRS3 Total ", "Mean PIGD Subscore", "Mean Tremor Subscore", "Mean Bradykinesia", "Mean MOCA  Total", "Mean LEDD", 'Functional.State.UPDRS3.Cat ON', 'Functional.State.UPDRS3.Cat OFF', 'Functional.State.UPDRS3.Cat NA', "CHR1.POS155197554 (0 / 1 / 2 / NA)", "snp_rs6265 (0 / 1 / 2 / NA)" ,  "N DATLoad Percent" , "Mean DATLoad Percent" , "Mean Left DATLoad" , "Mean Right DATLoad"]
numbers = [n, age_mean_std, sex_count,education_mean_std ,updrs1_patient_mean_std,updrs1_rater_mean_std,updrs2_mean_std,updrs3_mean_std,pigd_mean_std,tremor_mean_std,brady_mean_std,moca_mean_std,ledd_mean_std,len(func_state_on),len(func_state_off),len(func_state_na),chr_pos, snp_rs, len(count_dataload_percent), datload_percent_mean_std, datload_percent_left_std, datload_percent_right_mean_std]

data={'Name':name_list,'Num':numbers}
df=pd.DataFrame(data)


print(df)
df.to_csv('/Users/areardon/Desktop/df' + subtype_col + '_' + event_id + '.csv')


