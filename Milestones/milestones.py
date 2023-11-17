## Create milestones df from ppmi_merge

import pandas as pd
import numpy as np 
from scipy import stats
import datetime


def main() :
    
    ## Read in file 
    v = 'v0.0.5'
    userdir = "/Users/areardon/Desktop/Projects/PPMI_Merge3_20230920/" 
    savedir = "/Users/areardon/Desktop/Projects/Milestones/" + v + '/' 
    ppmi_merge_v = '0.1.1'
    ppmi_merge = pd.read_csv(userdir + 'ppmi_merge_clinical_v' + ppmi_merge_v + '.csv')

    ## Domains 
    clinical = ['Subject.ID',	'Event.ID',	'Event.ID.Date',	'Enroll.Diagnosis',	'Enroll.Subtype',	'Consensus.Diagnosis',	'Consensus.Subtype',	'Analytic.Cohort',	'Subject.Phenoconverted']
    domain1 = ['Walking.Difficulty.UPDRS2.Num', 'Freezing.while.Walking.UPDRS2.Num', 'Gait.Problems.UPDRS3.Num', 'Freezing.of.Gait.UPDRS3.Num', 'Postural.Stability.Problems.UPDRS3.Num', 'Hoehn.and.Yahr.Stage.UPDRS3.Num','Functional.State.UPDRS3.Cat'] # FIXME functional state?
    domain2 = ['Time.Spent.with.Dyskinesias.UPDRS4.Num', 'Functional.Impact.of.Dyskinesias.UPDRS4.Num', 'Functional.Impact.Fluctuations.UPDRS4.Num', 'Complexity.of.Motor.Fluctuations.UPDRS4.Num']
    domain3 = ['MOCA.Total', 'Cognitive.Impairment.UPDRS1.Num', 'Hallucinations.and.Psychosis.UPDRS1.Num', 'Apathy.UPDRS1.Num', 'Cognitive.State', 'DVT.Total.RECALL','DVT_RECOG_DISC_INDEX', 'DVT_DELAYED_RECALL','DVT_RETENTION', 'JLO_TOTRAW','Symbol.Digit.Modalities.Total', 'Letter.Number.Sequencing.Total', 'Sematnic.Fluency.TScore','Functional.Cognitive.Impairment'] # FIXME SEMATNIC SPELLING
    domain4 = ['Urinary.Problems.UPDRS1.Num', 'SCAU8', 'SCAU9','SCAU15', 'Diastolic.BP.Sitting' , 'Systolic.BP.Sitting', 'Diastolic.BP.Standing', 'Systolic.BP.Standing', 'Lightheadedness.on.Standing.UPDRS1.Num', 'SCAU16']
    domain5 = ['MSEADLG']
    domain6 = ['Chewing.Swallowing.Difficulty.UPDRS2.Num', 'Eating.Difficulty.UPDRS2.Num', 'Dressing.Difficulty.UPDRS2.Num', 'Hygiene.Difficulty.UPDRS2.Num', 'Speech.Difficulty.UPDRS3.Num']


    ## Create a filtered df with only info we are interested in     
    full_list = clinical +  domain1 + domain2 + domain3 + domain4 +  domain5 + domain6
    ppmi_merge_filtered = ppmi_merge[full_list]


    ## Get blood pressure min/maxes
    ppmi_merge_filtered['sys.bp.diff'] = ''
    ppmi_merge_filtered['dia.bp.diff'] = ''
    for row_num in range(len(ppmi_merge_filtered['Systolic.BP.Standing'])) : 
        temp_sys = ppmi_merge_filtered['Systolic.BP.Standing'].loc[row_num] -  ppmi_merge_filtered['Systolic.BP.Sitting'].loc[row_num]
        temp_dia = ppmi_merge_filtered['Diastolic.BP.Standing'].loc[row_num] -  ppmi_merge_filtered['Diastolic.BP.Sitting'].loc[row_num]
        ppmi_merge_filtered['sys.bp.diff'].loc[row_num] = temp_sys
        ppmi_merge_filtered['dia.bp.diff'].loc[row_num] = temp_dia 
        

    ## Zscores 
    zscore_list = ['DVT_RECOG_DISC_INDEX', 'DVT.Total.RECALL', 'JLO_TOTRAW','Symbol.Digit.Modalities.Total', 'Letter.Number.Sequencing.Total', 'Sematnic.Fluency.TScore']
    for zscore_item in zscore_list :
        zscore_dvt = stats.zscore(ppmi_merge_filtered[zscore_item],nan_policy='omit')
        ppmi_merge_filtered[zscore_item + '.Zscore'] = zscore_dvt
  

    # Make categorical variables back to numeric
    ppmi_merge_filtered['Cognitive.State'].replace({'Normal Cognition': 0, 'Mild Cognitive Impairment (MCI)' : 0 , 'Dementia': 1}, inplace = True)
    ppmi_merge_filtered['Functional.Cognitive.Impairment'].replace({'No': 0, 'Yes' : 1}, inplace = True)


    ## Create scores to be between 0 and 1 for each milestone
    ## Domain 1 DONE
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Walking.Difficulty.UPDRS2.Num', 'Walking.Difficulty.UPDRS2.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Freezing.while.Walking.UPDRS2.Num', 'Freezing.while.Walking.UPDRS2.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Gait.Problems.UPDRS3.Num', 'Gait.Problems.UPDRS3.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Freezing.of.Gait.UPDRS3.Num', 'Freezing.of.Gait.UPDRS3.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Postural.Stability.Problems.UPDRS3.Num', 'Postural.Stability.Problems.UPDRS3.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Hoehn.and.Yahr.Stage.UPDRS3.Num', 'Hoehn.and.Yahr.Stage.UPDRS3.Num.Scaled', 0, 5) 

    
    ## Domain 2 DONE
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Time.Spent.with.Dyskinesias.UPDRS4.Num', 'Time.Spent.with.Dyskinesias.UPDRS4.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Functional.Impact.of.Dyskinesias.UPDRS4.Num', 'Functional.Impact.of.Dyskinesias.UPDRS4.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Functional.Impact.Fluctuations.UPDRS4.Num', 'Functional.Impact.Fluctuations.UPDRS4.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Complexity.of.Motor.Fluctuations.UPDRS4.Num', 'Complexity.of.Motor.Fluctuations.UPDRS4.Num.Scaled', 0, 4) 


    ## Domain 3 DONE
    ppmi_merge_filtered = create_reversed_scaled_col(ppmi_merge_filtered, 'MOCA.Total', 'MOCA.Total.Scaled', 0, 30) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Cognitive.Impairment.UPDRS1.Num', 'Cognitive.Impairment.UPDRS1.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Hallucinations.and.Psychosis.UPDRS1.Num', 'Hallucinations.and.Psychosis.UPDRS1.Num.Scaled', 0, 4)
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Apathy.UPDRS1.Num', 'Apathy.UPDRS1.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Cognitive.State', 'Cognitive.State.Scaled', 0,1) 
    ppmi_merge_filtered = create_reversed_scaled_col(ppmi_merge_filtered, 'DVT.Total.RECALL', 'DVT.Total.RECALL.Scaled', 20,75) 
    ppmi_merge_filtered = create_reversed_scaled_col(ppmi_merge_filtered, 'DVT_RECOG_DISC_INDEX', 'DVT_RECOG_DISC_INDEX.Scaled', 20,63)     
    ppmi_merge_filtered = create_reversed_scaled_col(ppmi_merge_filtered, 'JLO_TOTRAW', 'JLO_TOTRAW.Scaled', 0, 15) 
    ppmi_merge_filtered = create_reversed_scaled_col(ppmi_merge_filtered, 'Symbol.Digit.Modalities.Total', 'Symbol.Digit.Modalities.Total.Scaled', 0, 102) 
    ppmi_merge_filtered = create_reversed_scaled_col(ppmi_merge_filtered, 'Letter.Number.Sequencing.Total', 'Letter.Number.Sequencing.Total.Scaled', 0, 21) 
    ppmi_merge_filtered = create_reversed_scaled_col(ppmi_merge_filtered, 'Sematnic.Fluency.TScore', 'Sematnic.Fluency.TScore.Scaled', 6,88) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Functional.Cognitive.Impairment', 'Functional.Cognitive.Impairment.Scaled', 0, 1) # FIXME CHECK
    
    
    ## Domain 4 DONE
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Urinary.Problems.UPDRS1.Num', 'Urinary.Problems.UPDRS1.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'SCAU8', 'SCAU8.Scaled', 0, 3) # FIXME becausenow we left in 9
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'SCAU9', 'SCAU9.Scaled', 0, 3)  # FIXME because now we left in 9
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'SCAU15', 'SCAU15.Scaled', 0, 3) 
    ppmi_merge_filtered = create_bp_scaled_col(ppmi_merge_filtered, 'sys.bp.diff', 'sys.bp.diff.Scaled', 20)
    ppmi_merge_filtered = create_bp_scaled_col(ppmi_merge_filtered, 'dia.bp.diff', 'dia.bp.diff.Scaled', 10)
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Lightheadedness.on.Standing.UPDRS1.Num', 'Lightheadedness.on.Standing.UPDRS1.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'SCAU16', 'SCAU16.Scaled', 0, 3)     

    
    ## Domain 5 DONE
    ppmi_merge_filtered = create_reversed_scaled_col(ppmi_merge_filtered, 'MSEADLG', 'MSEADLG.Scaled', 0, 100) 

    
    ## Domain 6 DONE
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Chewing.Swallowing.Difficulty.UPDRS2.Num', 'Chewing.Swallowing.Difficulty.UPDRS2.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Eating.Difficulty.UPDRS2.Num', 'Eating.Difficulty.UPDRS2.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Dressing.Difficulty.UPDRS2.Num', 'Dressing.Difficulty.UPDRS2.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Hygiene.Difficulty.UPDRS2.Num', 'Hygiene.Difficulty.UPDRS2.Num.Scaled', 0, 4) 
    ppmi_merge_filtered = create_scaled_col(ppmi_merge_filtered, 'Speech.Difficulty.UPDRS3.Num', 'Speech.Difficulty.UPDRS3.Num.Scaled', 0, 4) 
    ppmi_merge_filtered['Domain6.Scaled'] = ppmi_merge_filtered[['Chewing.Swallowing.Difficulty.UPDRS2.Num.Scaled','Eating.Difficulty.UPDRS2.Num.Scaled', 'Dressing.Difficulty.UPDRS2.Num.Scaled','Hygiene.Difficulty.UPDRS2.Num.Scaled', 'Speech.Difficulty.UPDRS3.Num.Scaled' ]].sum(axis=1, min_count=1)


    cdir = '/Users/areardon/Desktop/Projects/PPMI_Merge/PPMI_Study_Data_Download/'
    MCI_df = pd.read_csv(cdir + 'PPMI_Original_Cohort_BL_to_Year_5_Dataset_Apr2020.csv')
    MCI_df = MCI_df[['PATNO', 'visit_date', 'MCI_testscores']]
    MCI_df['visit_date'] = MCI_df['visit_date'].apply(lambda x: datetime.datetime.strptime(x, "%b%Y").strftime("%m/%Y"))
    MCI_df = MCI_df.rename(columns = {'PATNO' : 'Subject.ID'})
    MCI_df = MCI_df.rename(columns = {'visit_date' : 'Event.ID.Date'})


    ## Merge MCI into main df 
    ppmi_merge_filtered = pd.merge(ppmi_merge_filtered, MCI_df, on = ['Subject.ID', 'Event.ID.Date'], how = "left")
    
    
    ## Calculate Domain Ns
    ## Domain 1 DONE
    ppmi_merge_filtered['WB.N'] = ''
    for row_num in range(len(ppmi_merge_filtered['Subject.ID'])) :
        count = 0
        if ppmi_merge_filtered['Walking.Difficulty.UPDRS2.Num'].loc[row_num]>=3 :
            count += 1
        if ppmi_merge_filtered['Freezing.while.Walking.UPDRS2.Num'].loc[row_num]>=3 : 
            count += 1
        if ppmi_merge_filtered['Gait.Problems.UPDRS3.Num'].loc[row_num]>=3 : 
            count += 1
        if ppmi_merge_filtered['Freezing.of.Gait.UPDRS3.Num'].loc[row_num]==4 : 
            count += 1 
        if ppmi_merge_filtered['Postural.Stability.Problems.UPDRS3.Num'].loc[row_num]>=3 : 
            count += 1 
        if ppmi_merge_filtered['Hoehn.and.Yahr.Stage.UPDRS3.Num'].loc[row_num]>=4 : 
            count += 1 
        ppmi_merge_filtered['WB.N'].loc[row_num] = count 
    


    ## Domain 2 DONE
    ppmi_merge_filtered['Motor.N'] = ''
    ppmi_merge_filtered['Dyskinesias'] = ''
    for row_num in range(len(ppmi_merge_filtered['Subject.ID'])) :
        count = 0
        if (ppmi_merge_filtered['Time.Spent.with.Dyskinesias.UPDRS4.Num'].loc[row_num]>=3) & (ppmi_merge_filtered['Functional.Impact.of.Dyskinesias.UPDRS4.Num'].loc[row_num] >= 3) : 
            count += 1 
            ppmi_merge_filtered['Dyskinesias'].loc[row_num] = 1
        if ppmi_merge_filtered['Functional.Impact.Fluctuations.UPDRS4.Num'].loc[row_num] >= 3 :
            count += 1 
        if ppmi_merge_filtered['Complexity.of.Motor.Fluctuations.UPDRS4.Num'].loc[row_num]>=3 :
            count += 1 
        ppmi_merge_filtered['Motor.N'].loc[row_num] = count 


    # ## Domain 3 DONE
    ppmi_merge_filtered['Cog.N'] = ''
    ppmi_merge_filtered['Dimentia.Composite'] = ''
    for row_num in range(len(ppmi_merge_filtered['Subject.ID'])) :
        count = 0
        cog_count = 0
        if ppmi_merge_filtered['MOCA.Total'].loc[row_num]<21  :
            count += 1 
        if ppmi_merge_filtered['Cognitive.Impairment.UPDRS1.Num'].loc[row_num]>= 3 :
            count += 1    
        if ppmi_merge_filtered['Hallucinations.and.Psychosis.UPDRS1.Num'].loc[row_num]>= 3 :
            count += 1    
        if ppmi_merge_filtered['Apathy.UPDRS1.Num'].loc[row_num]>= 3 :
            count += 1    
        if ppmi_merge_filtered['Cognitive.State'].loc[row_num] == 1 : # Dimentia
            count += 1      

        ## COGNITIVE TESTING FIXME NOT SURE IF THIS IS CORRECT 
        if ppmi_merge_filtered['DVT_RECOG_DISC_INDEX.Zscore'].loc[row_num] <= -1.5 : 
            cog_count += 1
        if ppmi_merge_filtered['DVT.Total.RECALL.Zscore'].loc[row_num] <= -1.5 : 
            cog_count += 1                   
        if ppmi_merge_filtered['JLO_TOTRAW.Zscore'].loc[row_num] <= -1.5 : 
            cog_count += 1
        if ppmi_merge_filtered['Symbol.Digit.Modalities.Total.Zscore'].loc[row_num] <= -1.5 : 
            cog_count += 1
        if ppmi_merge_filtered['Letter.Number.Sequencing.Total.Zscore'].loc[row_num] <= -1.5 : 
            cog_count += 1       
        if ppmi_merge_filtered['Sematnic.Fluency.TScore.Zscore'].loc[row_num] <= -1.5 : 
            cog_count += 1       
        if cog_count >= 2 :
            if ppmi_merge_filtered['Functional.Cognitive.Impairment'].loc[row_num] == 1 : 
                count += 1 
                ppmi_merge_filtered['Dimentia.Composite'].loc[row_num] = 1
        ppmi_merge_filtered['Cog.N'].loc[row_num] = count         
    

    ## Domain 4 DONE
    ppmi_merge_filtered['Automic.N'] = ''
    ppmi_merge_filtered['Orthostatic Hypotension'] = ''
    ppmi_merge_filtered['Incontinence'] = ''
    for row_num in range(len(ppmi_merge_filtered['Subject.ID'])) :
        count = 0
        if ppmi_merge_filtered['Urinary.Problems.UPDRS1.Num'].loc[row_num]>=3 :
            if (ppmi_merge_filtered['SCAU8'].loc[row_num]>=2) | (ppmi_merge_filtered['SCAU9'].loc[row_num]>=2) :
                count += 1 
                ppmi_merge_filtered['Incontinence'].loc[row_num] = 1
        if ppmi_merge_filtered['SCAU15'].loc[row_num]>=2 :         
            if ppmi_merge_filtered['sys.bp.diff'].loc[row_num]  >= 20 : 
                if ppmi_merge_filtered['dia.bp.diff'].loc[row_num]  >= 10 : # FIXME CHECK
                    count += 1    
                    ppmi_merge_filtered['Orthostatic Hypotension'].loc[row_num] = 1
        if ppmi_merge_filtered['Lightheadedness.on.Standing.UPDRS1.Num'].loc[row_num]==4 :
            count += 1     
        if ppmi_merge_filtered['SCAU16'].loc[row_num]>=1 :
            count += 1     
        ppmi_merge_filtered['Automic.N'].loc[row_num] = count 



    ## Domain 5 DONE
    ppmi_merge_filtered['FI.N'] = ''
    for row_num in range(len(ppmi_merge_filtered['Subject.ID'])) :
        count = 0
        if ppmi_merge_filtered['MSEADLG'].iloc[row_num] < 80 : 
            count+=1 
        ppmi_merge_filtered['FI.N'].loc[row_num] = count 


    ## Domain 6 DONE
    ppmi_merge_filtered['ADL.N'] = '' 
    for row_num in range(len(ppmi_merge_filtered['Subject.ID'])) :
        count = 0
        if ppmi_merge_filtered['Chewing.Swallowing.Difficulty.UPDRS2.Num'].iloc[row_num] >= 3 :
            count +=1
        if ppmi_merge_filtered['Eating.Difficulty.UPDRS2.Num'].iloc[row_num] >= 3 :
            count +=1
        if ppmi_merge_filtered['Dressing.Difficulty.UPDRS2.Num'].iloc[row_num] >= 3 :
            count +=1            
        if ppmi_merge_filtered['Hygiene.Difficulty.UPDRS2.Num'].iloc[row_num] >= 3 :
            count +=1
        if ppmi_merge_filtered['Speech.Difficulty.UPDRS3.Num'].iloc[row_num] >= 3 :
            count +=1
        ppmi_merge_filtered['ADL.N'].loc[row_num] = count 
    ppmi_merge_filtered.to_csv('/Users/areardon/Desktop/milestones' + v + '.csv')


    # ## Sum milestones for each domain 
    ppmi_merge_filtered = pd.read_csv('/Users/areardon/Desktop/milestones' + v + '.csv')
    ppmi_merge_filtered.fillna(np.nan, inplace = True)
    ppmi_merge_filtered['milestoneScore.WB'] = ppmi_merge_filtered[['Walking.Difficulty.UPDRS2.Num.Scaled',	'Freezing.while.Walking.UPDRS2.Num.Scaled',	'Gait.Problems.UPDRS3.Num.Scaled',	'Freezing.of.Gait.UPDRS3.Num.Scaled',	'Postural.Stability.Problems.UPDRS3.Num.Scaled', 'Hoehn.and.Yahr.Stage.UPDRS3.Num.Scaled']].sum(axis=1, min_count = 1)
    ppmi_merge_filtered['milestoneScore.Motor'] = ppmi_merge_filtered[['Time.Spent.with.Dyskinesias.UPDRS4.Num.Scaled', 'Functional.Impact.of.Dyskinesias.UPDRS4.Num.Scaled','Functional.Impact.Fluctuations.UPDRS4.Num.Scaled','Complexity.of.Motor.Fluctuations.UPDRS4.Num.Scaled']].sum(axis=1, min_count=1)
    ppmi_merge_filtered['milestoneScore.COG'] = ppmi_merge_filtered[['MOCA.Total.Scaled','Cognitive.Impairment.UPDRS1.Num.Scaled','Hallucinations.and.Psychosis.UPDRS1.Num.Scaled','Apathy.UPDRS1.Num.Scaled','Cognitive.State.Scaled', 'DVT.Total.RECALL.Scaled','DVT_RECOG_DISC_INDEX.Scaled', 'JLO_TOTRAW.Scaled','Symbol.Digit.Modalities.Total.Scaled','Letter.Number.Sequencing.Total.Scaled','Sematnic.Fluency.TScore.Scaled', 'Functional.Cognitive.Impairment.Scaled']].sum(axis=1, min_count=1)
    ppmi_merge_filtered['milestoneScore.FI'] = ppmi_merge_filtered[['MSEADLG.Scaled']]
    ppmi_merge_filtered['milestoneScore.Autonomic'] = ppmi_merge_filtered[['Urinary.Problems.UPDRS1.Num.Scaled','SCAU8.Scaled','SCAU9.Scaled','SCAU15.Scaled','sys.bp.diff.Scaled','dia.bp.diff.Scaled', 'Lightheadedness.on.Standing.UPDRS1.Num.Scaled','SCAU16.Scaled']].sum(axis=1, min_count=1)
    ppmi_merge_filtered['milestoneScore.ADL'] = ppmi_merge_filtered[['Chewing.Swallowing.Difficulty.UPDRS2.Num.Scaled','Eating.Difficulty.UPDRS2.Num.Scaled', 'Dressing.Difficulty.UPDRS2.Num.Scaled','Hygiene.Difficulty.UPDRS2.Num.Scaled', 'Speech.Difficulty.UPDRS3.Num.Scaled' ]].sum(axis=1, min_count=1)
    ppmi_merge_filtered['milestonesReached'] = ppmi_merge_filtered[['WB.N',	'Motor.N',	'Cog.N',	'Automic.N',	'FI.N',	'ADL.N']].sum(axis=1, min_count=1)


    # Fill in zeros that should be nans with nans
    for row_num in range(len(ppmi_merge_filtered['Subject.ID'])) : 
        if isNan(ppmi_merge_filtered['milestoneScore.Motor'].loc[row_num]) & isNan(ppmi_merge_filtered['milestoneScore.COG'].loc[row_num]) & isNan(ppmi_merge_filtered['milestoneScore.Autonomic'].loc[row_num]) & isNan(ppmi_merge_filtered['milestoneScore.FI'].loc[row_num]) & isNan(ppmi_merge_filtered['milestoneScore.ADL'].loc[row_num]) :
            ppmi_merge_filtered['milestonesReached'].loc[row_num] = np.nan
    ppmi_merge_filtered['milestonesReached'].fillna('REMOVE', inplace = True)
    ppmi_merge_filtered = ppmi_merge_filtered[ppmi_merge_filtered['milestonesReached'] != 'REMOVE']
    ppmi_merge_filtered.to_csv(savedir + 'milestones' + v + '.csv')

    ## Save condensed verion of milestones 
    temp = ppmi_merge_filtered
    temp = temp[['Subject.ID',	'Event.ID',	'Event.ID.Date','WB.N',	'Motor.N',	'Cog.N',	'Automic.N',	'FI.N',	'ADL.N','milestonesReached','milestoneScore.WB', 'milestoneScore.Motor','milestoneScore.COG','milestoneScore.Autonomic','milestoneScore.FI','milestoneScore.ADL']]
    temp = temp.drop_duplicates()
    temp.to_csv(savedir + '/condensed_milestones' + v + '.csv')
    jaentl





def create_scaled_col(df, old_col_name, new_col_name, min, max) :
    df[new_col_name] = ''
    for row_num in range(len(df[old_col_name])):
        if not_NaN(df[old_col_name].loc[row_num]) : 
            df[new_col_name].loc[row_num] = (df[old_col_name].loc[row_num] - min) / (max-min)
    return df 



def create_bp_scaled_col(df, old_col_name, new_col_name, dif) :
    df[new_col_name] = ''
    for row_num in range(len(df[old_col_name])):
        if not_NaN(df[old_col_name].loc[row_num]) : 
            if df[old_col_name].loc[row_num] >= dif : 
                df[new_col_name].loc[row_num] = 1
            else : 
                df[new_col_name].loc[row_num] = 0
    return df 




def create_reversed_scaled_col(df, old_col_name, new_col_name, min, max):
    df[new_col_name] = ''
    for row_num in range(len(df[old_col_name])):
        if not_NaN(df[old_col_name].loc[row_num]) : 
            df[new_col_name].loc[row_num] = 1 - ((df[old_col_name].loc[row_num] - min) / (max-min))
    return df 



def not_NaN(num):
    return num == num



def isNan(x):
    return (x is np.nan or x != x)



if __name__=="__main__":
    main()
