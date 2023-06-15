import pandas as pd
import numpy as np
from datetime import datetime
from dateutil import relativedelta
from io import StringIO
import re
from typing import List
import boto3


userdir = '/Users/areardon/Desktop/Projects/PPMI_Merge2_20230523/'
df = pd.read_csv(userdir + 'ppmi_merge_v0.1.0.csv')
print(df['T1Hier_vol_bn_gp_gpi_leftdeep_cit168'])

janetl

def main() :
    
    # Set up paths
    userdir = '/Users/areardon/Desktop/Projects/PPMI_Merge2_20230523/'
    ppmi_download_path = userdir + 'PPMI_Study_Downloads_20230523/'
    genetics_path = userdir + 'genetic_data/'
    datiq_path = userdir + 'datiq/'
    invicro_data = userdir + 'invicro_data/'
    version = '0.1.0'
    code_list = pd.read_csv(ppmi_download_path + 'Code_List_-__Annotated__23May2023.csv') # FIXME OR HARMONIZED?


    #### CLINICAL INFO ####
    ## Create cohort df
    xlsx = pd.ExcelFile(ppmi_download_path + 'Consensus_Committee_Analytic_Datasets_23Sep2022.xlsx') # Read in main xlsx file
    full_df = create_cohort_df(xlsx) 
    full_df = decode(full_df, code_list, 'PATIENT_STATUS', ['PHENOCNV'])
    full_df.rename(columns = {'Cohort' : 'Enroll.Diagnosis' , 'PHENOCNV' : 'Subject.Phenoconverted'}, inplace = True)
    full_df = full_df[['PATNO', 'Enroll.Diagnosis', 'Enroll.Subtype', 'Consensus.Diagnosis', 'Consensus.Subtype','Subject.Phenoconverted','DIAG1','DIAG1VIS', 'DIAG2','DIAG2VIS']] # Reorganize column order


    # ## Add in age info at each visit
    # ppmi_merge = merge_csv(ppmi_download_path, full_df, 'Age_at_visit_23May2023.csv', ['PATNO', 'EVENT_ID', 'AGE_AT_VISIT'], merge_on = ['PATNO'], merge_how = "outer")
    # ppmi_merge['EVENT_ID'].fillna('SC', inplace = True) # One subject (41358) has event_id as NaN - replace with 'SC' because later has a screening event id that we will merge info on for this sub


    # ## Add demographics, vital signs, and pd diagnosis history info, final event id and diagnosi change, dominant side of disease
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Demographics_23May2023.csv', ['PATNO','EVENT_ID','SEX', 'HANDED', 'BIRTHDT','AFICBERB','ASHKJEW','BASQUE', 'HISPLAT', 'RAASIAN', 'RABLACK', 'RAHAWOPI', 'RAINDALS', 'RANOS', 'RAWHITE'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer") # Bday, sex, handedness, race
    # ppmi_merge = decode(ppmi_merge, code_list, 'SCREEN', ['SEX', 'HANDED','AFICBERB','ASHKJEW','BASQUE', 'HISPLAT', 'RAASIAN', 'RABLACK', 'RAHAWOPI', 'RAINDALS', 'RANOS', 'RAWHITE'])
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Vital_Signs_23May2023.csv', ['PATNO','EVENT_ID','INFODT', 'WGTKG', 'HTCM', 'SYSSUP', 'DIASUP', 'SYSSTND', 'DIASTND'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer") # Visit date, weight and height
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge,  'PD_Diagnosis_History_23May2023.csv', ['PATNO', 'EVENT_ID', 'SXDT','PDDXDT'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer") # First symptom date, PD diagnosis date
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'SCOPA-AUT_23May2023.csv', ['PATNO', 'EVENT_ID', 'SCAU8', 'SCAU9', 'SCAU15', 'SCAU16'] , merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Modified_Schwab___England_Activities_of_Daily_Living_23May2023.csv', ['PATNO', 'EVENT_ID','MSEADLG'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")


    # ## Decode variables
    # ppmi_merge.rename(columns = {'AGE_AT_VISIT' : 'Age', 'SEX' : 'Sex', 'HANDED' : 'Handed', 'BIRTHDT' : 'BirthDate', 'WGTKG' : 'Weight(kg)', 'HTCM' : 'Height(cm)','SYSSUP':'Systolic.BP.Sitting', 'DIASUP' : 'Diastolic.BP.Sitting', 'SYSSTND' : 'Systolic.BP.Standing', 'DIASTND': 'Diastolic.BP.Standing', 'SXDT' : 'First.Symptom.Date', 'PDDXDT': 'PD.Diagnosis.Date', 'AFICBERB' : 'African.Berber.Race','ASHKJEW':'Ashkenazi.Jewish.Race', 'BASQUE' : 'Basque.Race', 'HISPLAT' : 'Hispanic.Latino.Race', 'RAASIAN' : 'Asian.Race', 'RABLACK' : 'African.American.Race', 'RAHAWOPI' : 'Hawian.Other.Pacific.Islander.Race', 'RAINDALS' : 'Indian.Alaska.Native.Race', 'RANOS' : 'Not.Specified.Race', 'RAWHITE': 'White.Race'}, inplace = True) # Rename columns
    # ppmi_merge = add_PD_Disease_Duration(ppmi_merge, 'PD.Diagnosis.Duration')
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Conclusion_of_Study_Participation_23May2023.csv', ['PATNO', 'EVENT_ID', 'COMPLT', 'WDRSN', 'WDDT'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer") # completed study, whithdrawal reason, withdrawal date
    # ppmi_merge = decode(ppmi_merge, code_list, 'CONCL', ['COMPLT', 'WDRSN'])    
    # ppmi_merge.rename(columns = {'COMPLT' : 'Completed.Study' , 'WDRSN': 'Reason.for.Withdrawal','WDDT' : 'Withdrawal.Date'}, inplace = True)
    # ppmi_merge = add_diagnosis_change(full_df, ppmi_merge)


    # ## Dominant side of disease
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'PPMI_Original_Cohort_BL_to_Year_5_Dataset_Apr2020.csv',['PATNO', 'EVENT_ID', 'DOMSIDE'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer") # Domside
    # ppmi_merge = decode(ppmi_merge, code_list, 'PDDXHIST', ['DOMSIDE']) 
       

    # ## Participant Motor Function Questionnaire
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Participant_Motor_Function_Questionnaire_23May2023.csv', ['PATNO', 'EVENT_ID', 'PAG_NAME', 'CMPLBY2', 'TRBUPCHR', 'WRTSMLR', 'VOICSFTR', 'POORBAL', 'FTSTUCK', 'LSSXPRSS', 'ARMLGSHK', 'TRBBUTTN', 'SHUFFLE', 'MVSLOW', 'TOLDPD'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge = decode(ppmi_merge, code_list, 'PQUEST', ['CMPLBY2', 'PAG_NAME','TRBUPCHR', 'WRTSMLR', 'VOICSFTR', 'POORBAL', 'FTSTUCK', 'LSSXPRSS', 'ARMLGSHK', 'TRBBUTTN', 'SHUFFLE', 'MVSLOW', 'TOLDPD'])   
    # ppmi_merge = ppmi_merge.rename(columns = {'PAG_NAME' : 'Motor.Function.Page.Name', 'CMPLBY2' : 'Motor.Function.Source', 'TRBUPCHR' : 'Trouble.Rising.Chair', 'WRTSMLR' : 'Writing.Smaller', 'VOICSFTR' : 'Voice.Softer' , 'POORBAL': 'Poor.Balance' , 'FTSTUCK' : 'Feet.Stuck', 'LSSXPRSS' : 'Less.Expressive' , 'ARMLGSHK':'Arms/Legs.Shake', 'TRBBUTTN' : 'Trouble.Buttons' , 'SHUFFLE' : 'Shuffle.Feet' , 'MVSLOW' : 'Slow.Movements' , 'TOLDPD' : 'Been.Told.PD' })


    # ## Cognitive symptoms - Cognitive Categorization
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Cognitive_Categorization_23May2023.csv',['PATNO' , 'EVENT_ID', 'PAG_NAME', 'COGDECLN', 'FNCDTCOG' , 'COGDXCL' ,'PTCGBOTH' , 'COGSTATE' , 'COGCAT_TEXT'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer") # Visit date, weight and height
    # ppmi_merge = decode(ppmi_merge, code_list, 'COGCATG',['PAG_NAME', 'COGDECLN', 'FNCDTCOG' , 'COGDXCL' ,'PTCGBOTH' , 'COGSTATE' , 'COGCAT_TEXT'])
    # ppmi_merge = ppmi_merge.rename(columns = {'PAG_NAME' : 'Cognitive.Page.Name', 'COGDECLN' : 'Cognitive.Decline', 'FNCDTCOG' : 'Functional.Cognitive.Impairment', 'COGDXCL' : 'Confidence.Level.Cognitive.Diagnosis', 'PTCGBOTH' : 'Cognitive.Source', 'COGSTATE' : 'Cognitive.State' , 'COGCAT_TEXT' : 'Cognitive.Tscore.Cat'})


    # ## MOCA, Medication, LEDD, and comorbidities, Education, Analytic Cohort column 
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Montreal_Cognitive_Assessment__MoCA__23May2023.csv',['PATNO', 'EVENT_ID', 'MCATOT'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge.rename(columns = {'MCATOT' : 'MOCA.Total'}, inplace = True) # Rename
    # ppmi_merge = add_concomitant_med_log(ppmi_merge, ppmi_download_path)
    # ppmi_merge = add_LEDD(ppmi_merge, ppmi_download_path)
    # ppmi_merge = make_categorical_LEDD_col(ppmi_merge, 'LEDD.sum', 'LEDD.sum.Cat', 3)
    # ppmi_merge = make_categorical_LEDD_col(ppmi_merge, 'LEDD.ongoing.sum', 'LEDD.ongoing.sum.Cat',3)
    # ppmi_merge = add_comorbidities(ppmi_merge, ppmi_download_path)
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Socio-Economics_23May2023.csv', ['PATNO', 'EVENT_ID', 'EDUCYRS'], merge_on = ['PATNO'], merge_how = "outer") # Add education in years
    # ppmi_merge.rename(columns = {'EDUCYRS' : 'Education.Years'}, inplace = True) # Rename
    

    # ## Reindex
    # ppmi_merge = ppmi_merge.reindex(columns = ['PATNO', 'EVENT_ID', 'INFODT' , 'Enroll.Diagnosis', 'Enroll.Subtype', 'Consensus.Diagnosis', 'Consensus.Subtype','Analytic.Cohort','Subject.Phenoconverted','First.Diagnosis.Change', 'Second.Diagnosis.Change',  'First.Symptom.Date', 'PD.Diagnosis.Date', 'PD.Diagnosis.Duration','BirthDate', 'Age', 'Sex', 'Handed', 'Weight(kg)',    'Height(cm)', 'Systolic.BP.Sitting', 'Diastolic.BP.Sitting',  'Systolic.BP.Standing',  'Diastolic.BP.Standing', 'SCAU8', 'SCAU9', 'SCAU15', 'SCAU16', 'MSEADLG', 'Education.Years', 'DOMSIDE', 'African.Berber.Race','Ashkenazi.Jewish.Race', 'Basque.Race', 'Hispanic.Latino.Race', 'Asian.Race', 'African.American.Race', 'Hawian.Other.Pacific.Islander.Race', 'Indian.Alaska.Native.Race', 'Not.Specified.Race',  'White.Race', 'Motor.Function.Page.Name',    'Motor.Function.Source',    'Trouble.Rising.Chair',    'Writing.Smaller',    'Voice.Softer',    'Poor.Balance',    'Feet.Stuck',    'Less.Expressive',    'Arms/Legs.Shake',    'Trouble.Buttons',    'Shuffle.Feet',    'Slow.Movements',    'Been.Told.PD',    'Cognitive.Page.Name',    'Cognitive.Source', 'Cognitive.Decline',    'Functional.Cognitive.Impairment',    'Confidence.Level.Cognitive.Diagnosis',    'Cognitive.State',    'Cognitive.Tscore.Cat',    'MOCA.Total', 'Medication' ,'LEDD.sum', 'LEDD.sum.Cat', 'LEDD.ongoing.sum','LEDD.ongoing.sum.Cat','Medical.History.Description(Diagnosis.Date)'])


    # ## Add in other csvs
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Modified_Boston_Naming_Test_23May2023.csv', ['PATNO', 'EVENT_ID', 'MBSTNSCR', 'MBSTNCRC', 'MBSTNCRR'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Clock_Drawing_23May2023.csv', ['PATNO', 'EVENT_ID', 'CLCKTOT'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Benton_Judgement_of_Line_Orientation_23May2023.csv', ['PATNO', 'EVENT_ID', 'JLO_TOTCALC','JLO_TOTRAW'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Letter_-_Number_Sequencing_23May2023.csv', ['PATNO', 'EVENT_ID', 'LNS_TOTRAW'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Modified_Semantic_Fluency_23May2023.csv', ['PATNO', 'EVENT_ID', 'DVS_SFTANIM', 'DVT_SFTANIM'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Hopkins_Verbal_Learning_Test_-_Revised_23May2023.csv',['PATNO', 'EVENT_ID', 'DVT_DELAYED_RECALL', 'DVT_TOTAL_RECALL','DVT_RECOG_DISC_INDEX','DVT_RETENTION'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'Symbol_Digit_Modalities_Test_23May2023.csv', ['PATNO', 'EVENT_ID', 'SDMTOTAL'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge.rename(columns = {'CLCKTOT' : 'Clock.Drawing.Total', 'JLOTOTCALC' : 'JOLO.Total', 'LNS_TOTRAW' : 'Letter.Number.Sequencing.Total','DVS_SFTANIM' : 'Semantic.Fluency.Scaled.Score', 'DVT_SFTANIM' :'Sematnic.Fluency.TScore', 'DVT_TOTAL_RECALL' : 'DVT.Total.RECALL','SDMTOTAL' : 'Symbol.Digit.Modalities.Total'}, inplace = True)


    # ## REM Sleeep behavior disorder questionnaire
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge, 'REM_Sleep_Behavior_Disorder_Questionnaire_23May2023.csv', ['PATNO', 'EVENT_ID', 'PAG_NAME', 'PTCGBOTH', 'DRMVIVID', 'DRMAGRAC', 'DRMNOCTB', 'SLPLMBMV', 'SLPINJUR', 'DRMVERBL', 'DRMFIGHT', 'DRMUMV', 'DRMOBJFL', 'MVAWAKEN',    'DRMREMEM',    'SLPDSTRB',    'STROKE', 'HETRA', 'PARKISM', 'RLS', 'NARCLPSY', 'DEPRS', 'EPILEPSY', 'BRNINFM', 'CNSOTH'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge = decode(ppmi_merge, code_list, 'REMSLEEP', ['PAG_NAME','DRMVIVID',    'DRMAGRAC',    'DRMNOCTB',    'SLPLMBMV',    'SLPINJUR',    'DRMVERBL',    'DRMFIGHT',    'DRMUMV',    'DRMOBJFL',    'MVAWAKEN',    'DRMREMEM',    'SLPDSTRB',    'STROKE',    'HETRA',    'PARKISM',    'RLS','NARCLPSY',    'DEPRS',    'EPILEPSY',    'BRNINFM',    'CNSOTH' ])
    # ppmi_merge['RBDTotal.REM'] = ppmi_merge[['DRMVIVID',    'DRMAGRAC',    'DRMNOCTB',    'SLPLMBMV',    'SLPINJUR',    'DRMVERBL',    'DRMFIGHT',    'DRMUMV',    'DRMOBJFL',    'MVAWAKEN',    'DRMREMEM',    'SLPDSTRB',    'STROKE',    'HETRA',    'PARKISM',    'RLS','NARCLPSY',    'DEPRS',    'EPILEPSY',    'BRNINFM',    'CNSOTH']].sum(axis = 1) # Add an RBDTotal.REM column
    # ppmi_merge.rename(columns = {'PAG_NAME' : 'REM.Sleep.Behavior.Disorder.Page.Name', 'PTCGBOTH' : 'Sleep.Behavior.Source.REM','DRMVIVID' : 'Vivid.Dreams.REM' , 'DRMAGRAC': 'Aggressive.or.Action-packed.Dreams.REM',    'DRMNOCTB':'Nocturnal.Behaviour.REM','SLPLMBMV':'Move.Arms/legs.During.Sleep.REM', 'SLPINJUR':'Hurt.Bed.Partner.REM',    'DRMVERBL':'Speaking.in.Sleep.REM',    'DRMFIGHT': 'Sudden.Limb.Movements.REM',    'DRMUMV':'Complex.Movements.REM',    'DRMOBJFL':'Things.Fell.Down.REM',    'MVAWAKEN':'My.Movements.Awake.Me.REM',    'DRMREMEM':'Remember.Dreams.REM',    'SLPDSTRB':'Sleep.is.Disturbed.REM',    'STROKE':'Stroke.REM',    'HETRA':'Head.Trauma.REM',    'PARKISM':'Parkinsonism.REM',    'RLS':'RLS.REM',    'NARCLPSY':'Narcolepsy.REM',    'DEPRS':'Depression.REM',    'EPILEPSY':'Epilepsy.REM',    'BRNINFM':'Inflammatory.Disease.of.the.Brain.REM',    'CNSOTH':'Other.REM'}, inplace = True)



    # #### IMAGING INFO ####
    # # FIXME - laterality issue?  SUV ?
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge,'DaTScan_Analysis_23May2023.csv', ['PATNO','EVENT_ID','DATSCAN_DATE','DATSCAN_CAUDATE_R','DATSCAN_CAUDATE_L','DATSCAN_PUTAMEN_R','DATSCAN_PUTAMEN_L','DATSCAN_ANALYZED','DATSCAN_NOT_ANALYZED_REASON'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge = merge_csv(ppmi_download_path, ppmi_merge,'DaTScan_Imaging_23May2023.csv', ['PATNO','EVENT_ID','PAG_NAME','INFODT','DATSCAN','PREVDATDT','SCNLOC','SCNINJCT','VSINTRPT','VSRPTELG'], merge_on = ['PATNO', 'EVENT_ID'], merge_how = "outer")
    # ppmi_merge = decode(ppmi_merge, code_list, 'DATSCAN', ['DATSCAN', 'SCNLOC','SCNINJCT', 'VSINTRPT','VSRPTELG'])
    # ppmi_merge.rename(columns = {'INFODT_x' : 'INFODT', 'INFODT_y' : 'DaTScan.INFODT', 'SCNLOC' : 'Location.Scan.Completed' , 'PREVDATDT' : 'Date.DaTscan.Imaging.Completed.Previously', 'SCNINJCT' : 'Scan.Injection', 'VSINTRPT' : 'Visual.Interpretation.Report', 'VSRPTELG' : 'Visual.Interpretation.Report(eligible/not)'}, inplace = True)
    # ppmi_merge['INFODT'].fillna(ppmi_merge['DaTScan.INFODT'], inplace = True) # Fill in NaN infodts with datscan infodts if NA
    # ppmi_merge = remove_duplicate_datscans(ppmi_merge) # FIXME - After merging in datscan files, duplicate event ids being created one with DATSCAN as "Completed" one with DATSCAN as "not completed" - if there are both of these - keep only "Completed"
    # ppmi_merge = add_datiq(ppmi_merge, datiq_path)
    # ppmi_merge = add_mri_csv(ppmi_merge, ppmi_download_path, code_list)
    # ppmi_merge = add_t1(ppmi_merge)


    # #### UPDRS NUMERIC ####
    # updrs_part1 = read_csv_drop_cols(ppmi_download_path, 'MDS-UPDRS_Part_I_23May2023.csv',['ORIG_ENTRY','LAST_UPDATE','REC_ID'], drop = True)
    # updrs_part1 = decode(updrs_part1, code_list, 'NUPDRS1', ['PAG_NAME', 'NUPSOURC'])
    # updrs_part1.rename(columns = {'PAG_NAME' : 'Page.Name.UPDRS1', 'NUPSOURC' : 'NUPSOURC.UPDRS1'}, inplace = True)
    
    # updrs_part1_pq = read_csv_drop_cols(ppmi_download_path, 'MDS-UPDRS_Part_I_Patient_Questionnaire_23May2023.csv', ['ORIG_ENTRY','LAST_UPDATE','REC_ID','INFODT'], drop = True)
    # updrs_part1_pq = decode(updrs_part1_pq, code_list, 'NUPDRS1P', ['PAG_NAME', 'NUPSOURC'])
    # updrs_part1_pq.rename(columns = {'PAG_NAME' : 'Page.Name.UPDRS1PQ','NUPSOURC' : 'NUPSOURC.UPDRS1PQ'}, inplace = True)
    
    # updrs_part2 = read_csv_drop_cols(ppmi_download_path,'MDS_UPDRS_Part_II__Patient_Questionnaire_23May2023.csv', ['ORIG_ENTRY','LAST_UPDATE','REC_ID','INFODT'], drop = True)
    # updrs_part2 = decode(updrs_part2, code_list, 'NUPDRS2P', ['PAG_NAME', 'NUPSOURC'])
    # updrs_part2.rename(columns = {'PAG_NAME' : 'Page.Name.UPDRS2', 'NUPSOURC' : 'NUPSOURC.UPDRS2'}, inplace = True) 

    # updrs_part3 = read_csv_drop_cols(ppmi_download_path, 'MDS-UPDRS_Part_III_23May2023.csv', ['ORIG_ENTRY','LAST_UPDATE','REC_ID','INFODT'], drop=True)
    # updrs_part3 = decode(updrs_part3, code_list, 'NUPDRS3TRT', ['PAG_NAME'])
    # updrs_part3.rename(columns = {'PAG_NAME' : 'Page.Name.UPDRS3'}, inplace = True)

    # updrs_part4 = read_csv_drop_cols(ppmi_download_path,'MDS-UPDRS_Part_IV__Motor_Complications_23May2023.csv', ['ORIG_ENTRY','LAST_UPDATE','REC_ID','INFODT'], drop = True)
    # updrs_part4 = decode(updrs_part4, code_list, 'NUPDRS4', ['PAG_NAME'])
    # updrs_part4.rename(columns = {'PAG_NAME' : 'Page.Name.UPDRS4'}, inplace = True) 


    # # Create one df for updrs_numeric
    # updrs_temp = pd.merge(updrs_part1, updrs_part1_pq , on = ['PATNO', 'EVENT_ID'], how = "outer")
    # updrs_temp= pd.merge(updrs_temp, updrs_part2 , on = ['PATNO', 'EVENT_ID'], how = "outer")
    # updrs_temp = pd.merge(updrs_temp, updrs_part3, on = ['PATNO', 'EVENT_ID'], how = "outer")
    # updrs_temp = pd.merge(updrs_temp, updrs_part4, on = ['PATNO', 'EVENT_ID'], how = "outer")
    # updrs_cat = updrs_temp.copy()
    
    # updrs_part1 = add_extension_to_column_names(updrs_part1, ['PATNO','EVENT_ID','INFODT'], '.UPDRS1')
    # updrs_part1_pq = add_extension_to_column_names(updrs_part1_pq, ['PATNO','EVENT_ID','INFODT'], '.UPDRS1')
    # updrs_part2 = add_extension_to_column_names(updrs_part2, ['PATNO','EVENT_ID','INFODT'], '.UPDRS2')
    # updrs_part3 = add_extension_to_column_names(updrs_part3, ['PATNO','EVENT_ID','INFODT'], '.UPDRS3')
    # updrs_part4 = add_extension_to_column_names(updrs_part4, ['PATNO','EVENT_ID','INFODT'], '.UPDRS4')

    # updrs_numeric = pd.merge(updrs_part1, updrs_part1_pq , on = ['PATNO', 'EVENT_ID'], how = "outer")
    # updrs_numeric = pd.merge(updrs_numeric, updrs_part2 , on = ['PATNO', 'EVENT_ID'], how = "outer")
    # updrs_numeric = pd.merge(updrs_numeric, updrs_part3, on = ['PATNO', 'EVENT_ID'], how = "outer")
    # updrs_numeric = pd.merge(updrs_numeric, updrs_part4, on = ['PATNO', 'EVENT_ID'], how = "outer")
    # updrs_numeric = keep_only_numeric_variables_updrs(updrs_numeric)


    # # Change all UPDRS dataframe cols begin with 'N' to floats
    # updrs_numeric = change_updrs_to_floats(updrs_numeric)
    
    # # Rename columns in updrs_numeric
    # updrs_numeric.rename(columns = {'NHY.UPDRS3' : 'Hoehn.and.Yahr.Stage.UPDRS3', 'NP3BRADY.UPDRS3' : 'Global.Spontaneity.of.Movement.UPDRS3', 'NP3PTRMR.UPDRS3' : 'Postural.Tremor.Right.Hand.UPDRS3' , 'NP3PTRML.UPDRS3' : 'Postural.Tremor.Left.Hand.UPDRS3' , 'NP3KTRMR.UPDRS3' : 'Kinetic.Tremor.Right.Hand.UPDRS3', 'NP3KTRML.UPDRS3' : 'Kinetic.Tremor.Left.Hand.UPDRS3', 'NP3RTARU.UPDRS3' : 'Rest.Tremor.Amplitude.RUE.UPDRS3', 'NP3RTALU.UPDRS3' : 'Rest.Tremor.Amplitude.LUE.UPDRS3', 'NP3RTARL.UPDRS3' : 'Rest.Tremor.Amplitude.RLE.UPDRS3' ,'NP3RTALL.UPDRS3' : 'Rest.Tremor.Amplitude.LLE.UPDRS3' ,'NP3RTALJ.UPDRS3' : 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS3', 'NP3RTCON.UPDRS3' : 'Constancy.of.Rest.Tremor.UPDRS3', 'NP3SPCH.UPDRS3' : 'Speech.Difficulty.UPDRS3', 'NP3FACXP.UPDRS3' : 'Facial.Expression.Difficulty.UPDRS3' , 'NP3RIGN.UPDRS3' : 'Rigidity.Neck.UPDRS3' , 'NP3RIGRU.UPDRS3' : 'Rigidity.RUE.UPDRS3', 'NP3RIGLU.UPDRS3' : 'Rigidity.LUE.UPDRS3', 'NP3RIGRL.UPDRS3' : 'Rigidity.RLE.UPDRS3', 'NP3RIGLL.UPDRS3' : 'Rigidity.LLE.UPDRS3', 'NP3FTAPR.UPDRS3' : 'Finger.Tapping.Right.Hand.UPDRS3' ,'NP3FTAPL.UPDRS3' : 'Finger.Tapping.Left.Hand.UPDRS3' ,'NP3HMOVR.UPDRS3' : 'Hand.Movements.Right.Hand.UPDRS3', 'NP3HMOVL.UPDRS3' : 'Hand.Movements.Left.Hand.UPDRS3', 'NP3PRSPR.UPDRS3' : 'Pronation.Supination.Right.Hand.UPDRS3', 'NP3PRSPL.UPDRS3' : 'Pronation.Supination.Left.Hand.UPDRS3' , 'NP3TTAPR.UPDRS3' : 'Toe.Tapping.Right.Foot.UPDRS3' , 'NP3TTAPL.UPDRS3' : 'Toe.Tapping.Left.Foot.UPDRS3', 'NP3LGAGR.UPDRS3' : 'Leg.Agility.Right.Leg.UPDRS3', 'NP3LGAGL.UPDRS3' : 'Leg.Agility.Left.Leg.UPDRS3', 'NP3RISNG.UPDRS3' : 'Rising.from.Chair.UPDRS3', 'NP3GAIT.UPDRS3' : 'Gait.Problems.UPDRS3' ,'NP3FRZGT.UPDRS3' : 'Freezing.of.Gait.UPDRS3' ,'NP3PSTBL.UPDRS3' : 'Postural.Stability.Problems.UPDRS3', 'NP3POSTR.UPDRS3' : 'Posture.Problems.UPDRS3' , 'NP3TOT.UPDRS3':'Total.UPDRS3','NP1COG.UPDRS1' : 'Cognitive.Impairment.UPDRS1', 'NP1HALL.UPDRS1' : 'Hallucinations.and.Psychosis.UPDRS1', 'NP1DPRS.UPDRS1' : 'Depressed.Moods.UPDRS1', 'NP1ANXS.UPDRS1' : 'Anxious.Moods.UPDRS1', 'NP1APAT.UPDRS1' : 'Apathy.UPDRS1', 'NP1DDS.UPDRS1' : 'Features.of.Dopamine.Dysregulation.Syndrome.UPDRS1', 'NP1RTOT.UPDRS1' : 'Rater.Completed.Total.UPDRS1','NP1SLPN.UPDRS1' : 'Sleep.Problems.Night.UPDRS1', 'NP1SLPD.UPDRS1' : 'Daytime.Sleepiness.UPDRS1', 'NP1PAIN.UPDRS1' : 'Pain.UPDRS1' , 'NP1URIN.UPDRS1' : 'Urinary.Problems.UPDRS1', 'NP1CNST.UPDRS1' : 'Constipation.Problems.UPDRS1' , 'NP1LTHD.UPDRS1' : 'Lightheadedness.on.Standing.UPDRS1' , 'NP1FATG.UPDRS1' : 'Fatigue.UPDRS1', 'NP1PTOT.UPDRS1' : 'Patient.Completed.Total.UPDRS1','NP2SPCH.UPDRS2' : 'Speech.Difficulty.UPDRS2' , 'NP2SALV.UPDRS2' : 'Saliva.Drooling.UPDRS2' ,'NP2SWAL.UPDRS2': 'Chewing.Swallowing.Difficulty.UPDRS2', 'NP2EAT.UPDRS2' : 'Eating.Difficulty.UPDRS2', 'NP2DRES.UPDRS2' : 'Dressing.Difficulty.UPDRS2', 'NP2HYGN.UPDRS2' : 'Hygiene.Difficulty.UPDRS2' , 'NP2HWRT.UPDRS2' : 'Handwriting.Difficulty.UPDRS2' ,'NP2HOBB.UPDRS2' : 'Hobbies.Difficulty.UPDRS2' ,'NP2TURN.UPDRS2' : 'Turning.in.Bed.Difficulty.UPDRS2', 'NP2TRMR.UPDRS2' : 'Tremor.UPDRS2', 'NP2RISE.UPDRS2' : 'Rising.from.Bed.Difficulty.UPDRS2', 'NP2WALK.UPDRS2' : 'Walking.Difficulty.UPDRS2' ,'NP2FREZ.UPDRS2' : 'Freezing.while.Walking.UPDRS2' , 'NP2PTOT.UPDRS2': 'Total.UPDRS2', 'NP4WDYSK.UPDRS4' : 'Time.Spent.with.Dyskinesias.UPDRS4', 'NP4DYSKI.UPDRS4':'Functional.Impact.of.Dyskinesias.UPDRS4','NP4OFF.UPDRS4' : 'Time.Spent.in.OFF.State.UPDRS4',     'NP4FLCTI.UPDRS4':'Functional.Impact.Fluctuations.UPDRS4',  'NP4FLCTX.UPDRS4':'Complexity.of.Motor.Fluctuations.UPDRS4' ,   'NP4DYSTN.UPDRS4':'Painful.OFF-state.Dystonia.UPDRS4' ,'NP4TOT.UPDRS4': 'Total.UPDRS4','NP4WDYSKDEN.UPDRS4':'Total.Hours.with.Dyskinesias.UPDRS4', 'NP4WDYSKNUM.UPDRS4' :'Total.Hours.Awake.Dysk.UPDRS4', 'NP4WDYSKPCT.UPDRS4' : 'Percent.Dyskinesia.UPDRS4','NP4OFFDEN.UPDRS4':'Total.Hours.OFF.UPDRS4', 'NP4OFFNUM.UPDRS4' : 'Total.Hours.Awake.OFF.UPDRS4','NP4OFFPCT.UPDRS4' : 'Percent.OFF.UPDRS4', 'NP4DYSTNDEN.UPDRS4' :'Total.Hours.OFF.with.Dystonia.UPDRS4',  'NP4DYSTNNUM.UPDRS4':'Total.Hours.OFF.Dyst.UPDRS4', 'NP4DYSTNPCT.UPDRS4':'Percent.OFF.Dystonia.UPDRS4', 'NP3BRADY.UPDRS4' : 'Global.Spontaneity.of.Movement.UPDRS4', 'NP3PTRMR.UPDRS4' : 'Postural.Tremor.Right.Hand.UPDRS4' , 'NP3PTRML.UPDRS4' : 'Postural.Tremor.Left.Hand.UPDRS4' , 'NP3KTRMR.UPDRS4' : 'Kinetic.Tremor.Right.Hand.UPDRS4', 'NP3KTRML.UPDRS4' : 'Kinetic.Tremor.Left.Hand.UPDRS4', 'NP3RTARU.UPDRS4' : 'Rest.Tremor.Amplitude.RUE.UPDRS4', 'NP3RTALU.UPDRS4' : 'Rest.Tremor.Amplitude.LUE.UPDRS4', 'NP3RTARL.UPDRS4' : 'Rest.Tremor.Amplitude.RLE.UPDRS4' ,'NP3RTALL.UPDRS4' : 'Rest.Tremor.Amplitude.LLE.UPDRS4' ,'NP3RTALJ.UPDRS4' : 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS4', 'NP3RTCON.UPDRS4' : 'Constancy.of.Rest.Tremor.UPDRS4'}, inplace = True)
    # updrs_numeric = calculate_subscores(updrs_numeric, 'Brady.Rigidity.Subscore.UPDRS3',    ['Rigidity.Neck.UPDRS3',  'Rigidity.RUE.UPDRS3',  'Rigidity.LUE.UPDRS3',  'Rigidity.RLE.UPDRS3',  'Rigidity.LLE.UPDRS3', 'Finger.Tapping.Right.Hand.UPDRS3' , 'Finger.Tapping.Left.Hand.UPDRS3' , 'Hand.Movements.Right.Hand.UPDRS3','Hand.Movements.Left.Hand.UPDRS3','Pronation.Supination.Right.Hand.UPDRS3', 'Pronation.Supination.Left.Hand.UPDRS3',   'Toe.Tapping.Right.Foot.UPDRS3','Toe.Tapping.Left.Foot.UPDRS3','Leg.Agility.Right.Leg.UPDRS3', 'Leg.Agility.Left.Leg.UPDRS3'])
    # updrs_numeric = calculate_subscores(updrs_numeric, 'Tremor.Subscore.UPDRS3', ['Tremor.UPDRS2', 'Postural.Tremor.Right.Hand.UPDRS3' ,'Postural.Tremor.Left.Hand.UPDRS3' ,'Kinetic.Tremor.Right.Hand.UPDRS3','Kinetic.Tremor.Left.Hand.UPDRS3', 'Rest.Tremor.Amplitude.RUE.UPDRS3','Rest.Tremor.Amplitude.LUE.UPDRS3', 'Rest.Tremor.Amplitude.RLE.UPDRS3' , 'Rest.Tremor.Amplitude.LLE.UPDRS3' , 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS3', 'Constancy.of.Rest.Tremor.UPDRS3'])
    # updrs_numeric = calculate_subscores(updrs_numeric, 'PIGD.Subscore.UPDRS3', ['Walking.Difficulty.UPDRS2' ,  'Freezing.while.Walking.UPDRS2' ,'Gait.Problems.UPDRS3'  , 'Freezing.of.Gait.UPDRS3' , 'Postural.Stability.Problems.UPDRS3'])
    # updrs_numeric = add_extension_to_column_names(updrs_numeric, ['PATNO', 'EVENT_ID', 'PIGD.Subscore.UPDRS3', 'Tremor.Subscore.UPDRS3', 'Brady.Rigidity.Subscore.UPDRS3'], '.Num') # Add a .Num extension to column names w updrs numeric vars


    # ### UPDRS CATEGORICAL ####
    # updrs_cat = decode(updrs_cat, code_list, 'NUPDRS1', ['NP1COG', 'NP1HALL', 'NP1DPRS', 'NP1ANXS', 'NP1APAT', 'NP1DDS'])
    # updrs_cat.rename(columns = {'NP1COG' : 'Cognitive.Impairment.UPDRS1', 'NP1HALL' : 'Hallucinations.and.Psychosis.UPDRS1', 'NP1DPRS' : 'Depressed.Moods.UPDRS1', 'NP1ANXS' : 'Anxious.Moods.UPDRS1', 'NP1APAT' : 'Apathy.UPDRS1', 'NP1DDS' : 'Features.of.Dopamine.Dysregulation.Syndrome.UPDRS1', 'NP1RTOT' : 'Rater.Completed.Total.UPDRS1'}, inplace = True)
    # updrs_cat = decode(updrs_cat, code_list,'NUPDRS1P', ['NP1SLPN', 'NP1SLPD', 'NP1PAIN', 'NP1URIN', 'NP1CNST', 'NP1LTHD', 'NP1FATG'])
    # updrs_cat.rename(columns = {'NP1SLPN' : 'Sleep.Problems.Night.UPDRS1', 'NP1SLPD' : 'Daytime.Sleepiness.UPDRS1', 'NP1PAIN' : 'Pain.UPDRS1' , 'NP1URIN' : 'Urinary.Problems.UPDRS1', 'NP1CNST' : 'Constipation.Problems.UPDRS1' , 'NP1LTHD' : 'Lightheadedness.on.Standing.UPDRS1' , 'NP1FATG' : 'Fatigue.UPDRS1', 'NP1PTOT' : 'Patient.Completed.Total.UPDRS1'}, inplace = True)
    # updrs_cat = decode(updrs_cat, code_list, 'NUPDRS2P', [ 'NP2SPCH','NP2SALV','NP2SWAL','NP2EAT','NP2DRES','NP2HYGN','NP2HWRT','NP2HOBB','NP2TURN','NP2TRMR','NP2RISE','NP2WALK','NP2FREZ'])
    # updrs_cat.rename(columns = {'NP2SPCH' : 'Speech.Difficulty.UPDRS2' , 'NP2SALV' : 'Saliva.Drooling.UPDRS2' ,'NP2SWAL': 'Chewing.Swallowing.Difficulty.UPDRS2', 'NP2EAT' : 'Eating.Difficulty.UPDRS2', 'NP2DRES' : 'Dressing.Difficulty.UPDRS2', 'NP2HYGN' : 'Hygiene.Difficulty.UPDRS2' , 'NP2HWRT' : 'Handwriting.Difficulty.UPDRS2' ,'NP2HOBB' : 'Hobbies.Difficulty.UPDRS2' ,'NP2TURN' : 'Turning.in.Bed.Difficulty.UPDRS2', 'NP2TRMR' : 'Tremor.UPDRS2', 'NP2RISE' : 'Rising.from.Bed.Difficulty.UPDRS2', 'NP2WALK' : 'Walking.Difficulty.UPDRS2' ,'NP2FREZ' : 'Freezing.while.Walking.UPDRS2' , 'NP2PTOT': 'Total.UPDRS2'}, inplace = True)
    # updrs_cat = decode(updrs_cat, code_list, 'NUPDRS3TRT',  ['DBSYN', 'OFFEXAM', 'ONEXAM', 'ONOFFORDER', 'ONNORSN', 'PDMEDYN', 'OFFNORSN','NP3SPCH', 'NP3FACXP', 'NP3RIGN', 'NP3RIGRU', 'NP3RIGLU', 'NP3RIGRL', 'NP3RIGLL', 'NP3FTAPR', 'NP3FTAPL', 'NP3HMOVR', 'NP3HMOVL', 'NP3PRSPR', 'NP3PRSPL', 'NP3TTAPR', 'NP3TTAPL', 'NP3LGAGR', 'NP3LGAGL', 'NP3RISNG', 'NP3GAIT', 'NP3FRZGT', 'NP3PSTBL', 'NP3POSTR', 'NP3BRADY', 'NP3PTRMR', 'NP3PTRML', 'NP3KTRMR', 'NP3KTRML', 'NP3RTARU', 'NP3RTALU', 'NP3RTARL', 'NP3RTALL', 'NP3RTALJ', 'NP3RTCON', 'DBSYN','DYSKPRES','DYSKIRAT','NHY','PDTRTMNT'])
    # updrs_cat.rename(columns = {'PDMEDYN': 'PDMEDYN.UPDRS3',	'DBSYN' : 'DBSYN.UPDRS3',  	'ONOFFORDER' : 'ONOFFORDER.UPDRS3',	'OFFEXAM' : 'OFFEXAM.UPDRS3',	'OFFNORSN':'OFFNORSN.UPDRS3', 'ONEXAM':'ONEXAM.UPDRS3',	'ONNORSN':'ONNORSN.UPDRS3', 'PDMEDDT': 'PDMEDDT.UPDRS3',	'PDMEDTM':'PDMEDTM.UPDRS3',	'EXAMDT': 'EXAMDT.UPDRS3', 'DBS_STATUS' : 'Deep.Brain.Stimulation.Treatment.UPDRS3' , 'NP3SPCH' : 'Speech.Difficulty.UPDRS3', 'NP3FACXP' : 'Facial.Expression.Difficulty.UPDRS3' , 'NP3RIGN' : 'Rigidity.Neck.UPDRS3' , 'NP3RIGRU' : 'Rigidity.RUE.UPDRS3', 'NP3RIGLU' : 'Rigidity.LUE.UPDRS3', 'NP3RIGRL' : 'Rigidity.RLE.UPDRS3', 'NP3RIGLL' : 'Rigidity.LLE.UPDRS3', 'NP3FTAPR' : 'Finger.Tapping.Right.Hand.UPDRS3' ,'NP3FTAPL' : 'Finger.Tapping.Left.Hand.UPDRS3' ,'NP3HMOVR' : 'Hand.Movements.Right.Hand.UPDRS3', 'NP3HMOVL' : 'Hand.Movements.Left.Hand.UPDRS3','NP3PRSPR' : 'Pronation.Supination.Right.Hand.UPDRS3', 'NP3PRSPL' : 'Pronation.Supination.Left.Hand.UPDRS3' , 'NP3TTAPR' : 'Toe.Tapping.Right.Foot.UPDRS3' , 'NP3TTAPL' : 'Toe.Tapping.Left.Foot.UPDRS3', 'NP3LGAGR' : 'Leg.Agility.Right.Leg.UPDRS3', 'NP3LGAGL' : 'Leg.Agility.Left.Leg.UPDRS3', 'NP3RISNG' : 'Rising.from.Chair.UPDRS3', 'NP3GAIT' : 'Gait.Problems.UPDRS3' ,'NP3FRZGT' : 'Freezing.of.Gait.UPDRS3' ,'NP3PSTBL' : 'Postural.Stability.Problems.UPDRS3', 'NP3POSTR' : 'Posture.Problems.UPDRS3' , 'NP3TOT':'Total.UPDRS3',  'Most.Recent.PD.Med.Dose.Date.Time.Before.OFF.Exam' : 'Most.Recent.PD.Med.Dose.Date.Time.Before.OFF.Exam.UPDRS3' ,'ONEXAMTM' : 'ON.Exam.Time.UPDRS3' , 'Most.Recent.PD.Med.Dose.Date.Time.Before.ON.Exam' :'Most.Recent.PD.Med.Dose.Date.Time.Before.ON.Exam.UPDRS3', 'DBSONTM' : 'Time.DBS.Turned.on.before.ON.Exam.UPDRS3', 'DBSOFFTM' : 'Time.DBS.Turned.off.before.OFF.Exam.UPDRS3', 'OFFEXAMTM' : 'OFF.Exam.Time.UPDRS3', 'HRPOSTMED' : 'Hours.btwn.PD.Med.and.UPDRS3.Exam.UPDRS3', 'HRDBSOFF' : 'Hours.btwn.DBS.Device.Off.and.UPDRS3.Exam.UPDRS3', 'HRDBSON' : 'Hours.btwn.DBS.Device.On.and.UPDRS3.Exam.UPDRS3' ,'DYSKPRES' : 'Dyskinesias.Present.UPDRS3', 'DYSKIRAT' : 'Movements.Interefered.with.Ratings.UPDRS3', 'NHY' : 'Hoehn.and.Yahr.Stage.UPDRS3', 'PDTRTMNT' : 'On.PD.Treatment.UPDRS3','NP3BRADY' : 'Global.Spontaneity.of.Movement.UPDRS3', 'NP3PTRMR' : 'Postural.Tremor.Right.Hand.UPDRS3' , 'NP3PTRML' : 'Postural.Tremor.Left.Hand.UPDRS3' , 'NP3KTRMR' : 'Kinetic.Tremor.Right.Hand.UPDRS3', 'NP3KTRML' : 'Kinetic.Tremor.Left.Hand.UPDRS3', 'NP3RTARU' : 'Rest.Tremor.Amplitude.RUE.UPDRS3', 'NP3RTALU' : 'Rest.Tremor.Amplitude.LUE.UPDRS3', 'NP3RTARL' : 'Rest.Tremor.Amplitude.RLE.UPDRS3' ,'NP3RTALL' : 'Rest.Tremor.Amplitude.LLE.UPDRS3' ,'NP3RTALJ' : 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS3', 'NP3RTCON' : 'Constancy.of.Rest.Tremor.UPDRS3', 'PDSTATE' : 'Functional.State.UPDRS3','EXAMTM' : 'Exam.Time.UPDRS3' }, inplace = True)
    # updrs_cat = decode(updrs_cat, code_list, 'NUPDRS4', ['NP4WDYSK','NP4DYSKI','NP4OFF','NP4FLCTI','NP4DYSTN','NP4FLCTX'])
    # updrs_cat.rename(columns = {'NP4WDYSKDEN':'Total.Hours.with.Dyskinesias.UPDRS4', 'NP4WDYSKNUM' :'Total.Hours.Awake.Dysk.UPDRS4', 'NP4WDYSKPCT' : 'Percent.Dyskinesia.UPDRS4','NP4OFFDEN':'Total.Hours.OFF.UPDRS4', 'NP4OFFNUM' : 'Total.Hours.Awake.OFF.UPDRS4','NP4OFFPCT' : 'Percent.OFF.UPDRS4', 'NP4DYSTNDEN' :'Total.Hours.OFF.with.Dystonia.UPDRS4',    'NP4DYSTNNUM':'Total.Hours.OFF.Dyst.UPDRS4', 'NP4DYSTNPCT':'Percent.OFF.Dystonia.UPDRS4', 'NP4WDYSK' : 'Time.Spent.with.Dyskinesias.UPDRS4', 'NP4DYSKI':'Functional.Impact.of.Dyskinesias.UPDRS4','NP4OFF' : 'Time.Spent.in.OFF.State.UPDRS4',     'NP4FLCTI':'Functional.Impact.Fluctuations.UPDRS4',    'NP4FLCTX':'Complexity.of.Motor.Fluctuations.UPDRS4' ,    'NP4DYSTN':'Painful.OFF-state.Dystonia.UPDRS4' ,'NP4TOT': 'Total.UPDRS4','NP4WDYSKDEN' : 'Total.Hours.with.Dyskinesia.UPDRS4', 'NP4WDYSKNUM' : 'Total.Hours.Awake.Dysk.UPDRS4', 'NP4WDYSKPCT' : 'Percent.Dyskinesia.UPDRS4',  'NP4OFFDEN' :'Total.Hours.OFF.UPDRS4' , 'NP4OFFNUM' :'Total.Hours.Awake.OFF.UPDRS4' , 'NP4OFFPCT': 'Percent.OFF.UPDRS4', 'NP4DYSTNDEN' : 'Total.Hours.OFF.with.Dystonia.UPDRS4', 'NP4DYSTNNUM' :'Total.Hours.OFF.Dyst.UPDRS4', 'NP4DYSTNPCT' : 'Percent.OFF.Dystonia.UPDRS4' }, inplace = True)
    # updrs_cat = add_extension_to_column_names(updrs_cat, ['PATNO', 'EVENT_ID','INFODT'], '.Cat') # Add a .Num extension to column names w updrs numeric vars


    # # Create one df with UPDRS scores .Num (numeric) and all UPDRS scores .Cat (categorical)
    # updrs_cat.drop(['INFODT','PATNO','EVENT_ID'], axis = 1, inplace = True)
    # updrs_merged = pd.concat([updrs_cat, updrs_numeric], axis = 1)
    # ppmi_merge = pd.merge(ppmi_merge, updrs_merged, on = ['PATNO', 'EVENT_ID'], how = "outer")


    # # Change names of event ids to be indicative of months
    # ppmi_merge = decode(ppmi_merge, code_list, '_ALL', ['EVENT_ID'])
    # ppmi_merge = fixed_variables(ppmi_merge, ['DOMSIDE', 'Enroll.Diagnosis', 'Enroll.Subtype','Consensus.Diagnosis', 'Consensus.Subtype', 'Subject.Phenoconverted', 'BirthDate', 'Sex', 'Handed', 'Analytic.Cohort','African.Berber.Race','Ashkenazi.Jewish.Race', 'Basque.Race', 'Hispanic.Latino.Race', 'Asian.Race', 'African.American.Race', 'Hawian.Other.Pacific.Islander.Race', 'Indian.Alaska.Native.Race', 'Not.Specified.Race',  'White.Race'])
    # ppmi_merge = ppmi_merge.rename(columns = {'INFODT' : 'Event.ID.Date','Medication' : 'Medication(Dates)' , 'DOMSIDE' : 'Dominant.Side.Disease', 'EVENT_ID' : 'Event.ID', 'PATNO' : 'Subject.ID'})
    
    # #### GENETICS INFO ####
    # lrrk2_genetics_df_formatted = format_genetics_df(genetics_path , 'lrrk2_geno_012_mac5_missing_geno.csv')
    # scna_genetics_df_formatted = format_genetics_df(genetics_path , 'scna_geno_012_mac5_missing_geno.csv')
    # apoe_genetics_df_formatted = format_genetics_df(genetics_path , 'apoe_geno_012_mac5_missing_geno.csv')
    # tmem_genetics_df_formatted = format_genetics_df(genetics_path , 'tmem175_geno_012_mac5_missing_geno.csv')
    # gba_genetics_df_formatted = format_genetics_df(genetics_path , 'gba_geno_012_mac5_missing_geno.csv')
    # genetics_df = merge_multiple_dfs([lrrk2_genetics_df_formatted, scna_genetics_df_formatted, apoe_genetics_df_formatted, tmem_genetics_df_formatted, gba_genetics_df_formatted], on = ["Subject.ID"], how = "outer")
    # genetics_df = change_genetics_int_2_float(genetics_df) # Change genetics col names int to float (remove .0 in all 'CHR.POS' columns)


    # # Merge ppmi_merge with genetics df
    # ppmi_merge = pd.merge(ppmi_merge, genetics_df, on = 'Subject.ID', how = "outer")
    # ppmi_merge = add_snp_recode(genetics_path, ppmi_merge)## Add in Brian's snp_rs6265_recode.csv file sent on slack 6/29/22
    # ppmi_merge = add_t1_mergewide(ppmi_merge, invicro_data)


    # #### DTI INFO ####
    # ppmi_merge = get_full_ImageAcquisitionDate(ppmi_merge)
    # ppmi_merge = merge_dti_results(ppmi_merge, 'ppmi-dti', 'processed/antspymm/antspymm_v0.3.3/PPMI/', 'mean_fa_summary', ['Subject.ID', 'Event.ID.Date'])
    # ppmi_merge = merge_dti_results(ppmi_merge, 'ppmi-dti', 'processed/antspymm/antspymm_v0.3.3/PPMI/', 'mean_md_summary', ['Subject.ID','Event.ID.Date', 'DTI.antspymm.Image.ID'])
    # ppmi_merge.to_csv('/Users/areardon/Desktop/ppmi_merge_after_mergedti.csv')
    
    ## TEMP START 
    ppmi_merge = pd.read_csv("/Users/areardon/Desktop/ppmi_merge_after_mergedti.csv")
    ## TEMP END
    
    
    ## Add in 'Analytic.Cohort' column
    analytic_cohort_subids = full_df['PATNO'].unique().tolist() # subids for analytic cohort
    ppmi_merge = add_analytic_cohort(ppmi_merge, analytic_cohort_subids)

    ## Get Enrollment Diagnosis for subjects in Not Analytic Cohort - do this using the participants_status.csv
    participant_status = read_csv_drop_cols(ppmi_download_path, 'Participant_Status_23May2023.csv',['PATNO', 'COHORT_DEFINITION'], drop = False )
    participant_status.rename(columns = {'PATNO' : 'Subject.ID', 'COHORT_DEFINITION' : 'Enroll.Diagnosis'}, inplace = True)
    ppmi_merge = get_enrollment_dx_nonanalytic(ppmi_merge, participant_status) 
    ppmi_merge = fix_event_id_date(ppmi_merge)


    #### Add in ppmi_qc_BA.csv - Brian sent on slack 1/31/22 ###
    ppmi_merge = add_BA_qc(invicro_data, ppmi_merge)

    ## Make any dominant side of disease that are NA into 'Symmetric' FIXME CHECK
    domsideisna = ppmi_merge['Dominant.Side.Disease'].isna()
    ppmi_merge['Dominant.Side.Disease'].loc[domsideisna] = 'Symmetric'
    ppmi_merge = add_lateralized_subscores(ppmi_merge,  ['Dominant.Side.Disease', 'Rigidity.Neck.UPDRS3.Num', 'Rigidity.LUE.UPDRS3.Num', 'Rigidity.LLE.UPDRS3.Num', 'Finger.Tapping.Left.Hand.UPDRS3.Num', 'Hand.Movements.Left.Hand.UPDRS3.Num', 'Pronation.Supination.Left.Hand.UPDRS3.Num', 'Toe.Tapping.Left.Foot.UPDRS3.Num', 'Leg.Agility.Left.Leg.UPDRS3.Num'], 'Left', 'Brady.Rigidity.Subscore-left.UPDRS3')
    ppmi_merge = add_lateralized_subscores(ppmi_merge, ['Dominant.Side.Disease', 'Rigidity.Neck.UPDRS3.Num', 'Rigidity.RUE.UPDRS3.Num', 'Rigidity.RLE.UPDRS3.Num', 'Finger.Tapping.Right.Hand.UPDRS3.Num', 'Hand.Movements.Right.Hand.UPDRS3.Num', 'Pronation.Supination.Right.Hand.UPDRS3.Num', 'Toe.Tapping.Right.Foot.UPDRS3.Num', 'Leg.Agility.Right.Leg.UPDRS3.Num'], 'Right', 'Brady.Rigidity.Subscore-right.UPDRS3')
    ppmi_merge = add_symmetric_subscores(ppmi_merge, ['Dominant.Side.Disease', 'Rigidity.Neck.UPDRS3.Num', 'Rigidity.RUE.UPDRS3.Num', 'Rigidity.LUE.UPDRS3.Num', 'Rigidity.RLE.UPDRS3.Num', 'Rigidity.LLE.UPDRS3.Num', 'Finger.Tapping.Right.Hand.UPDRS3.Num', 'Finger.Tapping.Left.Hand.UPDRS3.Num', 'Hand.Movements.Right.Hand.UPDRS3.Num', 'Hand.Movements.Left.Hand.UPDRS3.Num', 'Pronation.Supination.Right.Hand.UPDRS3.Num', 'Pronation.Supination.Left.Hand.UPDRS3.Num', 'Toe.Tapping.Right.Foot.UPDRS3.Num', 'Toe.Tapping.Left.Foot.UPDRS3.Num', 'Leg.Agility.Right.Leg.UPDRS3.Num', 'Leg.Agility.Left.Leg.UPDRS3.Num'], 'Symmetric', 'Brady.Rigidity.Subscore-sym.UPDRS3', '.UPDRS3.Num')
    ppmi_merge = combine_lateralized_subscores(ppmi_merge, "Brady.Rigidity.Subscore.lateralized.UPDRS3", "Brady.Rigidity.Subscore-right.UPDRS3", "Brady.Rigidity.Subscore-left.UPDRS3", "Brady.Rigidity.Subscore-sym.UPDRS3") # Combine left and right and sym subscores into same column


    #### TREMOR ####
    ppmi_merge = add_lateralized_subscores(ppmi_merge,  ['Dominant.Side.Disease', 'Tremor.UPDRS2.Num', 'Postural.Tremor.Left.Hand.UPDRS3.Num', 'Kinetic.Tremor.Left.Hand.UPDRS3.Num', 'Rest.Tremor.Amplitude.LUE.UPDRS3.Num', 'Rest.Tremor.Amplitude.LLE.UPDRS3.Num', 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS3.Num', 'Constancy.of.Rest.Tremor.UPDRS3.Num'], 'Left', 'Tremor.Subscore-left.UPDRS3')
    ppmi_merge = add_lateralized_subscores(ppmi_merge,  ['Dominant.Side.Disease', 'Tremor.UPDRS2.Num', 'Postural.Tremor.Right.Hand.UPDRS3.Num', 'Kinetic.Tremor.Right.Hand.UPDRS3.Num', 'Rest.Tremor.Amplitude.RUE.UPDRS3.Num', 'Rest.Tremor.Amplitude.RLE.UPDRS3.Num', 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS3.Num', 'Constancy.of.Rest.Tremor.UPDRS3.Num'], 'Right', 'Tremor.Subscore-right.UPDRS3')
    ppmi_merge = add_symmetric_subscores(ppmi_merge, ['Dominant.Side.Disease', 'Tremor.UPDRS2.Num', 'Postural.Tremor.Right.Hand.UPDRS3.Num', 'Postural.Tremor.Left.Hand.UPDRS3.Num', 'Kinetic.Tremor.Right.Hand.UPDRS3.Num', 'Kinetic.Tremor.Left.Hand.UPDRS3.Num', 'Rest.Tremor.Amplitude.RUE.UPDRS3.Num', 'Rest.Tremor.Amplitude.LUE.UPDRS3.Num', 'Rest.Tremor.Amplitude.RLE.UPDRS3.Num', 'Rest.Tremor.Amplitude.LLE.UPDRS3.Num', 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS3.Num', 'Constancy.of.Rest.Tremor.UPDRS3.Num'], 'Symmetric', 'Tremor.Subscore-sym.UPDRS3', '.UPDRS3.Num')
    ppmi_merge = combine_lateralized_subscores(ppmi_merge, "Tremor.Subscore.lateralized.UPDRS3", "Tremor.Subscore-right.UPDRS3", "Tremor.Subscore-left.UPDRS3", "Tremor.Subscore-sym.UPDRS3")# Combine left and right and sym scores into same column (.lateralized)
    ppmi_merge = fill_non_lateralized_subscore(ppmi_merge, 'Tremor.Subscore.lateralized.UPDRS3', 'Tremor.Subscore.UPDRS3')
    ppmi_merge = fill_non_lateralized_subscore(ppmi_merge, 'Brady.Rigidity.Subscore.lateralized.UPDRS3', 'Brady.Rigidity.Subscore.UPDRS3')



    ## temp start
    # Final re-organization of ppmi_merge and save
    ppmi_merge['Subject.ID'] = ppmi_merge['Subject.ID'].astype(int)
    ppmi_merge.set_index('Subject.ID', inplace = True)
    ppmi_merge.fillna('NA', inplace = True)
    ppmi_merge = remove_cols_that_startwith(ppmi_merge, ['Unnamed']) 
    ppmi_merge.to_csv(userdir + 'ppmi_merge_v' + version + '.csv')
    ## temp end 


    ## Add some other things
    ppmi_merge = add_bestEventID_resnet(ppmi_merge)
    ppmi_merge = add_bestImageAcquisitionDate(ppmi_merge)
    ppmi_merge = add_DXsimplified(ppmi_merge)
    ppmi_merge = add_min_PD_duration(ppmi_merge)
    ppmi_merge = add_Visit(ppmi_merge)


    # Final re-organization of ppmi_merge and save
    ppmi_merge['Subject.ID'] = ppmi_merge['Subject.ID'].astype(int)
    ppmi_merge.set_index('Subject.ID', inplace = True)
    ppmi_merge.fillna('NA', inplace = True)
    ppmi_merge = remove_cols_that_startwith(ppmi_merge, ['Unnamed']) 
    ppmi_merge.to_csv(userdir + 'ppmi_merge_v' + version + '.csv')
    
    
    

def fix_event_id_date(ppmi_merge) : 
    # Change Event.ID.Date to date time and corrected format
    ppmi_merge['Event.ID.Date'] = ppmi_merge['Event.ID.Date'].astype(str)
    ppmi_merge['Event.ID.Date'] = pd.to_datetime(ppmi_merge['Event.ID.Date'], errors = "ignore") # Change event.ID.Date column to date time so we can sort according to this
    ppmi_merge = ppmi_merge.sort_values(by = ['Subject.ID','Event.ID.Date']) # Sort values by subject and event id date
    ppmi_merge['Event.ID.Date'] = ppmi_merge['Event.ID.Date'].astype(str) # Change Event.ID.Date back to string so we can reformat
    
    ## HERE - lose 3101
    # Reformat Event.ID.Date from pd.to_datetime to month/year
    for row_num in range(len(ppmi_merge['Event.ID.Date'])):
        if ppmi_merge['Event.ID.Date'].iloc[row_num] != 'NaT':
            split = ppmi_merge['Event.ID.Date'].iloc[row_num].split('-')
            new_date = split[1] +'/' + split[0] # month/year format
            ppmi_merge['Event.ID.Date'].iloc[row_num] = new_date

    ppmi_merge['Event.ID.Date'] = ppmi_merge['Event.ID.Date'].replace('NaT','NA')
    return ppmi_merge

    

def decode(ppmi_merge, code_list, MOD_NAME, cols_to_decode) : 
    for col in cols_to_decode : 
        new_code_list = code_list[code_list['MOD_NAME'] == MOD_NAME]
        new_code_list = new_code_list[new_code_list['ITM_NAME'] == col]
        decoding_dict = dict(zip(new_code_list['CODE'], new_code_list['DECODE']))
        try : 
            decoding_dict_float = {float(k): v for k, v in decoding_dict.items()}
        except : 
            decoding_dict_float = decoding_dict
        ppmi_merge[col] = ppmi_merge[col].map(decoding_dict_float)
    return ppmi_merge




def read_csv_drop_cols(filepath, csv_filename : str, list_cols : List, drop : bool) :
    if drop == False :
        df = pd.read_csv(filepath + csv_filename, skipinitialspace = True)  ## Read in csv
        df = df[list_cols] # keep columns in list_cols
    else :
        df = pd.read_csv(filepath + csv_filename, skipinitialspace = True)  ## Read in csv
        df.drop(list_cols, axis = 1, inplace = True) # drop columns in list_cols
    return df



def add_BA_qc(invicro_data, ppmi_merge) : 
    ppmi_qc_BA = pd.read_csv(invicro_data + 'ppmi_qc_BA.csv')
    ppmi_qc_BA = ppmi_qc_BA.reset_index(drop = False) # Move index to first column so we can rename
    ppmi_qc_BA.rename(columns = {'ID' : 'ImageID'}, inplace = True) # Rename ImageID
    
    # Update ImageID column bc info from T1 file (where ImageID was created from) does not contain all the files from s3 (need this to merge in subs from QC csv)
    for row_num in range(len(ppmi_merge['ImageID'])) :
        if isinstance(ppmi_merge['T1.s3.Image.Name'].iloc[row_num], str):
            imageID = ppmi_merge['T1.s3.Image.Name'].iloc[row_num].split('.')[0] # take info before .nii.gz
            ppmi_merge['ImageID'].iloc[row_num] = imageID.split('-')[1] + '-' + imageID.split('-')[2] + '-' + imageID.split('-')[4]
            
    #ppmi_qc_BA['ImageID'] = ppmi_qc_BA['ImageID'].astype(float)
    ppmi_merge = pd.merge(ppmi_merge, ppmi_qc_BA, on = ['ImageID'], how = "left") # Merge - keep only from ImageIDs we already have
    return ppmi_merge




def merge_csv(filepath : str, df : pd.DataFrame, csv_filename : str, list_cols : List, merge_on : str, merge_how : str) :
    demo_df = read_csv_drop_cols(filepath, csv_filename, list_cols, drop = False) # Read in csv and keep only cols in list_cols
    
    if csv_filename == 'Socio-Economics_23May2023.csv' :
        demo_df = get_education_mean(demo_df) # Take the mean of education years if there are 2 different number of years for one subject
    
    demo_df['PATNO'] = demo_df['PATNO'].astype(float)
    ppmi_merge = pd.merge(df, demo_df, on = merge_on, how = merge_how) # Merge
    return ppmi_merge



def get_education_mean(df) :
    df = df.groupby('PATNO').mean().reset_index()
    return df 



def remove_cols_that_startwith(df: pd.DataFrame, list : List) :
    df = df.loc[:, ~df.columns.str.startswith(tuple(list))] # Remove columns that begin with CON and ENRL
    return df



def create_empty_col(df : pd.DataFrame, list : List) :
    for item in list :
        df[item] = ''
    return df
        


def create_cohort_df(xlsx : pd.ExcelFile) :
    df = pd.DataFrame()
    sheets = ['PD', 'Prodromal', 'HC', 'SWEDD']
    for sheet in sheets : 
        cohort_df = pd.read_excel(xlsx, sheet) # Read in
        cohort_df = remove_cols_that_startwith(cohort_df, ['Unnamed', 'CONDATE'])
        cohort_df = create_empty_col(cohort_df, ['Enrollment.Subtype', 'Consensus.Subtype'])
        if sheet == 'HC' :
            cohort_df['Subgroup'] = 'Healthy Control'
        if sheet == 'SWEDD' :
            cohort_df['Comments'] = '' # Replace comments with empty string because we don't want to merge comments for SWEDD sheet
        cohort_df = fill_subtype(cohort_df)
        df = df.append([cohort_df]) # Concat all 4 cohort dfs
    
    ## Rename columns
    df['CONPD'].replace({1 : 'Parkinson\'s Disease', 0 : ''}, inplace = True)
    df['CONPROD'].replace({1 : 'Prodromal',  0 : ''}, inplace = True)
    df['CONHC'].replace({1 : 'Healthy Control',  0 : ''}, inplace = True)
    df['CONSWEDD'].replace({1 : 'SWEDD',  0 : 'SWEDD/PD'}, inplace = True)
    df['Comments'].replace({'MSA' : 'Multiple System Atrophy'}, inplace = True)
    
    df = merge_columns(df, ['CONPD', 'CONPROD', 'CONHC', 'CONSWEDD','Comments'], 'Consensus.Diagnosis', ': ') # Get one column for Consensus Diagnosis with comments merged in
    df = merge_columns(df, ['Subgroup', 'Enrollment.Subtype'], 'Enroll.Subtype', '') # Get one column for Enroll.Subtype
    df = remove_cols_that_startwith(df, ['CON','ENRL'])
    
    return df


    

def merge_columns(df : pd.DataFrame , old_df_columns : list, new_df_column_name : str, separator = str) :
    """
    Takes entries in each of old_df_columns and joins them together with a sepator of choice.  Removes
    empty/nan column entries.
    """
    df = df.replace(r'^\s*$', np.NaN, regex=True) # Fill in empty cells with nan
    df[new_df_column_name] = df[old_df_columns].agg(lambda x: x.dropna().str.cat(sep= separator), axis=1) # Combine columns
    df.drop(old_df_columns, axis = 1, inplace = True)
    return df



def isNaN(num):
    return num != num



def condensed_df(df : pd.DataFrame, keep_col_list : List, rename_col_dict: dict, drop_col_list : List) :
    new_df = df[keep_col_list]
    new_df.rename(columns = rename_col_dict, inplace = True)
    new_df.dropna(subset = drop_col_list, inplace = True)
    return new_df



def merge_dti_results(ppmi_merge, bucket, prefix, search_string, merge_on) :
    ## Merge in FA and MD results
    print(f"Merge in {search_string}")
    dti = search_s3(bucket, prefix, search_string)
    client = boto3.client('s3', region_name="us-east-1")
    appended_data = []
    for key in dti :
        subid = np.int64(key.split('/')[4])
        date = key.split('/') [5]
        month_date = date[4:6] + '/' + date[0:4]
        image_id = key.split('/')[7]
        csv_obj = client.get_object(Bucket=bucket, Key = key)
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_string))
        df.drop(['u_hier_id','u_hier_id.1'], axis = 1, inplace = True)
        df['Subject.ID'] = subid
        df['Event.ID.Date'] = month_date
        df['DTI.antspymm.Image.ID'] = image_id
        if 'md' in search_string : # FIXME- if you fix md labels you can get rid of this
            df.columns = df.columns.str.replace("fa", "md") # FIXME - if you fix md labels you can get rid of this
        appended_data.append(df)
    appended_data_dti = pd.concat(appended_data)
    ppmi_merge = pd.merge(ppmi_merge, appended_data_dti, on = merge_on, how = "outer")
    return ppmi_merge



def fill_subtype(df : pd.DataFrame) :
    if df['Cohort'][0] == 'Parkinson\'s Disease' :
        # Decode Enrollment.Subtype ('Summary' sheet) and Consensus.Subtype ('Summary Analytic' sheet) of 'Consensus_Committee_Analytic_Datasets_28OCT21.xlsx'
        df.loc[(df['ENRLPD'] == 1) & (df['ENRLLRRK2'] == 0) & (df['ENRLGBA'] == 0) & (df['ENRLSNCA'] == 0), 'Enrollment.Subtype'] = '' # Sporadic - don't need to define here bc already covered in 'Subgroup' column in PD sheet
        df.loc[(df['ENRLPD' ]== 1) & (df['ENRLLRRK2'] == 1), 'Enrollment.Subtype'] =  ' : LRRK2'
        df.loc[(df['ENRLPD'] == 1) & (df['ENRLGBA'] == 1), 'Enrollment.Subtype'] = ' : GBA'
        df.loc[(df['ENRLPD'] == 1) & (df['ENRLSNCA'] == 1), 'Enrollment.Subtype'] =  ' : SNCA'
        df.loc[(df['CONPD'] == 1) & (df['CONLRRK2'] == 0) | (df['CONLRRK2'] == '.') & (df['CONGBA'] == 0) | (df['CONGBA'] == '.') & (df['CONSNCA'] == 0) | (df['CONSNCA'] == '.') , 'Consensus.Subtype'] = 'Sporadic'
        df.loc[(df['CONPD'] == 1) & (df['CONLRRK2']== 1) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 0), 'Consensus.Subtype'] = 'Genetic : LRRK2'
        df.loc[(df['CONPD'] == 1) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 1) & (df['CONSNCA'] == 0) , 'Consensus.Subtype'] = 'Genetic : GBA'
        df.loc[(df['CONPD'] == 1) & (df['CONLRRK2'] == 1) & (df['CONGBA'] == 1) & (df['CONSNCA'] == 0), 'Consensus.Subtype'] = 'Genetic : LRRK2 + GBA'
        df.loc[(df['CONPD'] == 1) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 1) , 'Consensus.Subtype'] = 'Genetic : SNCA'
        df.loc[(df['CONPD'] == 0) & (df['CONPROD']== 0) , 'Consensus.Subtype'] = 'non-PD' # FIXME
        df.loc[(df['CONPD'] == 0) & (df['CONPROD']== 1) & (df['CONLRRK2'] == 1) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 0), 'Consensus.Subtype'] = 'Genetic : LRRK2 Prodromal'
        df.loc[(df['CONPD'] == 0) & (df['CONPROD'] == 1) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 1) & (df['CONSNCA'] == 0) , 'Consensus.Subtype'] = 'Genetic : GBA Prodromal'
    
    elif df['Cohort'][0] == 'Prodromal' :
        # Decode Enrollment.Subtype and Consensus.Subtype to be categorical variables for prodromal df
        df.loc[(df['ENRLPROD'] == 1) & (df['ENRLLRRK2'] == 1), 'Enrollment.Subtype'] = ' : LRRK2 Prodromal'
        df.loc[(df['ENRLPROD'] == 1) & (df['ENRLGBA'] == 1), 'Enrollment.Subtype'] =  ' : GBA Prodromal'
        df.loc[(df['ENRLPROD'] == 1) & (df['ENRLSNCA'] == 1), 'Enrollment.Subtype'] = ' : SNCA Prodromal'
        df.loc[(df['ENRLPROD'] == 1) & (df['ENRLHPSM'] == 1) ,'Enrollment.Subtype'] = '' # Hyposmia already covered in 'Subgroup' column
        df.loc[(df['ENRLPROD'] == 1) & (df['ENRLRBD'] == 1), 'Enrollment.Subtype'] = '' # RBD already covered in 'Subgroup' column
        df.loc[(df['CONPROD'] == 1) & (df['PHENOCNV'] == 0) & (df['CONLRRK2'] == 1) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 0) ,'Consensus.Subtype'] = 'Genetic : LRRK2 Prodromal'
        df.loc[(df['CONPROD'] == 1) & (df['PHENOCNV'] == 1) & (df['CONLRRK2'] == 1) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 0), 'Consensus.Subtype'] = 'Genetic : LRRK2 Phenoconverted'
        df.loc[(df['CONPROD'] == 0) & (df['CONLRRK2'] == 1) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 0), 'Consensus.Subtype' ] = 'Genetic : LRRK2 not Prodromal'
        df.loc[(df['CONPROD'] == 1) & (df['PHENOCNV'] == 0) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 1) & (df['CONSNCA'] == 0), 'Consensus.Subtype'] = 'Genetic : GBA Prodromal'
        df.loc[(df['CONPROD'] == 1) & (df['PHENOCNV'] == 1) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 1) & (df['CONSNCA'] == 0) & (df['CONRBD'] == 0), 'Consensus.Subtype'] = 'Genetic : GBA Phenoconverted'
        df.loc[(df['CONPROD'] == 0) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 1) & (df['CONSNCA'] == 0) , 'Consensus.Subtype' ] = 'Genetic : GBA not Prodromal'
        df.loc[(df['CONPROD'] == 1) & (df['PHENOCNV'] == 0) & (df['CONLRRK2'] == 1) & (df['CONGBA'] == 1) & (df['CONSNCA'] == 0) , 'Consensus.Subtype'] = 'Genetic : LRRK2 + GBA Prodromal'
        df.loc[(df['CONPROD'] == 1) & (df['PHENOCNV'] == 1) & (df['CONLRRK2'] == 1) & (df['CONGBA'] == 1) & (df['CONSNCA'] == 0) ,'Consensus.Subtype'] = 'Genetic : LRRK2 + GBA Phenoconverted'
        df.loc[(df['CONPROD'] == 0) & (df['CONLRRK2'] == 1) & (df['CONGBA'] == 1) & (df['CONSNCA'] == 0) , 'Consensus.Subtype' ] = 'Genetic : LRRK2 + GBA not Prodromal'
        df.loc[(df['CONPROD'] == 1) & (df['PHENOCNV'] == 0) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 1), 'Consensus.Subtype'] = 'Genetic : SNCA Prodromal'
        df.loc[(df['CONPROD'] == 1) & (df['PHENOCNV'] == 1) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 1), 'Consensus.Subtype'] = 'Genetic : SNCA Phenoconverted'
        df.loc[(df['CONPROD'] == 0) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 1) , 'Consensus.Subtype' ] = 'Genetic : SNCA not Prodromal'
        df.loc[(df['CONPROD'] == 0) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 0) & (df['CONHPSM'] == 0) & (df['CONRBD'] == '.'), 'Consensus.Subtype' ] = 'No Mutation not Prodromal'
        df.loc[(df['CONPROD'] == 1) & (df['PHENOCNV'] == 0) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 0) & (df['CONHPSM'] == 1) & (df['CONRBD'] == '.'), 'Consensus.Subtype'] = 'Hyposmia'
        df.loc[(df['CONPROD'] == 1) & (df['PHENOCNV'] == 1) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 0) & (df['CONHPSM'] == 1) & (df['CONRBD'] == '.'), 'Consensus.Subtype' ] = 'Hyposmia : Phenoconverted'
        df.loc[(df['CONPROD'] == 0) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 0) & (df['CONHPSM'] == 1) & (df['CONRBD'] == '.'), 'Consensus.Subtype' ] =  'Hyposmia : not Prodromal'
        df.loc[(df['CONPROD'] == 1) & (df['CONRBD'] == 1) & (df['PHENOCNV'] == 0) , 'Consensus.Subtype'] = 'RBD'
        df.loc[(df['CONPROD'] == 1) & (df['CONRBD'] == 1) & (df['PHENOCNV'] == 1) & (df['CONGBA'] == 0), 'Consensus.Subtype'] = 'RBD : Phenoconverted'
        df.loc[(df['CONPROD'] == 1) & (df['CONRBD'] == 1) & (df['PHENOCNV'] == 1) & (df['CONGBA'] == 1), 'Consensus.Subtype' ] = 'RBD : Phenoconverted with GBA'

    elif df['Cohort'][0] == 'Healthy Control' :
        # Decode Enrollment.Subtype and Consensus.Subtype to be categorical variables for Healthy Control df
        df.loc[(df['ENRLHC'] == 1), 'Enrollment.Subtype'] = '' # Healthy Control already covered in Subgroup column
        df.loc[(df['CONHC'] == 1) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 0), 'Consensus.Subtype'] = 'Healthy Control'
        df.loc[(df['CONHC'] == 1) & (df['CONLRRK2'] == 1) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 0),'Consensus.Subtype'] = 'LRRK2'
        df.loc[(df['CONHC'] == 1) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 1) & (df['CONSNCA'] == 0), 'Consensus.Subtype'] = 'GBA'
        df.loc[(df['CONHC'] == 1) & (df['CONLRRK2'] == 1) & (df['CONGBA'] == 1) & (df['CONSNCA'] == 0) ,'Consensus.Subtype'] = 'LRRK + GBA'
        df.loc[(df['CONHC'] == 1) & (df['CONLRRK2'] == 0) & (df['CONGBA'] == 0) & (df['CONSNCA'] == 1), 'Consensus.Subtype'] = 'SNCA'
        df.loc[(df['CONHC'] == 0), 'Consensus.Subtype'] = 'non-HC'  # FIXME

    elif df['Cohort'][0] == 'SWEDD' :
        # Decode Enrollment.Subtype and Consensus.Subtype to be categorical variables for swedd df
        df.loc[df['ENRLSWEDD'] == 1 , 'Enrollment.Subtype'] =  'SWEDD Legacy'
        df.loc[df['CONSWEDD'] == 0 , 'Consensus.Subtype'] = 'SWEDD/PD Active'
        df.loc[df['CONSWEDD'] == 1 ,'Consensus.Subtype'] =  'SWEDD/non-PD Active'
    return df




# def add_PD_Disease_Duration(df : pd.DataFrame, col_name : str)  :
#     df[col_name] = '' # Initialize PD.Diagnosis.Duration variable
#     for row_num in range(len(df['PD.Diagnosis.Date'])) :
#         if isinstance(df['PD.Diagnosis.Date'].loc[row_num], str) and isinstance(df['INFODT'].loc[row_num], str): # If we have both a PD Diagnosis date and an event id date
#             diag_year = int(df['PD.Diagnosis.Date'].loc[row_num].split('/')[1]) # Diagnosis year
#             diag_month = int(df['PD.Diagnosis.Date'].loc[row_num].split('/')[0]) # Diagnosis month
#             event_year = int(df['INFODT'].loc[row_num].split('/')[1]) # Visit date year
#             event_month = int(df['INFODT'].loc[row_num].split('/')[0]) # Visit date month
#             diff = relativedelta.relativedelta(datetime(event_year, event_month, 1), datetime(diag_year, diag_month, 1)) # FIXME ASSUMPTION visit date and diagnosis date was the first of the month
#             df[col_name].iloc[row_num] = ((diff.years)*12 + diff.months)/12 # PD.Diagnosis.Duration in years
#     return df




def add_PD_Disease_Duration(df: pd.DataFrame, col_name: str):
    mask = df['PD.Diagnosis.Date'].notna() & df['INFODT'].notna()  # Mask to filter rows with non-null values

    diag_dates = pd.to_datetime(df.loc[mask, 'PD.Diagnosis.Date'], format='%m/%Y')  # Convert PD.Diagnosis.Date to datetime format
    event_dates = pd.to_datetime(df.loc[mask, 'INFODT'], format='%m/%Y')  # Convert INFODT to datetime format

    diffs = event_dates - diag_dates  # Calculate the differences between event and diagnosis dates
    durations = (diffs.dt.years * 12 + diffs.dt.months) / 12  # Convert the differences to duration in years

    df.loc[mask, col_name] = durations  # Assign the calculated durations to the corresponding rows

    return df

    

def add_concomitant_med_log(ppmi_merge : pd.DataFrame, ppmi_download_path : str) :
    ## Medication status - OLD WAY START Concomitant Med Log # FIXME not a useful way to show medication status
    med_df = pd.read_csv(ppmi_download_path + 'Concomitant_Medication_Log_23May2023.csv', skipinitialspace=True) # Medication history
    med_df.replace({';' : ','}, regex = True, inplace = True) # Replace ';' with ',' in med_df
    # FIXME - do we want to get rid of certain supplements we aren't interested in?  Or leave all?
    med_df['CMTRT'] = med_df['CMTRT'].str.title() # Capitalize all medication names
    med_df['CMTRT'] = med_df['CMTRT'].str.strip()
    n = 20 # FIXME how many of these to keep
    selection = med_df['CMTRT'].value_counts()[:n].index.tolist()
    med_df = med_df.loc[med_df['CMTRT'].isin(selection)]
    med_df['CMTRT'] = med_df['CMTRT'].str.title() # Capitalize all medication names
    med_df['STARTDT'].fillna('NA', inplace = True) # Fillna
    med_df['STOPDT'].fillna('NA', inplace = True) # Fillna
    med_df = med_df.astype({"STARTDT" : 'str', "STOPDT" :'str'}) # Change start and stop date to strings
    med_df = merge_columns(med_df, ['STARTDT', 'STOPDT'], 'Start_Stop', '-') # Merge columns Start and stop date together
    med_df['Start_Stop'] = '(' + med_df['Start_Stop'].astype(str) + ')'# Put parenthesis around dates so when you merge it with LED_med_and dose it is more organized
    med_df = merge_columns(med_df, ['CMTRT', 'Start_Stop'], 'Medication', ' ')
    med_df = med_df.groupby(['PATNO','EVENT_ID'])['Medication'].apply('; '.join)
    ppmi_merge = pd.merge(ppmi_merge, med_df, on = ['PATNO', 'EVENT_ID'], how = "outer") # Merge med_df in
    ppmi_merge = ppmi_merge.sort_values(by = ['PATNO','Age']).reset_index(drop = True) # Sort values by subject and age (similar to event id bc age in order of event id)
    return ppmi_merge



def search_s3(bucket : str, prefix : str, search_string : str):
    client = boto3.client('s3', region_name="us-east-1")
    paginator = client.get_paginator('list_objects')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
    keys = []
    for page in pages:
        contents = page['Contents']
        for c in contents:
            keys.append(c['Key'])
    if search_string:
        keys = [key for key in keys if search_string in key]
    return keys



def keep_only_numeric_variables_updrs(updrs_numeric: pd.DataFrame):
    conditions = ['NP', 'PATNO', 'EVENT', 'NHY'] # Define the conditions for selecting numeric variables
    numeric_vars = [col_name for col_name in updrs_numeric.columns if col_name.startswith(tuple(conditions))] # Use list comprehension to filter columns based on the conditions
    updrs_numeric = updrs_numeric[numeric_vars] # Select only the numeric variables
    
    return updrs_numeric



def get_enrollment_dx_nonanalytic(ppmi_merge, participant_status) : 
    analytic = ppmi_merge[ppmi_merge['Analytic.Cohort'] == 'Analytic Cohort'] # Split up Analytic cohort df and not Analytic Cohort df
    not_analytic = ppmi_merge[ppmi_merge['Analytic.Cohort'] == 'Not Analytic Cohort'] # Split up Analytic cohort df and not Analytic Cohort df
    
    not_analytic_participant_status = pd.merge(not_analytic, participant_status, on = ['Subject.ID'], how = "left") # Merge not Atlantic subids with enrollment diagnosis in participant_status
    not_analytic_participant_status.drop(['Enroll.Diagnosis_x'], axis = 1, inplace = True) # Remove the extra Enroll.Diagnosis created at merge
    not_analytic_participant_status.rename(columns = {'Enroll.Diagnosis_y' : 'Enroll.Diagnosis'}, inplace = True)
    not_analytic_participant_status.loc[not_analytic_participant_status['Enroll.Diagnosis'] == 'Healthy Control', 'Enroll.Subtype'] = 'Healthy Control' # For Healthy Control subjects in the Not Analytic Cohort - make 'Enroll.Subtype' = Healthy Control

    # Merge df of Not Analytic and Analytic subjects and sort by SubID and Event.ID.Date
    ppmi_merge = pd.concat([analytic, not_analytic_participant_status])
    return ppmi_merge

    

def func(row):
    ## If in LD column there is a (i.e. 150 + LD) * 0.33) - create a new duplicate column with just 150 variable - bc this LEDD needs to be added to full LEDD and these formulas are therefore not correct?  # per Pavan notes issues
    if '(' in str(row['LEDD']):
        row2 = row.copy()
        temp = row2['LEDD']
        row2['LEDD'] = re.search('\(([0-9]+)', temp).group(1)
        return pd.concat([row, row2], axis=1)
    return row


def add_LEDD(ppmi_merge, ppmi_download_path) :
    ## LEDD Medication Status - FIXME Assumtion : If stop date is NA we assume LEDD only occurred in that month
    LEDD_med_df = read_csv_drop_cols(ppmi_download_path, 'LEDD_Concomitant_Medication_Log_23May2023.csv', ['PATNO', 'LEDD', 'STARTDT', 'STOPDT'], drop = False)
    ppmi_merge['INFODT'] = pd.to_datetime(ppmi_merge['INFODT'], format = '%m%Y', errors = 'ignore') # change to INFODT to type datetime so we can sort according to date
    LEDD_med_df['STARTDT'] = pd.to_datetime(LEDD_med_df['STARTDT'], format = '%m%Y', errors = 'ignore') # change to STARTDT to type datetime so we can sort according to date
    LEDD_med_df['STOPDT'] = pd.to_datetime(LEDD_med_df['STOPDT'], format = '%m%Y', errors = 'ignore') # change to STOPDT to type datetime so we can sort according to date
    LEDD_med_df['STOPDT2'] = LEDD_med_df['STOPDT'] # Initialize second stop date variable
    LEDD_med_df['STOPDT2'].fillna(LEDD_med_df['STARTDT'], inplace = True) # Fill in NaN stop dates with start dates # ASSUMPTION START and STOP on same month
    LEDD_med_df = LEDD_med_df.merge(LEDD_med_df.apply(lambda s: pd.date_range(s.STARTDT, s.STOPDT2, freq='MS', inclusive = 'both'), 1).explode().rename('INFODT').dt.strftime('%m/%Y'), left_index=True, right_index=True) # Create a row for every month/year for LEDD
    LEDD_med_df.drop(['STOPDT2'], axis = 1, inplace = True) # Drop
    LEDD_med_df.rename(columns = {'STARTDT' : 'LEDD.STARTDT', 'STOPDT': 'LEDD.STOPDT'}, inplace = True) # Rename

    # Get a new df with LEDD dates merged onto corect event ids through infodts
    ppmi_merge_temp = ppmi_merge[['PATNO', 'EVENT_ID', 'INFODT']]
    ppmi_merge_temp = pd.merge(ppmi_merge_temp, LEDD_med_df, on = ['PATNO', 'INFODT'], how = "left")
    ppmi_merge_temp = ppmi_merge_temp[['PATNO', 'EVENT_ID', 'LEDD', 'LEDD.STARTDT', 'LEDD.STOPDT']] # keep only

    # Df with LD formulas as variables
    LD_only = ppmi_merge_temp[ppmi_merge_temp["LEDD"].str.contains("LD") == True] # Get df with only columns that contain LD formula (i.e. LD x0.33)
    LD_only['STOPDT2'] = LD_only['LEDD.STOPDT'] # Initialize second stop date variable
    LD_only['STOPDT2'].fillna(LD_only['LEDD.STARTDT'], inplace = True) # Fill in NaN stop dates with start dates # ASSUMPTION START and STOP on same month
    LD_only = LD_only.merge(LD_only.apply(lambda s: pd.date_range(s['LEDD.STARTDT'], s.STOPDT2, freq='MS', inclusive = 'both'), 1).explode().rename('INFODT').dt.strftime('%m/%Y'), left_index=True, right_index=True) # Create a row for every month/year for LEDD
    LD_only.drop(['STOPDT2','EVENT_ID','LEDD.STARTDT','LEDD.STOPDT'], axis = 1, inplace = True) # Drop
    ppmi_merge_LD_only = ppmi_merge[['PATNO', 'EVENT_ID', 'INFODT']]
    ppmi_merge_LD_only = pd.merge(ppmi_merge_LD_only, LD_only, on = ['PATNO', 'INFODT'], how = "left")
    ppmi_merge_LD_only = ppmi_merge_LD_only[['PATNO', 'EVENT_ID', 'LEDD']] # keep only
    ppmi_merge_LD_only.rename(columns = {'LEDD' : 'LD'}, inplace = True)
    ppmi_merge_LD_only = ppmi_merge_LD_only.drop_duplicates() # with ongoing stop dates some overlap when merging on infodts so remove dups

    # Df without LD formula var - only numeric LEDD vars
    ppmi_merge_temp = ppmi_merge_temp[ppmi_merge_temp["LEDD"].str.contains("LD") == False] # Remove LD x .33 etc rows from this df
    ppmi_merge_temp = ppmi_merge_temp.astype({'LEDD' : 'float'})
    LEDD_sum = ppmi_merge_temp.groupby(['PATNO', 'EVENT_ID'])['LEDD'].sum().reset_index() # Get sum
    LEDD_sum.rename(columns = {'LEDD' : 'LEDD.sum'}, inplace = True) # Rename
    ppmi_merge = pd.merge(ppmi_merge, LEDD_sum, on = ['PATNO','EVENT_ID'], how = "left") # Merge into ppmi_merge
    ppmi_merge = pd.merge(ppmi_merge, ppmi_merge_LD_only, on = ['PATNO','EVENT_ID'], how = "left") # Merge LD formlas into ppmi_merge


    ## GET LEVODOPA ONLY FOR BELOW CALCULATIONS - # FIXME - need more clarification before adding this
    LEDD_med_df = read_csv_drop_cols(ppmi_download_path, 'LEDD_Concomitant_Medication_Log_23May2023.csv', ['PATNO','LEDTRT', 'LEDD', 'STARTDT', 'STOPDT'], drop = False)
    search_for = ['levodopa', 'sinemet', 'rytary', 'stalevo'] # FIXME per Pavan comments but there might be others
    levodopa_only = LEDD_med_df[LEDD_med_df["LEDTRT"].str.contains('|'.join(search_for), case = False) == True]
    levodopa_only = pd.concat([func(row) for _, row in levodopa_only.iterrows()], ignore_index=True, axis=1).T
    levodopa_only['STOPDT2'] = levodopa_only['STOPDT'] # Initialize second stop date variable
    levodopa_only['STOPDT2'].fillna(levodopa_only['STARTDT'], inplace = True) # Fill in NaN stop dates with start dates # ASSUMPTION START and STOP on same month
    levodopa_only = levodopa_only.merge(levodopa_only.apply(lambda s: pd.date_range(s['STARTDT'], s.STOPDT2, freq='MS', inclusive = 'both'), 1).explode().rename('INFODT').dt.strftime('%m/%Y'), left_index=True, right_index=True) # Create a row for every month/year for LEDD
    levodopa_only.drop(['STOPDT2','STARTDT','STOPDT'], axis = 1, inplace = True)
    ppmi_merge_levodopa_only = ppmi_merge[['PATNO', 'EVENT_ID', 'INFODT']]
    ppmi_merge_levodopa_only = pd.merge(ppmi_merge_levodopa_only, levodopa_only, on = ['PATNO', 'INFODT'], how = "left")
    ppmi_merge_levodopa_only = ppmi_merge_levodopa_only[['PATNO', 'EVENT_ID', 'LEDD']] # keep only
    ppmi_merge_levodopa_only = ppmi_merge_levodopa_only.drop_duplicates() # with ongoing stop dates some overlap when merging on infodts so remove dups
    ppmi_merge_levodopa_only = ppmi_merge_levodopa_only[ppmi_merge_levodopa_only["LEDD"].str.contains("LD") == False]
    ppmi_merge_levodopa_only = ppmi_merge_levodopa_only.astype({'LEDD' : 'float'})
    ppmi_merge_levodopa_only = ppmi_merge_levodopa_only.groupby(['PATNO', 'EVENT_ID'])['LEDD'].sum().reset_index()
    ppmi_merge_levodopa_only.rename(columns = {'LEDD' : 'Levodopa.only'}, inplace = True)
    ppmi_merge = pd.merge(ppmi_merge, ppmi_merge_levodopa_only, on = ['PATNO','EVENT_ID'], how = "left") # Merge LD formlas into ppmi_merge

    # Calculate LD formulas and add to LEDD column numbers # FIXME need to switch calculation from LEDD to Levadopa only
    ppmi_merge['LEDD.sum'].fillna(0, inplace = True)
    for row_num in range(len(ppmi_merge)) :
        if ppmi_merge['LD'].loc[row_num] == 'LD x 0.33' :
            ppmi_merge['LEDD.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] == '(150.0 + LD) x 0.33' :
            ppmi_merge['LEDD.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] == '(600.0 + LD) x 0.33' :
            ppmi_merge['LEDD.sum'].loc[row_num] =  float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] == 'LD x 0.5':
            ppmi_merge['LEDD.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.5 + float(ppmi_merge['LEDD.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] =='(800.0 + LD) x 0.33':
            ppmi_merge['LEDD.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] == '(300.0 + LD) x 0.33' :
            ppmi_merge['LEDD.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] == '(225.0 + LD) x 0.33' :
            ppmi_merge['LEDD.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] == '(450.0 + LD) x 0.33' :
            ppmi_merge['LEDD.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.sum'].loc[row_num])
    ppmi_merge.drop(['LD'], axis = 1, inplace = True)
    ppmi_merge = ppmi_merge.drop_duplicates() # with ongoing stop dates some overlap when merging on infodts so remove dups
    ppmi_merge['LEDD.sum'].replace({0 : np.NaN}, inplace = True)
    ppmi_merge.drop(['Levodopa.only'], axis = 1, inplace = True) # Drop
    
   
    # ## LEDD Medication Status - FIXME Assumtion: If stop date is NA, we assume LEDD only occurred in that month
    # LEDD_med_df = read_csv_drop_cols(ppmi_download_path, 'LEDD_Concomitant_Medication_Log_23May2023.csv', ['PATNO', 'LEDD', 'STARTDT', 'STOPDT'], drop=False)
    # ppmi_merge['INFODT'] = pd.to_datetime(ppmi_merge['INFODT'], format='%m%Y', errors='ignore') # change to INFODT to type datetime so we can sort according to date
    # LEDD_med_df['STARTDT'] = pd.to_datetime(LEDD_med_df['STARTDT'], format='%m%Y', errors='ignore') # change to STARTDT to type datetime so we can sort according to date
    # LEDD_med_df['STOPDT'] = pd.to_datetime(LEDD_med_df['STOPDT'], format='%m%Y', errors='ignore') # change to STOPDT to type datetime so we can sort according to date
    # LEDD_med_df['STOPDT2'] = LEDD_med_df['STOPDT'].fillna(LEDD_med_df['STARTDT']) # Fill in NaN stop dates with start dates # ASSUMPTION START and STOP on same month
    # LEDD_med_df = LEDD_med_df.merge(LEDD_med_df.apply(lambda s: pd.date_range(s.STARTDT, s.STOPDT2, freq='MS', inclusive='both'), 1).explode().rename('INFODT').dt.strftime('%m/%Y'), left_index=True, right_index=True) # Create a row for every month/year for LEDD
    # LEDD_med_df.drop(['STOPDT2'], axis=1, inplace=True) # Drop
    # LEDD_med_df.rename(columns={'STARTDT': 'LEDD.STARTDT', 'STOPDT': 'LEDD.STOPDT'}, inplace=True) # Rename

    # # Get a new df with LEDD dates merged onto correct event ids through infodts
    # ppmi_merge_temp = ppmi_merge[['PATNO', 'EVENT_ID', 'INFODT']]
    # ppmi_merge_temp = pd.merge(ppmi_merge_temp, LEDD_med_df, on=['PATNO', 'INFODT'], how="left")
    # ppmi_merge_temp = ppmi_merge_temp[['PATNO', 'EVENT_ID', 'LEDD', 'LEDD.STARTDT', 'LEDD.STOPDT']] # keep only

    # # Df with LD formulas as variables
    # LD_only = ppmi_merge_temp[ppmi_merge_temp['LEDD'].str.contains("LD") == True] # Get df with only columns that contain LD formula (i.e. LD x0.33)
    # LD_only['STOPDT2'] = LD_only['LEDD.STOPDT'].fillna(LD_only['LEDD.STARTDT']) # Fill in NaN stop dates with start dates # ASSUMPTION START and STOP on same month
    # LD_only = LD_only.merge(LD_only.apply(lambda s: pd.date_range(s['LEDD.STARTDT'], s.STOPDT2, freq='MS', inclusive='both'), 1).explode().rename('INFODT').dt.strftime('%m/%Y'), left_index=True, right_index=True) # Create a row for every month/year for LEDD
    # LD_only.drop(['STOPDT2', 'EVENT_ID', 'LEDD.STARTDT', 'LEDD.STOPDT'], axis=1, inplace=True) # Drop
    # ppmi_merge_LD_only = pd.merge(ppmi_merge[['PATNO', 'EVENT_ID', 'INFODT']], LD_only, on=['PATNO', 'INFODT'], how="left")
    # ppmi_merge_LD_only = ppmi_merge_LD_only[['PATNO', 'EVENT_ID', 'LEDD']] # keep only
    # ppmi_merge_LD_only.rename(columns={'LEDD': 'LD'}, inplace=True)
    # ppmi_merge_LD_only = ppmi_merge_LD_only.drop_duplicates() # with ongoing stop dates some overlap when merging on infodts so remove dups

    # # Df without LD formula var - only numeric LEDD vars
    # ppmi_merge_temp = ppmi_merge_temp[ppmi_merge_temp['LEDD'].str.contains("LD") == False] # Remove LD x .33 etc rows from this df
    # ppmi_merge_temp = ppmi_merge_temp.astype({'LEDD': 'float'})
    # LEDD_sum = ppmi_merge_temp.groupby(['PATNO', 'EVENT_ID'])['LEDD'].sum().reset_index() # Get sum
    # LEDD_sum.rename(columns={'LEDD': 'LEDD.sum'}, inplace=True) # Rename
    # ppmi_merge = pd.merge(ppmi_merge, LEDD_sum, on=['PATNO', 'EVENT_ID'], how="left") # Merge into ppmi_merge
    # ppmi_merge = pd.merge(ppmi_merge, ppmi_merge_LD_only, on=['PATNO', 'EVENT_ID'], how="left") # Merge LD formulas into ppmi_merge

    # ## GET LEVODOPA ONLY FOR BELOW CALCULATIONS - # FIXME - need more clarification before adding this
    # LEDD_med_df = read_csv_drop_cols(ppmi_download_path, 'LEDD_Concomitant_Medication_Log_23May2023.csv', ['PATNO', 'LEDTRT', 'LEDD', 'STARTDT', 'STOPDT'], drop=False)
    # search_for = ['levodopa', 'sinemet', 'rytary', 'stalevo'] # FIXME per Pavan comments but there might be others
    # levodopa_only = LEDD_med_df[LEDD_med_df['LEDTRT'].str.contains('|'.join(search_for), case=False) == True]
    # levodopa_only['STOPDT2'] = levodopa_only['STOPDT'].fillna(levodopa_only['STARTDT']) # Fill in NaN stop dates with start dates # ASSUMPTION START and STOP on same month
    # levodopa_only = levodopa_only.merge(levodopa_only.apply(lambda s: pd.date_range(s['STARTDT'], s.STOPDT2, freq='MS', inclusive='both'), 1).explode().rename('INFODT').dt.strftime('%m/%Y'), left_index=True, right_index=True) # Create a row for every month/year for LEDD
    # levodopa_only.drop(['STOPDT2', 'STARTDT', 'STOPDT'], axis=1, inplace=True)
    # ppmi_merge_levodopa_only = pd.merge(ppmi_merge[['PATNO', 'EVENT_ID', 'INFODT']], levodopa_only, on=['PATNO', 'INFODT'], how="left")
    # ppmi_merge_levodopa_only = ppmi_merge_levodopa_only[['PATNO', 'EVENT_ID', 'LEDD']] # keep only
    # ppmi_merge_levodopa_only = ppmi_merge_levodopa_only.drop_duplicates() # with ongoing stop dates some overlap when merging on infodts so remove dups
    # ppmi_merge_levodopa_only = ppmi_merge_levodopa_only[ppmi_merge_levodopa_only['LEDD'].str.contains("LD") == False]
    # ppmi_merge_levodopa_only = ppmi_merge_levodopa_only.astype({'LEDD': 'float'})
    # ppmi_merge_levodopa_only = ppmi_merge_levodopa_only.groupby(['PATNO', 'EVENT_ID'])['LEDD'].sum().reset_index()
    # ppmi_merge_levodopa_only.rename(columns={'LEDD': 'Levodopa.only'}, inplace=True)
    # ppmi_merge = pd.merge(ppmi_merge, ppmi_merge_levodopa_only, on=['PATNO', 'EVENT_ID'], how="left") # Merge LD formulas into ppmi_merge


    # ld_mapping = {
    #     'LD x 0.33': 0.33,
    #     '(150.0 + LD) x 0.33': 0.33,
    #     '(600.0 + LD) x 0.33': 0.33,
    #     'LD x 0.5': 0.5,
    #     '(800.0 + LD) x 0.33': 0.33,
    #     '(300.0 + LD) x 0.33': 0.33,
    #     '(225.0 + LD) x 0.33': 0.33,
    #     '(450.0 + LD) x 0.33': 0.33
    # }

    # ld_columns = ['LD x 0.33', '(150.0 + LD) x 0.33', '(600.0 + LD) x 0.33',
    #             'LD x 0.5', '(800.0 + LD) x 0.33', '(300.0 + LD) x 0.33',
    #             '(225.0 + LD) x 0.33', '(450.0 + LD) x 0.33']

    # ppmi_merge['LEDD.sum'].fillna(0, inplace=True)

    # for row_num, ld_value in enumerate(ppmi_merge['LD']):
    #     if ld_value in ld_columns:
    #         ld_factor = ld_mapping[ld_value]
    #         levodopa_only = float(ppmi_merge['Levodopa.only'].loc[row_num])
    #         ppmi_merge.loc[row_num, 'LEDD.sum'] += levodopa_only * ld_factor

    # ppmi_merge.drop(['LD'], axis=1, inplace=True)
    # ppmi_merge = ppmi_merge.drop_duplicates()
    # ppmi_merge['LEDD.sum'].replace({0: np.NaN}, inplace=True)
    # ppmi_merge.drop(['Levodopa.only'], axis=1, inplace=True)

    # return ppmi_merge


    ## LEDD Medication Status - FIXME Assumption : If stop date is NA we assume therapy is ongoing
    LEDD_med_df = read_csv_drop_cols(ppmi_download_path, 'LEDD_Concomitant_Medication_Log_23May2023.csv', ['PATNO', 'LEDD', 'STARTDT', 'STOPDT'], drop = False)
    ppmi_merge['INFODT'] = pd.to_datetime(ppmi_merge['INFODT'], format = '%m%Y', errors = 'ignore') # Change to INFODT to type datetime so we can sort according to date
    LEDD_med_df['STARTDT'] = pd.to_datetime(LEDD_med_df['STARTDT'], format = '%m%Y', errors = 'ignore') # Change to INFODT to type datetime so we can sort according to date
    LEDD_med_df['STOPDT'] = pd.to_datetime(LEDD_med_df['STOPDT'], format = '%m%Y', errors = 'ignore') # Change to INFODT to type datetime so we can sort according to date
    LEDD_med_df['STOPDT3'] = LEDD_med_df['STOPDT']
    LEDD_med_df['STOPDT3'].fillna('01/2022', inplace = True) # ASSUMPTION fill in ongoing stopdate (12/2021 is max infodt in ppmi_merge file)
    LEDD_med_df['STOPDT3'] = pd.to_datetime(LEDD_med_df['STOPDT3'], format = '%m%Y', errors = 'ignore') # change to INFODT to type datetime so we can sort according to date
    LEDD_med_df = LEDD_med_df.merge(LEDD_med_df.apply(lambda s: pd.date_range(s.STARTDT, s.STOPDT3, freq='MS', inclusive = 'both'), 1).explode().rename('INFODT').dt.strftime('%m/%Y'), left_index=True, right_index=True) # Create a row for every month/year for LEDD
    LEDD_med_df.rename(columns = {'LEDD' : 'LEDD.ongoing', 'STARTDT' : 'LEDD.STARTDT.ongoing', 'STOPDT3': 'LEDD.STOPDT.ongoing'}, inplace = True) # Rename

    # Get a new df with LEDD dates merged onto corect event ids through infodts
    ppmi_merge_temp = ppmi_merge[['PATNO', 'EVENT_ID', 'INFODT']]
    ppmi_merge_temp = pd.merge(ppmi_merge_temp, LEDD_med_df, on = ['PATNO', 'INFODT'], how = "left")
    ppmi_merge_temp = ppmi_merge_temp[['PATNO', 'EVENT_ID', 'LEDD.ongoing', 'LEDD.STARTDT.ongoing', 'LEDD.STOPDT.ongoing']] # keep only

    # Df with LD formulas as variables
    LD_only = ppmi_merge_temp[ppmi_merge_temp["LEDD.ongoing"].str.contains("LD")==True] # Get df with only columns that contain LD formula (i.e. LD x0.33)
    LD_only['STOPDT2'] = LD_only['LEDD.STOPDT.ongoing'] # Initialize second stop date variable
    LD_only['STOPDT2'].fillna('01/2022', inplace = True) # Fill in NaN stop dates with start dates # ASSUMPTION
    LD_only['STOPDT2'] = pd.to_datetime(LD_only['STOPDT2'], format = '%m%Y', errors = 'ignore') # change to INFODT to type datetime so we can sort according to date
    LD_only = LD_only.merge(LD_only.apply(lambda s: pd.date_range(s['LEDD.STARTDT.ongoing'], s.STOPDT2, freq='MS', inclusive = 'both'), 1).explode().rename('INFODT').dt.strftime('%m/%Y'), left_index=True, right_index=True) # Create a row for every month/year for LEDD
    LD_only.drop(['STOPDT2','EVENT_ID','LEDD.STARTDT.ongoing','LEDD.STOPDT.ongoing'], axis = 1, inplace = True) # Drop
    ppmi_merge_LD_only = ppmi_merge[['PATNO', 'EVENT_ID', 'INFODT']]
    ppmi_merge_LD_only = pd.merge(ppmi_merge_LD_only, LD_only, on = ['PATNO', 'INFODT'], how = "left")
    ppmi_merge_LD_only = ppmi_merge_LD_only[['PATNO', 'EVENT_ID', 'LEDD.ongoing']] # keep only
    ppmi_merge_LD_only.rename(columns = {'LEDD.ongoing' : 'LD'}, inplace = True)
    ppmi_merge_LD_only = ppmi_merge_LD_only.drop_duplicates() # with ongoing stop dates some overlap when merging on infodts so remove dups

    # Df without LD formula var - only numeric LEDD vars
    ppmi_merge_temp = ppmi_merge_temp[ppmi_merge_temp["LEDD.ongoing"].str.contains("LD") == False] # Remove LD from this df (add in later)
    ppmi_merge_temp = ppmi_merge_temp.astype({'LEDD.ongoing' : 'float'})
    LEDD_sum = ppmi_merge_temp.groupby(['PATNO', 'EVENT_ID'])['LEDD.ongoing'].sum().reset_index() #  Sum
    LEDD_sum.rename(columns = {'LEDD.ongoing' : 'LEDD.ongoing.sum'}, inplace = True)
    ppmi_merge = pd.merge(ppmi_merge, LEDD_sum, on = ['PATNO','EVENT_ID'], how = "left") # Merge into ppmi_merge
    ppmi_merge = pd.merge(ppmi_merge, ppmi_merge_LD_only, on = ['PATNO','EVENT_ID'], how = "left") # Merge into ppmi_merge

    ## If in LD column there is a (i.e. 150 + LD) * 0.33) - create a new duplicate column with just 150 variable - bc this LEDD needs to be added to full LEDD and these formulas are therefore not correct?  # per Pavan notes issues
    ## GET LEVODOPA ONLY FOR BELOW CALCULATIONS - # FIXME - need more clarification before adding this
    LEDD_med_df = read_csv_drop_cols(ppmi_download_path, 'LEDD_Concomitant_Medication_Log_23May2023.csv', ['PATNO','LEDTRT', 'LEDD', 'STARTDT', 'STOPDT'], drop = False)
    search_for = ['levodopa', 'sinemet', 'rytary', 'stalevo'] # FIXME per Pavan comments but there might be others
    levodopa_only = LEDD_med_df[LEDD_med_df["LEDTRT"].str.contains('|'.join(search_for), case = False) == True]
    levodopa_only = pd.concat([func(row) for _, row in levodopa_only.iterrows()], ignore_index=True, axis=1).T
    levodopa_only['STOPDT2'] = levodopa_only['STOPDT'] # Initialize second stop date variable
    levodopa_only['STOPDT2'].fillna('01/2022', inplace = True) # Fill in NaN stop dates with start dates # ASSUMPTION START and STOP on same month
    levodopa_only = levodopa_only.merge(levodopa_only.apply(lambda s: pd.date_range(s['STARTDT'], s.STOPDT2, freq='MS', inclusive = 'both'), 1).explode().rename('INFODT').dt.strftime('%m/%Y'), left_index=True, right_index=True) # Create a row for every month/year for LEDD
    levodopa_only.drop(['STOPDT2','STARTDT','STOPDT'], axis = 1, inplace = True)
    ppmi_merge_levodopa_only = ppmi_merge[['PATNO', 'EVENT_ID', 'INFODT']]
    ppmi_merge_levodopa_only = pd.merge(ppmi_merge_levodopa_only, levodopa_only, on = ['PATNO', 'INFODT'], how = "left")
    ppmi_merge_levodopa_only = ppmi_merge_levodopa_only[['PATNO', 'EVENT_ID', 'LEDD']] # keep only
    ppmi_merge_levodopa_only = ppmi_merge_levodopa_only.drop_duplicates() # with ongoing stop dates some overlap when merging on infodts so remove dups
    ppmi_merge_levodopa_only = ppmi_merge_levodopa_only[ppmi_merge_levodopa_only["LEDD"].str.contains("LD") == False]
    ppmi_merge_levodopa_only = ppmi_merge_levodopa_only.astype({'LEDD' : 'float'})
    ppmi_merge_levodopa_only = ppmi_merge_levodopa_only.groupby(['PATNO', 'EVENT_ID'])['LEDD'].sum().reset_index()
    ppmi_merge_levodopa_only.rename(columns = {'LEDD' : 'Levodopa.only'}, inplace = True)
    ppmi_merge = pd.merge(ppmi_merge, ppmi_merge_levodopa_only, on = ['PATNO','EVENT_ID'], how = "left") # Merge LD formlas into ppmi_merge

    # Calculate LD formulas and add to LEDD column numbers # FIXME need to switch calculation from LEDD to Levadopa only
    for row_num in range(len(ppmi_merge)) :
        if ppmi_merge['LD'].loc[row_num] == 'LD x 0.33' :
            ppmi_merge['LEDD.ongoing.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.ongoing.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] == '(150.0 + LD) x 0.33' :
            ppmi_merge['LEDD.ongoing.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.ongoing.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] == '(600.0 + LD) x 0.33' :
            ppmi_merge['LEDD.ongoing.sum'].loc[row_num] =  float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.ongoing.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] == 'LD x 0.5':
            ppmi_merge['LEDD.ongoing.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.5 + float(ppmi_merge['LEDD.ongoing.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] =='(800.0 + LD) x 0.33':
            ppmi_merge['LEDD.ongoing.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.ongoing.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] == '(300.0 + LD) x 0.33' :
            ppmi_merge['LEDD.ongoing.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.ongoing.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] == '(225.0 + LD) x 0.33' :
            ppmi_merge['LEDD.ongoing.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.ongoing.sum'].loc[row_num])
        elif ppmi_merge['LD'].loc[row_num] == '(450.0 + LD) x 0.33' :
            ppmi_merge['LEDD.ongoing.sum'].loc[row_num] = float(ppmi_merge['Levodopa.only'].loc[row_num]) * 0.33 + float(ppmi_merge['LEDD.ongoing.sum'].loc[row_num])

    #ppmi_merge['LEDD.STOPDT.ongoing'].replace({'01/2022'  : np.NaN}, inplace = True) # Replace filler stop date for ledd ongoing back to nan
    ppmi_merge.drop(['LD'], axis = 1, inplace = True)
    return ppmi_merge





def make_categorical_LEDD_col(df, df_col, new_df_col, num_categories) :
    """
    Function to take LEDD dosages and make three equal categorical columns
    """
    df_col_2_list = sorted(set(df[df_col].dropna().to_list())) # sort list of all dosages from lowest to highest
    lists = np.array_split(df_col_2_list, num_categories) # Split list into thirds
    count = 1
    start = 0
    for i in range(num_categories) :
        df.loc[(df[df_col] >= start ) & (df[df_col] <= lists[i][-1]) , new_df_col ] = 'OnQ' + str(count)
        start = lists[i][-1] + 0.1
        count += 1
    return df



def format_genetics_df(genetics_file_path : str, csv_filename) :
    """
    Format genetics_df to make merge-able with ppmi_merge
    """
    genetics_df = read_csv_drop_cols(genetics_file_path, csv_filename, ['COUNTED', 'ALT', 'SNP', '(C)M'] , drop=True)
    
    

    # column_mappings = {col: int(col.split('_')[-1]) for col in genetics_df.columns if '_' in col}
    # genetics_df.rename(columns=column_mappings, inplace=True)


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
    return genetics_df



def fill_non_lateralized_subscore(df, subscore_lateralized_name, subscore_name) :
    """
    If lateralized subscore is nan - input the non-lateralized score for Tremor and Brady.Rigidity
    """

    latisna = df[subscore_lateralized_name].isna() & df[subscore_name].notna()
    df[subscore_lateralized_name].loc[latisna] = df[subscore_name].loc[latisna]
    return df



def add_comorbidities(ppmi_merge, ppmi_download_path) :
    ## Comorbidities # FIXME not useful column
    comorbid_df = pd.read_csv(ppmi_download_path + 'Medical_Conditions_Log_23May2023.csv', skipinitialspace=True) # Medication history
    comorbid_df.replace({';' : ','}, regex = True, inplace = True) # Replace ';' with ','
    comorbid_df = comorbid_df[['PATNO', 'EVENT_ID', 'MHDIAGDT','MHTERM']] # keep only
    comorbid_df['MHTERM'] = comorbid_df['MHTERM'].str.capitalize() # Capitalize all MHTERM names
    comorbid_df['MHDIAGDT'].fillna('NA', inplace = True) # If no diagnosis date - fill in with NA
    comorbid_df['MHDIAGDT'] = '(' + comorbid_df['MHDIAGDT'].astype(str) + ')'# Put parentheses around diagnosis date
    comorbid_df = comorbid_df.astype({"MHDIAGDT" : 'str'}) # Change date to string
    comorbid_df = merge_columns(comorbid_df, ['MHTERM', 'MHDIAGDT'], 'Medical.History.Description(Diagnosis.Date)' , ' ')
    comorbid_df = comorbid_df.groupby(['PATNO','EVENT_ID'])['Medical.History.Description(Diagnosis.Date)'].apply('; '.join)
    ppmi_merge = pd.merge(ppmi_merge, comorbid_df, on = ['PATNO','EVENT_ID'], how = "outer")
    return ppmi_merge



def add_analytic_cohort(df, analytic_cohort_list):
    df['Analytic.Cohort'] = df['Subject.ID'].apply(lambda x: 'Analytic Cohort' if x in analytic_cohort_list else 'Not Analytic Cohort')
    return df
    


def add_lateralized_subscores(df : pd.DataFrame, subscore_side_list : list, side : str, new_col_name : str) :
    """
    Include lateralized subscroes (i.e. Brady Rigidity and Tremor subscores) into dataframe.
    Arguments
    ------------------
    df : pd.DataFrame containing scores that make up subscore
    subscore_side_list : list containing column names of the scores that make up the subscore
    side : 'Left' or 'Right'
    new_col_name : name of new column name with lateralized subscore
    """
    subscore_side = df[subscore_side_list]  # Get dataframe of only columns in brady_left
    df[new_col_name] = 0 # Initialize lateralized variable
    subscore_side.loc[subscore_side['Dominant.Side.Disease'] != side, :] = np.nan # Make all rows nan if dominant side of disease is not left
    subscore_side_temp = subscore_side.drop('Dominant.Side.Disease',1) # Drop dominant side of disease - necessary because this cannot be summed in next line
    idx  = subscore_side_temp.loc[pd.isnull(subscore_side_temp).any(1), :].index
    df[new_col_name] = subscore_side_temp.sum(axis = 1) # Sum of all columns in each row where dom side is left
    df[new_col_name].iloc[idx] = np.nan # Fill in subscores that should be nans as nan
    return df




def add_symmetric_subscores(df : pd.DataFrame, subscore_side_list : list, side : str, new_col_name : str, ext : str) :
    subscore_side = df[subscore_side_list]  # Get dataframe of only columns in brady_left
    df[new_col_name] = 0 # Initialize lateralized variable
    subscore_side.loc[subscore_side['Dominant.Side.Disease'] != side, :] = np.nan # Make all rows nan if dominant side of disease is not side
    subscore_side_temp = subscore_side.drop('Dominant.Side.Disease',1) # Drop dominant side of disease - necessary because this cannot be summed in next line
    idx  = subscore_side_temp.loc[pd.isnull(subscore_side_temp).any(1), :].index
    x = subscore_side_temp.fillna(0) # because adding 1 plus nan equals nan
    if "Brady" in new_col_name :
        df[new_col_name] = x['Rigidity.Neck' + ext ] + (x['Rigidity.RUE' + ext] + x['Rigidity.LUE'+ ext ])/2 + (x['Rigidity.RLE'+ ext] + x['Rigidity.LLE'+ ext])/2  + (x['Finger.Tapping.Right.Hand'+ ext] +x['Finger.Tapping.Left.Hand'+ ext])/2 + (x['Hand.Movements.Right.Hand'+ ext] + x['Hand.Movements.Left.Hand'+ ext])/2 + (x['Pronation.Supination.Right.Hand'+ ext]+x['Pronation.Supination.Left.Hand'+ ext])/2 +  (x['Toe.Tapping.Right.Foot'+ ext]+ x['Toe.Tapping.Left.Foot'+ ext])/2 +  (x['Leg.Agility.Right.Leg'+ ext] + x['Leg.Agility.Left.Leg'+ ext])/2
        df[new_col_name].iloc[idx] = np.nan # Fill in subscores that should be nans as nan
    elif "Tremor" in new_col_name :
        df[new_col_name] = x['Tremor.UPDRS2.Num'] +  (x['Postural.Tremor.Right.Hand' + ext ]  + x['Postural.Tremor.Left.Hand' + ext ])/2 + (x['Kinetic.Tremor.Right.Hand' + ext ] + x['Kinetic.Tremor.Left.Hand'+ ext ])/2 + (x['Rest.Tremor.Amplitude.RUE' + ext ]+ x['Rest.Tremor.Amplitude.LUE' + ext])/2 + (x['Rest.Tremor.Amplitude.RLE' + ext ] +  x['Rest.Tremor.Amplitude.LLE' + ext])/2 + x['Rest.Tremor.Amplitude.Lip.Jaw' + ext] + x['Constancy.of.Rest.Tremor' + ext]
        df[new_col_name].iloc[idx] = np.nan
    return df

    

def remove_duplicate_datscans(ppmi_merge):
    # FIXME - After merging in datscan files, duplicate event ids being created one with DATSCAN as "Completed" one with DATSCAN as "not completed" - if there are both of these - keep only "Completed"
    duplicate_datscan = ppmi_merge[['PATNO','EVENT_ID']].duplicated(keep = False) # Find locations of True for duplicated subs w/ 2 MRI at baseline
    duplicate_datscan_index = ppmi_merge[duplicate_datscan == True].index.tolist() # Get index of duplicates
    dup_subid_list = [] # Initialize duplicate subid list variable
    [dup_subid_list.append(index) for index in duplicate_datscan_index if ppmi_merge['DATSCAN'][index] == 'Not Completed']# Get the indices of duplicate subids that were labeled as Not Completed
    ppmi_merge = ppmi_merge.reset_index(drop = True)
    [ppmi_merge.drop(index = i, axis = 1, inplace = True) for i in reversed(dup_subid_list) if ppmi_merge['DATSCAN'][i] == 'Not Completed'] # Get rid of the duplicate subids that were labeled as Not Completed
    return ppmi_merge




def add_datiq(ppmi_merge, datiq_path):
    datiq = pd.ExcelFile(datiq_path + 'IQDAT_PPMI_PDHCproromalPD_12July2022_send.xlsx')

    # Read necessary sheets
    pd_datiq = pd.read_excel(datiq, 'PD').drop('#', axis=1)
    hc_datiq = pd.read_excel(datiq, 'HC').drop('#', axis=1)
    prodromal_datiq = pd.read_excel(datiq, 'prodromalPD').drop('#', axis=1)

    # Create 'PATNO' and 'INFODT' columns
    dfs = [pd_datiq, hc_datiq]
    for df in dfs:
        split_names = df['subjNames'].str.split('_', expand=True)
        df['PATNO'] = split_names[0]
        df['INFODT'] = split_names[1].str.split('-', expand=True)[0]

    # Fix prodromal dates
    prodromal_info = pd.read_csv(datiq_path + 'DATIQ_results_ver2_prodromalPD_IDsheets.csv')
    prodromal_info['INFODT'] = pd.to_datetime(prodromal_info['ScanDate'], format='%d-%b-%y').dt.strftime('%Y%m')
    prodromal_info.rename(columns={'FullFilename': 'subjNames'}, inplace=True)
    prodromal_datiq = pd.merge(prodromal_datiq, prodromal_info[['subjNames', 'INFODT']], how='outer', on='subjNames')
    prodromal_datiq['PATNO'] = prodromal_datiq['subjNames'].str.split('_').str[2]
    prodromal_datiq.drop('subjNames', axis=1, inplace=True)

    # Add Enroll.Diagnosis column
    prodromal_datiq['Enroll.Diagnosis'] = 'Prodromal'
    hc_datiq['Enroll.Diagnosis'] = 'Healthy Control'
    pd_datiq['Enroll.Diagnosis'] = "Parkinson's Disease"

    # Define column order and reindex
    column_order = ['PATNO', 'INFODT', 'Enroll.Diagnosis', 'DATLoad(%)', 'DATLoadLeft(%)' , 'DATLoadRight(%)']
    dfs = pd.concat([prodromal_datiq, hc_datiq, pd_datiq]).reindex(columns=column_order)
    dfs.rename(columns = {'DATLoad(%)' :'DATLoad.Percent', 'DATLoadLeft(%)':'DATLoadLeft.Percent' , 'DATLoadRight(%)':'DATLoadRight.Percent'}, inplace = True)
    
    dfs['INFODT'] = dfs['INFODT'].str[4:6] + '/' + dfs['INFODT'].str[0:4]
    dfs['PATNO'] = dfs['PATNO'].astype(int)

    ppmi_merge = pd.merge(ppmi_merge, dfs, how='outer', on=['PATNO', 'INFODT', 'Enroll.Diagnosis'])
    ppmi_merge.fillna('NA', inplace=True)

    return ppmi_merge




def add_mri_csv(ppmi_merge, ppmi_download_path, code_list) :
    mri_df = read_csv_drop_cols(ppmi_download_path, 'Magnetic_Resonance_Imaging__MRI__23May2023.csv',[ 'PATNO', 'EVENT_ID', 'INFODT', 'MRICMPLT', 'MRIWDTI', 'MRIWRSS', 'MRIRSLT', 'MRIRSSDF' ], drop = False)
    mri_df = decode(mri_df, code_list, 'MRI', ['MRIWDTI','MRIWRSS','MRIRSSDF','MRICMPLT','MRIRSLT'])
    mri_df.rename(columns = { 'INFODT' : 'Image.Acquisition.Date', 'MRICMPLT' : 'MRI.Completed', 'MRIWDTI' : 'MRI.DTI' , 'MRIWRSS' : 'MRI.Resting.State' , 'MRIRSLT' : 'MRI.Results' , 'MRIRSSDF' : 'Resting.State.Dif.Day.PDMed.Use'}, inplace = True) # Rename
    # FIXME Some subjects had two baseline rows - 1 with incomplete MRI.Completed and 1 with complete as MRI.Complete - I am only keeping the one that is complete bc the data we have on s3 is complete
    duplicate_mri = mri_df[['PATNO','EVENT_ID']].duplicated(keep = False) # Find locations of True for duplicated subs w/ 2 MRI at baseline
    duplicate_mri_index = mri_df[duplicate_mri == True].index.tolist() # Get index of duplicates
    dup_subid_list = [] # Initialize duplicate subid list variable
    [dup_subid_list.append(index) for index in duplicate_mri_index if mri_df['MRI.Completed'][index] == 'Not Completed']# Get the indices of duplicate subids that were labeled as Not Completed
    mri_df = mri_df.reset_index(drop = True)
    [mri_df.drop(index = i, axis = 1, inplace = True) for i in reversed(dup_subid_list) if mri_df['MRI.Completed'][i] == 'Not Completed'] # Get rid of the duplicate subids that were labeled as Not Completed (that also have another labeled as completed)
    ppmi_merge = pd.merge(ppmi_merge, mri_df, on = ['PATNO','EVENT_ID'], how = "outer")
    return ppmi_merge




def calculate_subscores(df, new_col_name, subscore_list) :
    """
    Add Brady-Rigidity, Tremor and PIGD Subscores
    Subscore info from :
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7242837/
    https://www.movementdisorders.org/MDS-Files1/PDFs/Rating-Scales/MDS-UPDRS_English_FINAL.pdf
    """

    subscore_only = df[subscore_list] # extract df of only cols we are interested in for current subscore
    df[new_col_name] = 0 # initalize new col for subscore
    idx  = subscore_only.loc[pd.isnull(subscore_only).any(1), :].index
    df[new_col_name] = subscore_only.sum(axis = 1) # Get sum of subscore
    df[new_col_name].iloc[idx] = np.nan # Replace rows that should be nan with nan
    return df



def add_extension_to_column_names(df, skip_col_list, ext):
    # For all UPDRS df columns - add the respective extension for which UPDRS assessment it is
    for col_name in df :
        if col_name not in skip_col_list :
            df.rename(columns = {str(col_name) : str(col_name) + ext }, inplace = True)
    return df



def add_t1(ppmi_merge):
    ppmi_merge = pd.concat([ppmi_merge, pd.DataFrame(columns=['Subid.Date.TEMP'])])  # Create 'Subid.Date.TEMP' column
    ppmi_merge['PATNO'] = ppmi_merge['PATNO'].astype(int)
    ppmi_merge['Subid.Date.TEMP'] = ppmi_merge['PATNO'].astype(str) + '/' + ppmi_merge['Image.Acquisition.Date'].str.split('/').str[1] + ppmi_merge['Image.Acquisition.Date'].str.split('/').str[0]
    subid_date_ordered = pd.Series(ppmi_merge['Subid.Date.TEMP'].dropna().tolist())  # Convert to a pandas Series 
    
    keys = search_s3('invicro-ia-object-repository', 'refined/ppmi/data/PPMI/', 'T1w/')
    woutppmi = [key.split('PPMI/')[1] for key in keys] # Remove PPMI/ from key
    woutt1w = [key.split('/T1w/')[0] for key in woutppmi] # Remove 'T1w' from key
    s3woutdate = [current_subid_date[:-2] for current_subid_date in woutt1w] # Remove the day from date - want only yearmonth i.e. 202106
    matches = [current_subid_date for current_subid_date in subid_date_ordered if current_subid_date in s3woutdate] 

    s3_data = []
    s3_df = pd.DataFrame(columns = ['PATNO', 'EVENT_ID', 'T1.s3.Image.Name']) # create s3_df dataframe
    for current_subid_date_temp in matches:
        matching_keys = [key for key in woutppmi if current_subid_date_temp in key and key.endswith('.nii.gz')]
        for image_id in matching_keys:
            image_id_split = image_id.split('/')
            s3_data.append({'PATNO': image_id_split[0], 'EVENT_ID': ppmi_merge.loc[ppmi_merge['Subid.Date.TEMP'] == current_subid_date_temp, 'EVENT_ID'].iloc[0], 'T1.s3.Image.Name': image_id_split[-1]})

    s3_df = pd.concat([s3_df, pd.DataFrame(s3_data)])    
    s3_df['PATNO'] = s3_df['PATNO'].astype(int)
    s3_df['Image_ID_merge'] = s3_df['T1.s3.Image.Name'].str.split('.').str[0].str.split('-').str[4]
    ppmi_merge = pd.merge(ppmi_merge, s3_df, on=['PATNO', 'EVENT_ID'], how='outer')
    ppmi_merge.drop(['Subid.Date.TEMP'], axis = 1, inplace = True)

    return ppmi_merge



def change_updrs_to_floats(df) :
    """
    Change all UPDRS dataframe cols begin with 'N' to floats
    """
    
    for col_name in df :
        if col_name.startswith('N') :
            df[col_name] = pd.to_numeric(df[col_name], errors = 'coerce', downcast = 'float')
    return df



def fixed_variables(ppmi_merge: pd.DataFrame, fixed_var_list: List[str]) -> pd.DataFrame:
    for col_name in fixed_var_list:
        ppmi_merge[col_name].fillna('NA', inplace=True)
        na_rows = ppmi_merge[col_name] == 'NA'  # Find rows with NA values
        
        # Get unique PATNO values in the NA rows
        unique_patnos = ppmi_merge.loc[na_rows, 'PATNO'].unique()
        
        # Iterate over unique PATNO values and fill in NA values
        for patno in unique_patnos:
            mask = (ppmi_merge['PATNO'] == patno) & (~na_rows)
            fixed_var_value = ppmi_merge.loc[mask, col_name].values
            if fixed_var_value.any():
                ppmi_merge.loc[na_rows & (ppmi_merge['PATNO'] == patno), col_name] = fixed_var_value[0]
    
    return ppmi_merge

    



def add_bestEventID_resnet(ppmi_merge) :
    ## Inlcude columns for bestEventID (bestScreening, bestBaseline, etc) and denote the highest resnetGrade with True (else = False)
    myevs = ppmi_merge['Event.ID'].unique() # Unique event ids
    uids = ppmi_merge['Subject.ID'].unique() # Unique subject ids
    for myev in myevs :
        if not isNaN(myev) :
            mybe = "best" + myev # Create best Visit column
            ppmi_merge[mybe] = False # Set all best visit to be False
            for u in uids :
                selu = ppmi_merge.loc[(ppmi_merge['Subject.ID'] == u) & (ppmi_merge['Event.ID'] == myev) & (ppmi_merge['resnetGrade'].notna())] # For one subject at one event id if resnetGrade not na
                if len(selu) == 1 : # If there is one event id for that subject
                    idx = selu.index # Ge the index
                    ppmi_merge.loc[idx, mybe] = True
                if len(selu) > 1 : # IF there is more than one event id for that subject and resnet grade is not na
                    maxidx = selu[['resnetGrade']].idxmax() # Get the higher resnetGrade for each visit if there are more than one
                    ppmi_merge.loc[maxidx, mybe] = True
    return ppmi_merge







def add_bestImageAcquisitionDate(ppmi_merge) :
    """
    Include a column for bestAtImage.Acquisition.Date - denote the one or highest resnetGrade with True (else = False)
    """
    ppmi_merge['bestAtImage.Acquisition.Date'] = False # Initialize bestAtImage.Acuqisition.Date col
    myevs = ppmi_merge['Event.ID'].unique() # Unique event ids
    uids = ppmi_merge['Subject.ID'].unique() # Unique subject ids
    for myev in myevs :
        for u in uids :
            selu = ppmi_merge.loc[(ppmi_merge['Subject.ID'] == u) & (ppmi_merge['Event.ID'] == myev) & (ppmi_merge['resnetGrade'].notna())]
            if len(selu) == 1 : # If there is one event id for that subject
                idx = selu.index # Get the index
                ppmi_merge.loc[idx, 'bestAtImage.Acquisition.Date'] = True
            if len(selu) > 1 : # IF there is more than one event id for that subject and resnet grade is not na
                maxidx = selu[['resnetGrade']].idxmax() # Get the higher resnetGrade for each visit if there are more than one
                ppmi_merge.loc[maxidx, 'bestAtImage.Acquisition.Date'] = True
    return ppmi_merge



def add_DXsimplified(ppmi_merge):
    ppmi_merge['DXsimplified'] = '' # Initialize DXsimplfied
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == 'Healthy Control', 'DXsimplified'] = 'HC'
    ppmi_merge.loc[ppmi_merge['Enroll.Diagnosis'] == 'Healthy Control', 'DXsimplified'] = 'HC'
    ppmi_merge.loc[ppmi_merge['Enroll.Diagnosis'] == 'Parkinson\'s Disease', 'DXsimplified'] = 'Sporadic_PD'
    ppmi_merge.loc[ppmi_merge['Enroll.Diagnosis'] == 'SWEDD', 'DXsimplified'] = "nonPDorMSA"
    ppmi_merge.loc[ppmi_merge['Enroll.Diagnosis'] == "Prodromal", 'DXsimplified'] = "Sporadic_Pro"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "GBA", 'DXsimplified'] = "GBA_HC"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "Genetic : GBA", 'DXsimplified'] = "GBA_PD"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "Genetic : GBA not Prodromal", 'DXsimplified'] = "GBA_PD"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "Genetic : GBA Prodromal", 'DXsimplified'] = "GBA_Pro"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "Genetic : LRRK2", 'DXsimplified'] = "LRRK2_PD"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "Genetic : LRRK2 + GBA", 'DXsimplified'] = "LRRK2_PD"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "Genetic : LRRK2 + GBA not Prodromal", 'DXsimplified'] = "LRRK2_PD"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "Genetic : LRRK2 + GBA Prodromal", 'DXsimplified'] = "LRRK2_Pro"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "Genetic : LRRK2 not Prodromal", 'DXsimplified'] = "LRRK2_PD"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "Genetic : LRRK2 Phenoconverted", 'DXsimplified'] = "LRRK2_Pro"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] ==  "Genetic : LRRK2 Prodromal", 'DXsimplified'] = "LRRK2_Pro"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] ==  "Genetic : SNCA", 'DXsimplified'] = "SNCA_PD"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "Genetic : SNCA Prodromal", 'DXsimplified'] = "SNCA_Pro"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "Hyposmia" , 'DXsimplified'] = "Sporadic_Pro"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "Hyposmia : Phenoconverted", 'DXsimplified'] = "Sporadic_Pro"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "No Mutation not Prodromal", 'DXsimplified'] = np.NaN
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "non-HC", 'DXsimplified'] = np.NaN
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "non-PD", 'DXsimplified'] = "nonPDorMSA"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "RBD", 'DXsimplified'] = "Sporadic_Pro"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] == "RBD : Phenoconverted", 'DXsimplified'] = "Sporadic_Pro"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] ==  "RBD : Phenoconverted with GBA", 'DXsimplified'] = "GBA_Pro"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] ==  "Sporadic", 'DXsimplified'] = "Sporadic_PD"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] ==  "SWEDD/non-PD Active", 'DXsimplified'] = "nonPDorMSA"
    ppmi_merge.loc[ppmi_merge['Consensus.Subtype'] ==  "SWEDD/PD Active", 'DXsimplified'] = np.NaN
    return ppmi_merge



def add_min_PD_duration(ppmi_merge) :
    ## Add in min PD Disease duration
    # Create a simplified diagnosis group of just HC, PD, Prodromal, or nonPDorMSA
    ppmi_merge['DXs2'] = ''
    ppmi_merge['DXsimplified'].fillna('NA', inplace = True)
    ppmi_merge.loc[ppmi_merge['DXsimplified'].str.contains('HC'), 'DXs2'] = 'HC'
    ppmi_merge.loc[ppmi_merge['DXsimplified'].str.contains('_PD'), 'DXs2'] = 'PD'
    ppmi_merge.loc[ppmi_merge['DXsimplified'].str.contains('_Pro'), 'DXs2'] = 'Pro'
    ppmi_merge.loc[ppmi_merge['DXsimplified'].str.contains('nonPDorMSA'), 'DXs2'] = 'nonPDorMSA'

    # If HC, Prodromal or nonPDorMSA - fill in with 0 for PD.Min.Disease.Duration
    ppmi_merge.loc[ppmi_merge['DXs2'] == 'HC', 'PD.Min.Disease.Duration'] = 0
    ppmi_merge.loc[ppmi_merge['DXs2'] == 'Pro', 'PD.Min.Disease.Duration'] = 0
    ppmi_merge.loc[ppmi_merge['DXs2'] == 'nonPDorMSA', 'PD.Min.Disease.Duration'] = 0

    # For PD subjects, fill in PD.Min.Disease.Duration
    ppmi_merge['PD.Diagnosis.Duration'].fillna('', inplace = True)
    subids = ppmi_merge['Subject.ID'].unique() # Unique subject ids
    for subid in subids :
        df = ppmi_merge[(ppmi_merge['Subject.ID'] == subid) & (ppmi_merge['DXs2'] == 'PD') & (ppmi_merge['PD.Diagnosis.Duration'] != '')]
        if len(df) > 0 :
            print(df['PD.Diagnosis.Duration'])
            mydd = min(df['PD.Diagnosis.Duration'])
            ppmi_merge.loc[ppmi_merge['Subject.ID'] == subid, 'PD.Min.Disease.Duration'] = mydd
    return ppmi_merge



def add_Visit(ppmi_merge) :
    ## Add in Visit column
    ppmi_merge['Visit'] = np.NaN # Initialize Visit col
    searchfor = ['Baseline', 'Visit Month '] # Strings to search for
    temp = ppmi_merge['Event.ID'].str.contains('|'.join(searchfor)) # locations of where row contains str: baseline or visit month
    ppmi_merge['Visit'].loc[temp == True] = ppmi_merge['Event.ID'].loc[temp == True] # Fill in 'Visit' col with event.ID for baseline or visit month
    ppmi_merge['Visit'] = ppmi_merge['Visit'].str.replace("Remote Visit Month ", "") # Replace Remote visit month with '' (want only month number)
    ppmi_merge['Visit'] = ppmi_merge['Visit'].str.replace("Visit Month ", "") # Replace Visit month with '' (want only month number)
    ppmi_merge['Visit'] = ppmi_merge['Visit'].str.replace("Baseline", "0") # Replace baseline with 0
    ppmi_merge['Visit'] = ppmi_merge['Visit'].fillna(9999) # Filling with 9999 so we can change this col to int
    ppmi_merge['Visit'] = ppmi_merge['Visit'].astype(int) # str to int
    ppmi_merge['Visit'] = ppmi_merge['Visit'].replace(9999, np.nan)  # Replace 9999 with nan
    return ppmi_merge

               

def add_diagnosis_change(full_df, ppmi_merge) :
    ## Add diagnosis change info on event id
    diag_vis1 = condensed_df(full_df, ['PATNO', 'DIAG1', 'DIAG1VIS'], {'DIAG1VIS' : 'EVENT_ID'}, ['EVENT_ID'])
    diag_vis2 = condensed_df(full_df, ['PATNO', 'DIAG2', 'DIAG2VIS'], {'DIAG2VIS' : 'EVENT_ID'},['EVENT_ID'])
    ppmi_merge.drop(['DIAG1', 'DIAG1VIS', 'DIAG2', 'DIAG2VIS'], axis = 1, inplace = True) # Drop these from ppmi_merge so there aren't duplicates when we merge the diag_vis dfs
    ppmi_merge = pd.merge(diag_vis1, ppmi_merge, on = ['EVENT_ID', 'PATNO'], how = "outer" ) # Merge in first diagnosis change
    ppmi_merge = pd.merge(diag_vis2, ppmi_merge, on = ['EVENT_ID', 'PATNO'], how = "outer" ) # Merge in second diagnosis change
    ppmi_merge['DIAG1'].replace({ 'PD' : 'Parkinson\'s Disease', 'DLB': 'Dimentia with Lewy Bodies'}, inplace = True) # Decode
    ppmi_merge['DIAG2'].replace({ 'MSA' : 'Multiple System Atrophy', 'DLB': 'Dimentia with Lewy Bodies'}, inplace = True) # Decode
    ppmi_merge.rename(columns = {'DIAG1' : 'First.Diagnosis.Change', 'DIAG2' : 'Second.Diagnosis.Change'}, inplace = True) # Rename columns
    return ppmi_merge



def get_full_ImageAcquisitionDate(ppmi_merge) :
    # Put full date in Image.Acquisition.Date column
    for row_num in range(len(ppmi_merge['T1.s3.Image.Name'])) :
        if isinstance(ppmi_merge['T1.s3.Image.Name'].iloc[row_num],str) :
            date = ppmi_merge['T1.s3.Image.Name'].iloc[row_num].split('-')[2]
            ppmi_merge['Image.Acquisition.Date'].iloc[row_num] = date[4:6] + '/' + date[6:8] +'/' + date[0:4]
    return ppmi_merge



def combine_lateralized_subscores(ppmi_merge : pd.DataFrame, new_lateralized_col_name : str, right_subscore_name : str, left_subscore_name : str, sym_subscore_name : str) :
    ppmi_merge[new_lateralized_col_name] = ppmi_merge.pop(right_subscore_name).fillna(ppmi_merge.pop(left_subscore_name))
    ppmi_merge[new_lateralized_col_name] = ppmi_merge.pop(new_lateralized_col_name).fillna(ppmi_merge.pop(sym_subscore_name))
    return ppmi_merge



def add_snp_recode(genetics_path : str, ppmi_merge : pd.DataFrame) :
    ## Add in Brian's snp_rs6265_recode.csv file sent on slack 6/29/22
    snp_recode = read_csv_drop_cols(genetics_path, 'snp_rs6265_recode.csv',['CHR', 'POS', 'COUNTED', 'ALT', 'SNP', '(C)M'], drop = True)

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
    ppmi_merge = pd.merge(ppmi_merge, snp_recode, on = ['Subject.ID'], how = "outer")
    return ppmi_merge



def add_t1_mergewide(ppmi_merge, invicro_data) :
    #### T1 Info - Taylor's File ####
    ppmi_t1_df = pd.read_csv(invicro_data + 'ppmi_mergewide_t1.csv') # Read in Taylor's T1 results file
    ppmi_t1_df.rename(columns = {'u_hier_id_OR': 'Subject.ID'}, inplace = True) # Rename subject id column in Taylors df to match ppmi_merge

    # Create a column for object name to merge on with ppmi_merge
    ppmi_t1_df['Image_ID_merge'] = ''
    for row_num in range(len(ppmi_t1_df['ImageID'])) :
        image_id = ppmi_t1_df['ImageID'].iloc[row_num].split('-')[2]
        ppmi_t1_df['Image_ID_merge'].iloc[row_num] = image_id

    # Merge ppmi_merge_genetics  with t1 info
    ppmi_merge['Subject.ID'] = ppmi_merge['Subject.ID'].astype(float)
    ppmi_t1_df['Subject.ID'] = ppmi_t1_df['Subject.ID'].astype(float)
    ppmi_merge['Image_ID_merge'] = ppmi_merge['Image_ID_merge'].astype(str)
    ppmi_t1_df['Image_ID_merge'] = ppmi_t1_df['Image_ID_merge'].astype(str)
    ppmi_merge = pd.merge(ppmi_merge, ppmi_t1_df, on = ['Subject.ID','Image_ID_merge'], how = "left") # Merge
    ppmi_merge.drop(['Image_ID_merge'], axis = 1, inplace = True) # Drop
    return ppmi_merge



def merge_multiple_dfs(df_list, on, how):
    df0 = df_list[0] # first df
    df1 = df_list[1] # second df
    merged_df = pd.merge(df0, df1, on = on, how = how) # merge first and second df
    num_dfs = len(df_list) # get total number of dfs in df_list
    for i in range(2, num_dfs) :
        merged_df = pd.merge(merged_df, df_list[i], on = on , how = how) # merge the rest of dfs into merged_df
    return merged_df
        


def change_genetics_int_2_float(genetics_df): 
    for col_name in genetics_df :
        if col_name.startswith('CHR'):
            genetics_df[col_name] = genetics_df[col_name].fillna(-9999.0)
            genetics_df[col_name] = genetics_df[col_name].astype(int)
    genetics_df.replace({-9999.0 : 'NA'}, inplace = True)
    return genetics_df
    
    

if __name__=="__main__":
    main()
              