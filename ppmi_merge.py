import pandas as pd
import numpy as np
from datetime import datetime
from dateutil import relativedelta
import re
from typing import List
import glob


# Set up paths
userdir = '/Users/areardon/Desktop/Projects/PPMI_Merge3_20230920/'
ppmi_download_path = '/Users/areardon/Desktop/Projects/PPMI_Merge3_20230920/PPMI_Study_Downloads_20230920/'
date = '20Sep2023'
version = 'v0.1.1'
code_list = pd.read_csv(glob.glob(ppmi_download_path + 'Code_List*Annotated__*.csv')[0])  
    
    
def main() :
    cohort_df = create_cohort()
    ppmi_merge = merge_clinical_files(cohort_df)
    ppmi_merge = merge_updrs_files(ppmi_merge)
    ppmi_merge = cleanup(ppmi_merge)
    


def create_cohort() : 
    excel_file = pd.ExcelFile(glob.glob(ppmi_download_path + '*Consensus_Committee_Analytic_Datasets*.xlsx')[0]) # Read in main xlsx file
    cohort_df = create_cohort_df(excel_file) 
    cohort_df = decode(cohort_df, 'PATIENT_STATUS', ['PHENOCNV'],rename_cols = {'Cohort' : 'Enroll.Diagnosis' , 'PHENOCNV' : 'Subject.Phenoconverted'})
    return cohort_df 


 
def merge_clinical_files(cohort_df) : 
    ppmi_merge = merge_and_transform_data('Age_at_visit_' + date + '.csv', list_cols = ['PATNO', 'EVENT_ID', 'AGE_AT_VISIT'], rename_list = {'AGE_AT_VISIT' : 'Age'}, merge_on = ['PATNO'], merge_how = "outer", df=cohort_df)    
    ppmi_merge = merge_and_transform_data('Demographics_' + date + '.csv', list_cols = ['PATNO','EVENT_ID','SEX', 'HANDED', 'BIRTHDT','AFICBERB','ASHKJEW','BASQUE', 'HISPLAT', 'RAASIAN', 'RABLACK', 'RAHAWOPI', 'RAINDALS', 'RANOS', 'RAWHITE'], rename_list = {'SEX' : 'Sex', 'HANDED' : 'Handed', 'BIRTHDT' : 'BirthDate',  'AFICBERB' : 'African.Berber.Race','ASHKJEW':'Ashkenazi.Jewish.Race', 'BASQUE' : 'Basque.Race', 'HISPLAT' : 'Hispanic.Latino.Race', 'RAASIAN' : 'Asian.Race', 'RABLACK' : 'African.American.Race', 'RAHAWOPI' : 'Hawian.Other.Pacific.Islander.Race', 'RAINDALS' : 'Indian.Alaska.Native.Race', 'RANOS' : 'Not.Specified.Race', 'RAWHITE': 'White.Race'},mod_name = 'SCREEN', decode_list = ['SEX', 'HANDED','AFICBERB','ASHKJEW','BASQUE', 'HISPLAT', 'RAASIAN', 'RABLACK', 'RAHAWOPI', 'RAINDALS', 'RANOS', 'RAWHITE'], df = ppmi_merge)
    ppmi_merge = merge_and_transform_data('Vital_Signs_' + date + '.csv', list_cols = ['PATNO','EVENT_ID','INFODT', 'WGTKG', 'HTCM', 'SYSSUP', 'DIASUP', 'SYSSTND', 'DIASTND'], rename_list = {'SEX' : 'Sex', 'HANDED' : 'Handed', 'BIRTHDT' : 'BirthDate', 'WGTKG' : 'Weight(kg)', 'HTCM' : 'Height(cm)','SYSSUP':'Systolic.BP.Sitting', 'DIASUP' : 'Diastolic.BP.Sitting', 'SYSSTND' : 'Systolic.BP.Standing' , 'DIASTND': 'Diastolic.BP.Standing'}, df = ppmi_merge)
    ppmi_merge = merge_and_transform_data('PD_Diagnosis_History_' + date + '.csv', list_cols = ['PATNO', 'EVENT_ID', 'SXDT','PDDXDT'], rename_list = { 'SXDT' : 'First.Symptom.Date', 'PDDXDT': 'PD.Diagnosis.Date'}, df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('SCOPA-AUT_' + date + '.csv', list_cols = ['PATNO', 'EVENT_ID', 'SCAU8', 'SCAU9', 'SCAU15', 'SCAU16'], df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Modified_Schwab___England_Activities_of_Daily_Living_' + date + '.csv', list_cols = ['PATNO', 'EVENT_ID','MSEADLG'], df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Conclusion_of_Study_Participation_' + date + '.csv', list_cols =['PATNO', 'EVENT_ID', 'COMPLT', 'WDRSN', 'WDDT'], rename_list = {'COMPLT' : 'Completed.Study' , 'WDRSN': 'Reason.for.Withdrawal','WDDT' : 'Withdrawal.Date'}, df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('PPMI_Original_Cohort_BL_to_Year_5_Dataset_Apr2020.csv', list_cols = ['PATNO', 'EVENT_ID', 'DOMSIDE'], mod_name = 'PDDXHIST', decode_list = ['DOMSIDE'], rename_list = {'DOMSIDE' : 'Dominant.Side.Disease'}, df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Participant_Motor_Function_Questionnaire_' + date + '.csv', list_cols =['PATNO', 'EVENT_ID', 'PAG_NAME', 'CMPLBY2', 'TRBUPCHR', 'WRTSMLR', 'VOICSFTR', 'POORBAL', 'FTSTUCK', 'LSSXPRSS', 'ARMLGSHK', 'TRBBUTTN', 'SHUFFLE', 'MVSLOW', 'TOLDPD'], mod_name = 'PQUEST', decode_list =  ['CMPLBY2', 'PAG_NAME','TRBUPCHR', 'WRTSMLR', 'VOICSFTR', 'POORBAL', 'FTSTUCK', 'LSSXPRSS', 'ARMLGSHK', 'TRBBUTTN', 'SHUFFLE', 'MVSLOW', 'TOLDPD'],rename_list = {'PAG_NAME' : 'Motor.Function.Page.Name', 'CMPLBY2' : 'Motor.Function.Source', 'TRBUPCHR' : 'Trouble.Rising.Chair', 'WRTSMLR' : 'Writing.Smaller', 'VOICSFTR' : 'Voice.Softer' , 'POORBAL': 'Poor.Balance' , 'FTSTUCK' : 'Feet.Stuck', 'LSSXPRSS' : 'Less.Expressive' , 'ARMLGSHK':'Arms/Legs.Shake', 'TRBBUTTN' : 'Trouble.Buttons' , 'SHUFFLE' : 'Shuffle.Feet' , 'MVSLOW' : 'Slow.Movements' , 'TOLDPD' : 'Been.Told.PD'}, df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Cognitive_Categorization_' + date + '.csv', list_cols =  ['PATNO' , 'EVENT_ID', 'PAG_NAME', 'COGDECLN', 'FNCDTCOG' , 'COGDXCL' ,'PTCGBOTH' , 'COGSTATE' , 'COGCAT_TEXT'], mod_name = 'COGCATG', decode_list = ['PAG_NAME', 'COGDECLN', 'FNCDTCOG' , 'COGDXCL' ,'PTCGBOTH' , 'COGSTATE' , 'COGCAT_TEXT'], rename_list = {'PAG_NAME' : 'Cognitive.Page.Name', 'COGDECLN' : 'Cognitive.Decline', 'FNCDTCOG' : 'Functional.Cognitive.Impairment', 'COGDXCL' : 'Confidence.Level.Cognitive.Diagnosis', 'PTCGBOTH' : 'Cognitive.Source', 'COGSTATE' : 'Cognitive.State' , 'COGCAT_TEXT' : 'Cognitive.Tscore.Cat'}, df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Montreal_Cognitive_Assessment__MoCA__' + date + '.csv',  list_cols =  ['PATNO', 'EVENT_ID', 'MCATOT'], rename_list = {'MCATOT' : 'MOCA.Total'}, df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Socio-Economics_' + date + '.csv', list_cols =['PATNO', 'EDUCYRS'], merge_on = ['PATNO'], merge_how = "outer", rename_list = {'EDUCYRS' : 'Education.Years'}, df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Modified_Boston_Naming_Test_' + date + '.csv', list_cols = ['PATNO', 'EVENT_ID', 'MBSTNSCR', 'MBSTNCRC', 'MBSTNCRR'], df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Clock_Drawing_' + date + '.csv', list_cols = ['PATNO', 'EVENT_ID', 'CLCKTOT'], df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Benton_Judgement_of_Line_Orientation_' + date + '.csv', list_cols = ['PATNO', 'EVENT_ID', 'JLO_TOTCALC','JLO_TOTRAW'], df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Letter_-_Number_Sequencing_' + date + '.csv', list_cols =  ['PATNO', 'EVENT_ID', 'LNS_TOTRAW'], df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Modified_Semantic_Fluency_' + date + '.csv', list_cols = ['PATNO', 'EVENT_ID', 'DVS_SFTANIM', 'DVT_SFTANIM'], df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Hopkins_Verbal_Learning_Test_-_Revised_' + date + '.csv', list_cols = ['PATNO', 'EVENT_ID', 'DVT_DELAYED_RECALL', 'DVT_TOTAL_RECALL','DVT_RECOG_DISC_INDEX','DVT_RETENTION'], df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('Symbol_Digit_Modalities_Test_' + date + '.csv', list_cols = ['PATNO', 'EVENT_ID', 'SDMTOTAL'], rename_list = {'CLCKTOT' : 'Clock.Drawing.Total', 'JLOTOTCALC' : 'JOLO.Total', 'LNS_TOTRAW' : 'Letter.Number.Sequencing.Total','DVS_SFTANIM' : 'Semantic.Fluency.Scaled.Score', 'DVT_SFTANIM' :'Sematnic.Fluency.TScore', 'DVT_TOTAL_RECALL' : 'DVT.Total.RECALL','SDMTOTAL' : 'Symbol.Digit.Modalities.Total'}, df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('REM_Sleep_Behavior_Disorder_Questionnaire_' + date + '.csv', list_cols =   ['PATNO', 'EVENT_ID', 'PAG_NAME', 'PTCGBOTH', 'DRMVIVID', 'DRMAGRAC', 'DRMNOCTB', 'SLPLMBMV', 'SLPINJUR', 'DRMVERBL', 'DRMFIGHT', 'DRMUMV', 'DRMOBJFL', 'MVAWAKEN',    'DRMREMEM',    'SLPDSTRB',    'STROKE', 'HETRA', 'PARKISM', 'RLS', 'NARCLPSY', 'DEPRS', 'EPILEPSY', 'BRNINFM', 'CNSOTH'], rename_list = {'PAG_NAME' : 'REM.Page.Name'}, mod_name = 'REMSLEEP', decode_list = ['PAG_NAME','DRMVIVID',    'DRMAGRAC',    'DRMNOCTB',    'SLPLMBMV',    'SLPINJUR',    'DRMVERBL',    'DRMFIGHT',    'DRMUMV',    'DRMOBJFL',    'MVAWAKEN',    'DRMREMEM',    'SLPDSTRB',    'STROKE',    'HETRA',    'PARKISM',    'RLS','NARCLPSY',    'DEPRS',    'EPILEPSY',    'BRNINFM',    'CNSOTH' ], df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('DaTScan_Analysis_' + date + '.csv', list_cols =  ['PATNO','EVENT_ID','DATSCAN_DATE','DATSCAN_CAUDATE_R','DATSCAN_CAUDATE_L','DATSCAN_PUTAMEN_R','DATSCAN_PUTAMEN_L','DATSCAN_ANALYZED','DATSCAN_NOT_ANALYZED_REASON'], df= ppmi_merge)
    ppmi_merge = merge_and_transform_data('DaTScan_Imaging_' + date + '.csv', list_cols = ['PATNO','EVENT_ID','DATSCAN','INFODT', 'PREVDATDT','SCNLOC','SCNINJCT','VSINTRPT','VSRPTELG'], mod_name = 'DATSCAN', decode_list =['DATSCAN', 'SCNLOC','SCNINJCT', 'VSINTRPT','VSRPTELG'], rename_list = {'INFODT_x' : 'INFODT', 'INFODT_y' : 'DaTScan.INFODT', 'SCNLOC' : 'Location.Scan.Completed' , 'PREVDATDT' : 'Date.DaTscan.Imaging.Completed.Previously', 'SCNINJCT' : 'Scan.Injection', 'VSINTRPT' : 'Visual.Interpretation.Report', 'VSRPTELG' : 'Visual.Interpretation.Report(eligible/not)'}, df= ppmi_merge)   
    ppmi_merge['INFODT'].fillna(ppmi_merge['DaTScan.INFODT'], inplace = True) # Fill in NaN infodts with datscan infodts if NA
    ppmi_merge = remove_duplicate_datscans(ppmi_merge) # FIXME - After merging in datscan files, duplicate event ids being created one with DATSCAN as "Completed" one with DATSCAN as "not completed" - if there are both of these - keep only "Completed"
    ppmi_merge = add_diagnosis_change(cohort_df, ppmi_merge)
    ppmi_merge = add_concomitant_med_log(ppmi_merge)
    ppmi_merge = add_LEDD(ppmi_merge)
    ppmi_merge = make_categorical_LEDD_col(ppmi_merge, 'LEDD.sum', 'LEDD.sum.Cat', 3)
    ppmi_merge = make_categorical_LEDD_col(ppmi_merge, 'LEDD.ongoing.sum', 'LEDD.ongoing.sum.Cat',3)
    ppmi_merge = add_comorbidities(ppmi_merge)
    ppmi_merge['RBDTotal.REM'] = ppmi_merge[['DRMVIVID',    'DRMAGRAC',    'DRMNOCTB',    'SLPLMBMV',    'SLPINJUR',    'DRMVERBL',    'DRMFIGHT',    'DRMUMV',    'DRMOBJFL',    'MVAWAKEN',    'DRMREMEM',    'SLPDSTRB',    'STROKE',    'HETRA',    'PARKISM',    'RLS','NARCLPSY',    'DEPRS',    'EPILEPSY',    'BRNINFM',    'CNSOTH']].sum(axis = 1) # Add an RBDTotal.REM column
    ppmi_merge = add_mri_csv(ppmi_merge)
    ppmi_merge = get_enrollment_dx_nonanalytic(ppmi_merge, cohort_df) 
    ppmi_merge = add_DXsimplified(ppmi_merge)
    ppmi_merge = add_PD_Disease_Duration(ppmi_merge)
    return ppmi_merge



def merge_updrs_files(ppmi_merge):
    updrs_part1 = merge_and_transform_data('MDS-UPDRS_Part_I_' + date + '.csv', list_cols= ['ORIG_ENTRY','LAST_UPDATE','REC_ID'], list_cols_drop = True, rename_list= {'PAG_NAME' : 'Page.Name.UPDRS1', 'NUPSOURC' : 'NUPSOURC.UPDRS1'}, mod_name='NUPDRS1', decode_list= ['PAG_NAME', 'NUPSOURC'],ext_name = '.UPDRS1', ext_drop = ['PATNO','EVENT_ID','PAG_NAME','INFODT','NUPSOURC'])
    updrs_part1_pq = merge_and_transform_data('MDS-UPDRS_Part_I_Patient_Questionnaire_' + date + '.csv', list_cols= ['ORIG_ENTRY','LAST_UPDATE','REC_ID','INFODT'], list_cols_drop = True, rename_list= {'PAG_NAME' : 'Page.Name.UPDRS1PQ','NUPSOURC' : 'NUPSOURC.UPDRS1PQ'},  mod_name='NUPDRS1P', decode_list= ['PAG_NAME', 'NUPSOURC'], df = updrs_part1, ext_name = '.UPDRS1PQ', ext_drop = ['PATNO','EVENT_ID','INFODT','PAG_NAME', 'NUPSOURC'])
    updrs_part2 = merge_and_transform_data('MDS_UPDRS_Part_II__Patient_Questionnaire_' + date + '.csv', list_cols= ['ORIG_ENTRY','LAST_UPDATE','REC_ID','INFODT'], list_cols_drop = True, rename_list= {'PAG_NAME' : 'Page.Name.UPDRS2', 'NUPSOURC' : 'NUPSOURC.UPDRS2'},  mod_name='NUPDRS2P', decode_list= ['PAG_NAME', 'NUPSOURC'], df = updrs_part1_pq, ext_name = '.UPDRS2', ext_drop = ['PATNO','EVENT_ID','INFODT', 'PAG_NAME','NUPSOURC'])
    updrs_part3 = merge_and_transform_data('MDS-UPDRS_Part_III_' + date + '.csv', list_cols= ['ORIG_ENTRY','LAST_UPDATE','REC_ID','INFODT'], list_cols_drop = True, rename_list= {'PAG_NAME' : 'Page.Name.UPDRS3'},  mod_name='NUPDRS3TRT', decode_list= ['PAG_NAME'], df = updrs_part2, ext_name = '.UPDRS3',ext_drop = ['PATNO','EVENT_ID','INFODT','PAG_NAME'])
    updrs_temp = merge_and_transform_data('MDS-UPDRS_Part_IV__Motor_Complications_' + date + '.csv', list_cols= ['ORIG_ENTRY','LAST_UPDATE','REC_ID','INFODT'], list_cols_drop = True, rename_list= {'PAG_NAME' : 'Page.Name.UPDRS4'}, mod_name='NUPDRS4', decode_list= ['PAG_NAME'], df = updrs_part3, ext_name = '.UPDRS4', ext_drop = ['PATNO','EVENT_ID','INFODT','PAG_NAME'])
    updrs_cat = updrs_temp.copy()
    updrs_numeric = format_updrs(updrs_temp)
    updrs_numeric.rename(columns = {'NHY.UPDRS3' : 'Hoehn.and.Yahr.Stage.UPDRS3', 'NP3BRADY.UPDRS3' : 'Global.Spontaneity.of.Movement.UPDRS3', 'NP3PTRMR.UPDRS3' : 'Postural.Tremor.Right.Hand.UPDRS3' , 'NP3PTRML.UPDRS3' : 'Postural.Tremor.Left.Hand.UPDRS3' , 'NP3KTRMR.UPDRS3' : 'Kinetic.Tremor.Right.Hand.UPDRS3', 'NP3KTRML.UPDRS3' : 'Kinetic.Tremor.Left.Hand.UPDRS3', 'NP3RTARU.UPDRS3' : 'Rest.Tremor.Amplitude.RUE.UPDRS3', 'NP3RTALU.UPDRS3' : 'Rest.Tremor.Amplitude.LUE.UPDRS3', 'NP3RTARL.UPDRS3' : 'Rest.Tremor.Amplitude.RLE.UPDRS3' ,'NP3RTALL.UPDRS3' : 'Rest.Tremor.Amplitude.LLE.UPDRS3' ,'NP3RTALJ.UPDRS3' : 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS3', 'NP3RTCON.UPDRS3' : 'Constancy.of.Rest.Tremor.UPDRS3', 'NP3SPCH.UPDRS3' : 'Speech.Difficulty.UPDRS3', 'NP3FACXP.UPDRS3' : 'Facial.Expression.Difficulty.UPDRS3' , 'NP3RIGN.UPDRS3' : 'Rigidity.Neck.UPDRS3' , 'NP3RIGRU.UPDRS3' : 'Rigidity.RUE.UPDRS3', 'NP3RIGLU.UPDRS3' : 'Rigidity.LUE.UPDRS3', 'NP3RIGRL.UPDRS3' : 'Rigidity.RLE.UPDRS3', 'NP3RIGLL.UPDRS3' : 'Rigidity.LLE.UPDRS3', 'NP3FTAPR.UPDRS3' : 'Finger.Tapping.Right.Hand.UPDRS3' ,'NP3FTAPL.UPDRS3' : 'Finger.Tapping.Left.Hand.UPDRS3' ,'NP3HMOVR.UPDRS3' : 'Hand.Movements.Right.Hand.UPDRS3', 'NP3HMOVL.UPDRS3' : 'Hand.Movements.Left.Hand.UPDRS3', 'NP3PRSPR.UPDRS3' : 'Pronation.Supination.Right.Hand.UPDRS3', 'NP3PRSPL.UPDRS3' : 'Pronation.Supination.Left.Hand.UPDRS3' , 'NP3TTAPR.UPDRS3' : 'Toe.Tapping.Right.Foot.UPDRS3' , 'NP3TTAPL.UPDRS3' : 'Toe.Tapping.Left.Foot.UPDRS3', 'NP3LGAGR.UPDRS3' : 'Leg.Agility.Right.Leg.UPDRS3', 'NP3LGAGL.UPDRS3' : 'Leg.Agility.Left.Leg.UPDRS3', 'NP3RISNG.UPDRS3' : 'Rising.from.Chair.UPDRS3', 'NP3GAIT.UPDRS3' : 'Gait.Problems.UPDRS3' ,'NP3FRZGT.UPDRS3' : 'Freezing.of.Gait.UPDRS3' ,'NP3PSTBL.UPDRS3' : 'Postural.Stability.Problems.UPDRS3', 'NP3POSTR.UPDRS3' : 'Posture.Problems.UPDRS3' , 'NP3TOT.UPDRS3':'Total.UPDRS3','NP1COG.UPDRS1' : 'Cognitive.Impairment.UPDRS1', 'NP1HALL.UPDRS1' : 'Hallucinations.and.Psychosis.UPDRS1', 'NP1DPRS.UPDRS1' : 'Depressed.Moods.UPDRS1', 'NP1ANXS.UPDRS1' : 'Anxious.Moods.UPDRS1', 'NP1APAT.UPDRS1' : 'Apathy.UPDRS1', 'NP1DDS.UPDRS1' : 'Features.of.Dopamine.Dysregulation.Syndrome.UPDRS1', 'NP1RTOT.UPDRS1' : 'Rater.Completed.Total.UPDRS1','NP1SLPN.UPDRS1' : 'Sleep.Problems.Night.UPDRS1', 'NP1SLPD.UPDRS1' : 'Daytime.Sleepiness.UPDRS1', 'NP1PAIN.UPDRS1' : 'Pain.UPDRS1' , 'NP1URIN.UPDRS1' : 'Urinary.Problems.UPDRS1', 'NP1CNST.UPDRS1' : 'Constipation.Problems.UPDRS1' , 'NP1LTHD.UPDRS1' : 'Lightheadedness.on.Standing.UPDRS1' , 'NP1FATG.UPDRS1' : 'Fatigue.UPDRS1', 'NP1PTOT.UPDRS1' : 'Patient.Completed.Total.UPDRS1','NP2SPCH.UPDRS2' : 'Speech.Difficulty.UPDRS2' , 'NP2SALV.UPDRS2' : 'Saliva.Drooling.UPDRS2' ,'NP2SWAL.UPDRS2': 'Chewing.Swallowing.Difficulty.UPDRS2', 'NP2EAT.UPDRS2' : 'Eating.Difficulty.UPDRS2', 'NP2DRES.UPDRS2' : 'Dressing.Difficulty.UPDRS2', 'NP2HYGN.UPDRS2' : 'Hygiene.Difficulty.UPDRS2' , 'NP2HWRT.UPDRS2' : 'Handwriting.Difficulty.UPDRS2' ,'NP2HOBB.UPDRS2' : 'Hobbies.Difficulty.UPDRS2' ,'NP2TURN.UPDRS2' : 'Turning.in.Bed.Difficulty.UPDRS2', 'NP2TRMR.UPDRS2' : 'Tremor.UPDRS2', 'NP2RISE.UPDRS2' : 'Rising.from.Bed.Difficulty.UPDRS2', 'NP2WALK.UPDRS2' : 'Walking.Difficulty.UPDRS2' ,'NP2FREZ.UPDRS2' : 'Freezing.while.Walking.UPDRS2' , 'NP2PTOT.UPDRS2': 'Total.UPDRS2', 'NP4WDYSK.UPDRS4' : 'Time.Spent.with.Dyskinesias.UPDRS4', 'NP4DYSKI.UPDRS4':'Functional.Impact.of.Dyskinesias.UPDRS4','NP4OFF.UPDRS4' : 'Time.Spent.in.OFF.State.UPDRS4',     'NP4FLCTI.UPDRS4':'Functional.Impact.Fluctuations.UPDRS4',  'NP4FLCTX.UPDRS4':'Complexity.of.Motor.Fluctuations.UPDRS4' ,   'NP4DYSTN.UPDRS4':'Painful.OFF-state.Dystonia.UPDRS4' ,'NP4TOT.UPDRS4': 'Total.UPDRS4','NP4WDYSKDEN.UPDRS4':'Total.Hours.with.Dyskinesias.UPDRS4', 'NP4WDYSKNUM.UPDRS4' :'Total.Hours.Awake.Dysk.UPDRS4', 'NP4WDYSKPCT.UPDRS4' : 'Percent.Dyskinesia.UPDRS4','NP4OFFDEN.UPDRS4':'Total.Hours.OFF.UPDRS4', 'NP4OFFNUM.UPDRS4' : 'Total.Hours.Awake.OFF.UPDRS4','NP4OFFPCT.UPDRS4' : 'Percent.OFF.UPDRS4', 'NP4DYSTNDEN.UPDRS4' :'Total.Hours.OFF.with.Dystonia.UPDRS4',  'NP4DYSTNNUM.UPDRS4':'Total.Hours.OFF.Dyst.UPDRS4', 'NP4DYSTNPCT.UPDRS4':'Percent.OFF.Dystonia.UPDRS4', 'NP3BRADY.UPDRS4' : 'Global.Spontaneity.of.Movement.UPDRS4', 'NP3PTRMR.UPDRS4' : 'Postural.Tremor.Right.Hand.UPDRS4' , 'NP3PTRML.UPDRS4' : 'Postural.Tremor.Left.Hand.UPDRS4' , 'NP3KTRMR.UPDRS4' : 'Kinetic.Tremor.Right.Hand.UPDRS4', 'NP3KTRML.UPDRS4' : 'Kinetic.Tremor.Left.Hand.UPDRS4', 'NP3RTARU.UPDRS4' : 'Rest.Tremor.Amplitude.RUE.UPDRS4', 'NP3RTALU.UPDRS4' : 'Rest.Tremor.Amplitude.LUE.UPDRS4', 'NP3RTARL.UPDRS4' : 'Rest.Tremor.Amplitude.RLE.UPDRS4' ,'NP3RTALL.UPDRS4' : 'Rest.Tremor.Amplitude.LLE.UPDRS4' ,'NP3RTALJ.UPDRS4' : 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS4', 'NP3RTCON.UPDRS4' : 'Constancy.of.Rest.Tremor.UPDRS4'}, inplace = True)

    for column in updrs_cat.columns:
        if not column.startswith(('Page.Name', 'NUPSOURC')):
            updrs_cat.rename(columns={column: column.split('.UPDRS')[0]}, inplace=True)
    updrs_cat = decode(updrs_cat, 'NUPDRS1', ['NP1COG', 'NP1HALL', 'NP1DPRS', 'NP1ANXS', 'NP1APAT', 'NP1DDS'], rename_cols ={'NP1COG' : 'Cognitive.Impairment.UPDRS1', 'NP1HALL' : 'Hallucinations.and.Psychosis.UPDRS1', 'NP1DPRS' : 'Depressed.Moods.UPDRS1', 'NP1ANXS' : 'Anxious.Moods.UPDRS1', 'NP1APAT' : 'Apathy.UPDRS1', 'NP1DDS' : 'Features.of.Dopamine.Dysregulation.Syndrome.UPDRS1', 'NP1RTOT' : 'Rater.Completed.Total.UPDRS1'} )
    updrs_cat = decode(updrs_cat, 'NUPDRS1P', ['NP1SLPN', 'NP1SLPD', 'NP1PAIN', 'NP1URIN', 'NP1CNST', 'NP1LTHD', 'NP1FATG'], rename_cols = {'NP1SLPN' : 'Sleep.Problems.Night.UPDRS1', 'NP1SLPD' : 'Daytime.Sleepiness.UPDRS1', 'NP1PAIN' : 'Pain.UPDRS1' , 'NP1URIN' : 'Urinary.Problems.UPDRS1', 'NP1CNST' : 'Constipation.Problems.UPDRS1' , 'NP1LTHD' : 'Lightheadedness.on.Standing.UPDRS1' , 'NP1FATG' : 'Fatigue.UPDRS1', 'NP1PTOT' : 'Patient.Completed.Total.UPDRS1'})
    updrs_cat = decode(updrs_cat, 'NUPDRS2P', [ 'NP2SPCH','NP2SALV','NP2SWAL','NP2EAT','NP2DRES','NP2HYGN','NP2HWRT','NP2HOBB','NP2TURN','NP2TRMR','NP2RISE','NP2WALK','NP2FREZ'], rename_cols = {'NP2SPCH' : 'Speech.Difficulty.UPDRS2' , 'NP2SALV' : 'Saliva.Drooling.UPDRS2' ,'NP2SWAL': 'Chewing.Swallowing.Difficulty.UPDRS2', 'NP2EAT' : 'Eating.Difficulty.UPDRS2', 'NP2DRES' : 'Dressing.Difficulty.UPDRS2', 'NP2HYGN' : 'Hygiene.Difficulty.UPDRS2' , 'NP2HWRT' : 'Handwriting.Difficulty.UPDRS2' ,'NP2HOBB' : 'Hobbies.Difficulty.UPDRS2' ,'NP2TURN' : 'Turning.in.Bed.Difficulty.UPDRS2', 'NP2TRMR' : 'Tremor.UPDRS2', 'NP2RISE' : 'Rising.from.Bed.Difficulty.UPDRS2', 'NP2WALK' : 'Walking.Difficulty.UPDRS2' ,'NP2FREZ' : 'Freezing.while.Walking.UPDRS2' , 'NP2PTOT': 'Total.UPDRS2'})
    updrs_cat = decode(updrs_cat, 'NUPDRS3TRT',  ['DBSYN', 'OFFEXAM', 'ONEXAM', 'ONOFFORDER', 'ONNORSN', 'PDMEDYN', 'OFFNORSN','NP3SPCH', 'NP3FACXP', 'NP3RIGN', 'NP3RIGRU', 'NP3RIGLU', 'NP3RIGRL', 'NP3RIGLL', 'NP3FTAPR', 'NP3FTAPL', 'NP3HMOVR', 'NP3HMOVL', 'NP3PRSPR', 'NP3PRSPL', 'NP3TTAPR', 'NP3TTAPL', 'NP3LGAGR', 'NP3LGAGL', 'NP3RISNG', 'NP3GAIT', 'NP3FRZGT', 'NP3PSTBL', 'NP3POSTR', 'NP3BRADY', 'NP3PTRMR', 'NP3PTRML', 'NP3KTRMR', 'NP3KTRML', 'NP3RTARU', 'NP3RTALU', 'NP3RTARL', 'NP3RTALL', 'NP3RTALJ', 'NP3RTCON', 'DBSYN','DYSKPRES','DYSKIRAT','NHY','PDTRTMNT'], rename_cols = {'PDMEDYN': 'PDMEDYN.UPDRS3',	'DBSYN' : 'DBSYN.UPDRS3',  	'ONOFFORDER' : 'ONOFFORDER.UPDRS3',	'OFFEXAM' : 'OFFEXAM.UPDRS3',	'OFFNORSN':'OFFNORSN.UPDRS3', 'ONEXAM':'ONEXAM.UPDRS3',	'ONNORSN':'ONNORSN.UPDRS3', 'PDMEDDT': 'PDMEDDT.UPDRS3',	'PDMEDTM':'PDMEDTM.UPDRS3',	'EXAMDT': 'EXAMDT.UPDRS3', 'DBS_STATUS' : 'Deep.Brain.Stimulation.Treatment.UPDRS3' , 'NP3SPCH' : 'Speech.Difficulty.UPDRS3', 'NP3FACXP' : 'Facial.Expression.Difficulty.UPDRS3' , 'NP3RIGN' : 'Rigidity.Neck.UPDRS3' , 'NP3RIGRU' : 'Rigidity.RUE.UPDRS3', 'NP3RIGLU' : 'Rigidity.LUE.UPDRS3', 'NP3RIGRL' : 'Rigidity.RLE.UPDRS3', 'NP3RIGLL' : 'Rigidity.LLE.UPDRS3', 'NP3FTAPR' : 'Finger.Tapping.Right.Hand.UPDRS3' ,'NP3FTAPL' : 'Finger.Tapping.Left.Hand.UPDRS3' ,'NP3HMOVR' : 'Hand.Movements.Right.Hand.UPDRS3', 'NP3HMOVL' : 'Hand.Movements.Left.Hand.UPDRS3','NP3PRSPR' : 'Pronation.Supination.Right.Hand.UPDRS3', 'NP3PRSPL' : 'Pronation.Supination.Left.Hand.UPDRS3' , 'NP3TTAPR' : 'Toe.Tapping.Right.Foot.UPDRS3' , 'NP3TTAPL' : 'Toe.Tapping.Left.Foot.UPDRS3', 'NP3LGAGR' : 'Leg.Agility.Right.Leg.UPDRS3', 'NP3LGAGL' : 'Leg.Agility.Left.Leg.UPDRS3', 'NP3RISNG' : 'Rising.from.Chair.UPDRS3', 'NP3GAIT' : 'Gait.Problems.UPDRS3' ,'NP3FRZGT' : 'Freezing.of.Gait.UPDRS3' ,'NP3PSTBL' : 'Postural.Stability.Problems.UPDRS3', 'NP3POSTR' : 'Posture.Problems.UPDRS3' , 'NP3TOT':'Total.UPDRS3',  'Most.Recent.PD.Med.Dose.Date.Time.Before.OFF.Exam' : 'Most.Recent.PD.Med.Dose.Date.Time.Before.OFF.Exam.UPDRS3' ,'ONEXAMTM' : 'ON.Exam.Time.UPDRS3' , 'Most.Recent.PD.Med.Dose.Date.Time.Before.ON.Exam' :'Most.Recent.PD.Med.Dose.Date.Time.Before.ON.Exam.UPDRS3', 'DBSONTM' : 'Time.DBS.Turned.on.before.ON.Exam.UPDRS3', 'DBSOFFTM' : 'Time.DBS.Turned.off.before.OFF.Exam.UPDRS3', 'OFFEXAMTM' : 'OFF.Exam.Time.UPDRS3', 'HRPOSTMED' : 'Hours.btwn.PD.Med.and.UPDRS3.Exam.UPDRS3', 'HRDBSOFF' : 'Hours.btwn.DBS.Device.Off.and.UPDRS3.Exam.UPDRS3', 'HRDBSON' : 'Hours.btwn.DBS.Device.On.and.UPDRS3.Exam.UPDRS3' ,'DYSKPRES' : 'Dyskinesias.Present.UPDRS3', 'DYSKIRAT' : 'Movements.Interefered.with.Ratings.UPDRS3', 'NHY' : 'Hoehn.and.Yahr.Stage.UPDRS3', 'PDTRTMNT' : 'On.PD.Treatment.UPDRS3','NP3BRADY' : 'Global.Spontaneity.of.Movement.UPDRS3', 'NP3PTRMR' : 'Postural.Tremor.Right.Hand.UPDRS3' , 'NP3PTRML' : 'Postural.Tremor.Left.Hand.UPDRS3' , 'NP3KTRMR' : 'Kinetic.Tremor.Right.Hand.UPDRS3', 'NP3KTRML' : 'Kinetic.Tremor.Left.Hand.UPDRS3', 'NP3RTARU' : 'Rest.Tremor.Amplitude.RUE.UPDRS3', 'NP3RTALU' : 'Rest.Tremor.Amplitude.LUE.UPDRS3', 'NP3RTARL' : 'Rest.Tremor.Amplitude.RLE.UPDRS3' ,'NP3RTALL' : 'Rest.Tremor.Amplitude.LLE.UPDRS3' ,'NP3RTALJ' : 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS3', 'NP3RTCON' : 'Constancy.of.Rest.Tremor.UPDRS3', 'PDSTATE' : 'Functional.State.UPDRS3','EXAMTM' : 'Exam.Time.UPDRS3' })
    updrs_cat = decode(updrs_cat, 'NUPDRS4', ['NP4WDYSK','NP4DYSKI','NP4OFF','NP4FLCTI','NP4DYSTN','NP4FLCTX'],{'NP4WDYSKDEN':'Total.Hours.with.Dyskinesias.UPDRS4', 'NP4WDYSKNUM' :'Total.Hours.Awake.Dysk.UPDRS4', 'NP4WDYSKPCT' : 'Percent.Dyskinesia.UPDRS4','NP4OFFDEN':'Total.Hours.OFF.UPDRS4', 'NP4OFFNUM' : 'Total.Hours.Awake.OFF.UPDRS4','NP4OFFPCT' : 'Percent.OFF.UPDRS4', 'NP4DYSTNDEN' :'Total.Hours.OFF.with.Dystonia.UPDRS4',    'NP4DYSTNNUM':'Total.Hours.OFF.Dyst.UPDRS4', 'NP4DYSTNPCT':'Percent.OFF.Dystonia.UPDRS4', 'NP4WDYSK' : 'Time.Spent.with.Dyskinesias.UPDRS4', 'NP4DYSKI':'Functional.Impact.of.Dyskinesias.UPDRS4','NP4OFF' : 'Time.Spent.in.OFF.State.UPDRS4',     'NP4FLCTI':'Functional.Impact.Fluctuations.UPDRS4',    'NP4FLCTX':'Complexity.of.Motor.Fluctuations.UPDRS4' ,    'NP4DYSTN':'Painful.OFF-state.Dystonia.UPDRS4' ,'NP4TOT': 'Total.UPDRS4','NP4WDYSKDEN' : 'Total.Hours.with.Dyskinesia.UPDRS4', 'NP4WDYSKNUM' : 'Total.Hours.Awake.Dysk.UPDRS4', 'NP4WDYSKPCT' : 'Percent.Dyskinesia.UPDRS4',  'NP4OFFDEN' :'Total.Hours.OFF.UPDRS4' , 'NP4OFFNUM' :'Total.Hours.Awake.OFF.UPDRS4' , 'NP4OFFPCT': 'Percent.OFF.UPDRS4', 'NP4DYSTNDEN' : 'Total.Hours.OFF.with.Dystonia.UPDRS4', 'NP4DYSTNNUM' :'Total.Hours.OFF.Dyst.UPDRS4', 'NP4DYSTNPCT' : 'Percent.OFF.Dystonia.UPDRS4' })
    updrs_cat = add_extension_to_column_names(updrs_cat, ['PATNO', 'EVENT_ID','INFODT'], '.Cat') # Add a .Num extension to column names w updrs numeric vars

    # Subscores
    updrs_numeric = add_subscore(updrs_numeric,  ['Rigidity.Neck.UPDRS3',  'Rigidity.RUE.UPDRS3',  'Rigidity.LUE.UPDRS3',  'Rigidity.RLE.UPDRS3',  'Rigidity.LLE.UPDRS3', 'Finger.Tapping.Right.Hand.UPDRS3' , 'Finger.Tapping.Left.Hand.UPDRS3' , 'Hand.Movements.Right.Hand.UPDRS3','Hand.Movements.Left.Hand.UPDRS3','Pronation.Supination.Right.Hand.UPDRS3', 'Pronation.Supination.Left.Hand.UPDRS3',   'Toe.Tapping.Right.Foot.UPDRS3','Toe.Tapping.Left.Foot.UPDRS3','Leg.Agility.Right.Leg.UPDRS3', 'Leg.Agility.Left.Leg.UPDRS3'], 'Brady.Rigidity.Subscore.UPDRS3')
    updrs_numeric = add_subscore(updrs_numeric, ['Tremor.UPDRS2', 'Postural.Tremor.Right.Hand.UPDRS3' ,'Postural.Tremor.Left.Hand.UPDRS3' ,'Kinetic.Tremor.Right.Hand.UPDRS3','Kinetic.Tremor.Left.Hand.UPDRS3', 'Rest.Tremor.Amplitude.RUE.UPDRS3','Rest.Tremor.Amplitude.LUE.UPDRS3', 'Rest.Tremor.Amplitude.RLE.UPDRS3' , 'Rest.Tremor.Amplitude.LLE.UPDRS3' , 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS3', 'Constancy.of.Rest.Tremor.UPDRS3'], 'Tremor.Subscore.UPDRS3')
    updrs_numeric = add_subscore(updrs_numeric, ['Walking.Difficulty.UPDRS2' ,  'Freezing.while.Walking.UPDRS2' ,'Gait.Problems.UPDRS3'  , 'Freezing.of.Gait.UPDRS3' , 'Postural.Stability.Problems.UPDRS3'], 'PIGD.Subscore.UPDRS3')
    updrs_numeric = add_extension_to_column_names(updrs_numeric, ['PATNO', 'EVENT_ID', 'PIGD.Subscore.UPDRS3', 'Tremor.Subscore.UPDRS3', 'Brady.Rigidity.Subscore.UPDRS3'], '.Num') # Add a .Num extension to column names w updrs numeric vars

    # Create one df with UPDRS scores .Num (numeric) and all UPDRS scores .Cat (categorical)
    updrs_cat.drop(['INFODT','PATNO','EVENT_ID'], axis = 1, inplace = True)
    updrs_merged = pd.concat([updrs_cat, updrs_numeric], axis = 1)
    ppmi_merge = pd.merge(ppmi_merge, updrs_merged, on = ['PATNO', 'EVENT_ID'], how = "outer")

    ## Make any dominant side of disease that are NA into 'Symmetric' FIXME CHECK
    domsideisna = ppmi_merge['Dominant.Side.Disease'].isna()
    ppmi_merge['Dominant.Side.Disease'].loc[domsideisna] = 'Symmetric'
    ppmi_merge = add_subscore(ppmi_merge,  ['Dominant.Side.Disease', 'Rigidity.Neck.UPDRS3.Num', 'Rigidity.LUE.UPDRS3.Num', 'Rigidity.LLE.UPDRS3.Num', 'Finger.Tapping.Left.Hand.UPDRS3.Num', 'Hand.Movements.Left.Hand.UPDRS3.Num', 'Pronation.Supination.Left.Hand.UPDRS3.Num', 'Toe.Tapping.Left.Foot.UPDRS3.Num', 'Leg.Agility.Left.Leg.UPDRS3.Num'],  'Brady.Rigidity.Subscore-left.UPDRS3', 'Left')
    ppmi_merge = add_subscore(ppmi_merge, ['Dominant.Side.Disease', 'Rigidity.Neck.UPDRS3.Num', 'Rigidity.RUE.UPDRS3.Num', 'Rigidity.RLE.UPDRS3.Num', 'Finger.Tapping.Right.Hand.UPDRS3.Num', 'Hand.Movements.Right.Hand.UPDRS3.Num', 'Pronation.Supination.Right.Hand.UPDRS3.Num', 'Toe.Tapping.Right.Foot.UPDRS3.Num', 'Leg.Agility.Right.Leg.UPDRS3.Num'], 'Brady.Rigidity.Subscore-right.UPDRS3', 'Right')
    ppmi_merge = add_subscore(ppmi_merge, ['Dominant.Side.Disease', 'Rigidity.Neck.UPDRS3.Num', 'Rigidity.RUE.UPDRS3.Num', 'Rigidity.LUE.UPDRS3.Num', 'Rigidity.RLE.UPDRS3.Num', 'Rigidity.LLE.UPDRS3.Num', 'Finger.Tapping.Right.Hand.UPDRS3.Num', 'Finger.Tapping.Left.Hand.UPDRS3.Num', 'Hand.Movements.Right.Hand.UPDRS3.Num', 'Hand.Movements.Left.Hand.UPDRS3.Num', 'Pronation.Supination.Right.Hand.UPDRS3.Num', 'Pronation.Supination.Left.Hand.UPDRS3.Num', 'Toe.Tapping.Right.Foot.UPDRS3.Num', 'Toe.Tapping.Left.Foot.UPDRS3.Num', 'Leg.Agility.Right.Leg.UPDRS3.Num', 'Leg.Agility.Left.Leg.UPDRS3.Num'],'Brady.Rigidity.Subscore-sym.UPDRS3',  'Symmetric', '.UPDRS3.Num')
    ppmi_merge = add_subscore(ppmi_merge,  ['Dominant.Side.Disease', 'Tremor.UPDRS2.Num', 'Postural.Tremor.Left.Hand.UPDRS3.Num', 'Kinetic.Tremor.Left.Hand.UPDRS3.Num', 'Rest.Tremor.Amplitude.LUE.UPDRS3.Num', 'Rest.Tremor.Amplitude.LLE.UPDRS3.Num', 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS3.Num', 'Constancy.of.Rest.Tremor.UPDRS3.Num'], 'Tremor.Subscore-left.UPDRS3', 'Left')
    ppmi_merge = add_subscore(ppmi_merge,  ['Dominant.Side.Disease', 'Tremor.UPDRS2.Num', 'Postural.Tremor.Right.Hand.UPDRS3.Num', 'Kinetic.Tremor.Right.Hand.UPDRS3.Num', 'Rest.Tremor.Amplitude.RUE.UPDRS3.Num', 'Rest.Tremor.Amplitude.RLE.UPDRS3.Num', 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS3.Num', 'Constancy.of.Rest.Tremor.UPDRS3.Num'],  'Tremor.Subscore-right.UPDRS3', 'Right')
    ppmi_merge = add_subscore(ppmi_merge, ['Dominant.Side.Disease', 'Tremor.UPDRS2.Num', 'Postural.Tremor.Right.Hand.UPDRS3.Num', 'Postural.Tremor.Left.Hand.UPDRS3.Num', 'Kinetic.Tremor.Right.Hand.UPDRS3.Num', 'Kinetic.Tremor.Left.Hand.UPDRS3.Num', 'Rest.Tremor.Amplitude.RUE.UPDRS3.Num', 'Rest.Tremor.Amplitude.LUE.UPDRS3.Num', 'Rest.Tremor.Amplitude.RLE.UPDRS3.Num', 'Rest.Tremor.Amplitude.LLE.UPDRS3.Num', 'Rest.Tremor.Amplitude.Lip.Jaw.UPDRS3.Num', 'Constancy.of.Rest.Tremor.UPDRS3.Num'], 'Tremor.Subscore-sym.UPDRS3', 'Symmetric', '.UPDRS3.Num')
    ppmi_merge = create_lateralized_subscore(ppmi_merge, "Brady.Rigidity.Subscore.lateralized.UPDRS3", "Brady.Rigidity.Subscore-right.UPDRS3", "Brady.Rigidity.Subscore-left.UPDRS3", "Brady.Rigidity.Subscore-sym.UPDRS3",  'Brady.Rigidity.Subscore.UPDRS3') # Combine left and right and sym subscores into same column
    ppmi_merge = create_lateralized_subscore(ppmi_merge, "Tremor.Subscore.lateralized.UPDRS3", "Tremor.Subscore-right.UPDRS3", "Tremor.Subscore-left.UPDRS3", "Tremor.Subscore-sym.UPDRS3", 'Tremor.Subscore.UPDRS3')# Combine left and right and sym scores into same column (.lateralized)
    return ppmi_merge



def cleanup(ppmi_merge) : 
    ppmi_merge = add_Visit(ppmi_merge)
    ppmi_merge = fixed_variables(ppmi_merge, ['Dominant.Side.Disease', 'Enroll.Diagnosis', 'Enroll.Subtype','Consensus.Diagnosis', 'Consensus.Subtype', 'Subject.Phenoconverted', 'BirthDate', 'Sex', 'Handed', 'Analytic.Cohort','African.Berber.Race','Ashkenazi.Jewish.Race', 'Basque.Race', 'Hispanic.Latino.Race', 'Asian.Race', 'African.American.Race', 'Hawian.Other.Pacific.Islander.Race', 'Indian.Alaska.Native.Race', 'Not.Specified.Race',  'White.Race'])
    ppmi_merge = decode(ppmi_merge, '_ALL', ['EVENT_ID'], rename_cols = {'INFODT' : 'Event.ID.Date','Medication' : 'Medication(Dates)' , 'EVENT_ID' : 'Event.ID', 'PATNO' : 'Subject.ID'})
    ppmi_merge = reindex_df(ppmi_merge)
    ppmi_merge.set_index('Subject.ID', inplace = True)
    ppmi_merge.fillna('NA', inplace = True)
    ppmi_merge.to_csv(userdir + 'ppmi_merge_clinical_' + version + '.csv')
    return ppmi_merge
    


def create_cohort_df(excel_file : pd.ExcelFile) :
    cohort_df = pd.DataFrame()
    sheets = ['PD', 'Prodromal', 'HC', 'SWEDD']
    for sheet in sheets : 
        current_cohort_df = pd.read_excel(excel_file, sheet) # Read in
        current_cohort_df = current_cohort_df.loc[:, ~current_cohort_df.columns.str.startswith(tuple(['Unnamed', 'CONDATE', 'DIAG3']))]
        current_cohort_df['Enrollment.Subtype'] = ''
        if sheet == 'HC' :
            current_cohort_df['Subgroup'] = 'Healthy Control'
        if sheet == 'SWEDD' :
            current_cohort_df['Comments'] = '' # Replace comments with empty string because we don't want to merge comments for SWEDD sheet
        current_cohort_df = fill_subtype(current_cohort_df)
        cohort_df = cohort_df.append([current_cohort_df]) # Concat all 4 cohort dfs
    
    ## Rename columns
    cohort_df['CONPD'].replace({1 : 'Parkinson\'s Disease', 0 : ''}, inplace = True)
    cohort_df['CONPROD'].replace({1 : 'Prodromal',  0 : ''}, inplace = True)
    cohort_df['CONHC'].replace({1 : 'Healthy Control',  0 : ''}, inplace = True)
    cohort_df['CONSWEDD'].replace({1 : 'SWEDD',  0 : 'SWEDD/PD'}, inplace = True)
    cohort_df['Comments'].replace({'MSA' : 'Multiple System Atrophy'}, inplace = True)
    cohort_df = merge_columns(cohort_df, ['CONPD', 'CONPROD', 'CONHC', 'CONSWEDD','Comments'], 'Consensus.Diagnosis', ': ') # Get one column for Consensus Diagnosis with comments merged in
    cohort_df = merge_columns(cohort_df, ['Subgroup', 'Enrollment.Subtype'], 'Enroll.Subtype', '') # Get one column for Enroll.Subtype
    cohort_df = cohort_df.loc[:, ~cohort_df.columns.str.startswith(tuple(['CON','ENRL']))] # Remove columns that begin with CON and ENRL
    
    return cohort_df



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



def add_diagnosis_change(cohort_df, ppmi_merge) :
    def condensed_df(df : pd.DataFrame, keep_col_list : List, rename_col_dict: dict, drop_col_list : List) :
        new_df = df[keep_col_list]
        new_df.rename(columns = rename_col_dict, inplace = True)
        new_df.dropna(subset = drop_col_list, inplace = True)
        return new_df 
    diag_vis1 = condensed_df(cohort_df, ['PATNO', 'DIAG1', 'DIAG1VIS'], {'DIAG1VIS' : 'EVENT_ID'}, ['EVENT_ID'])
    diag_vis2 = condensed_df(cohort_df, ['PATNO', 'DIAG2', 'DIAG2VIS'], {'DIAG2VIS' : 'EVENT_ID'},['EVENT_ID'])
    ppmi_merge.drop(['DIAG1', 'DIAG1VIS', 'DIAG2', 'DIAG2VIS'], axis = 1, inplace = True) # Drop these from ppmi_merge so there aren't duplicates when we merge the diag_vis dfs
    ppmi_merge = pd.merge(diag_vis1, ppmi_merge, on = ['EVENT_ID', 'PATNO'], how = "outer" ) # Merge in first diagnosis change
    ppmi_merge = pd.merge(diag_vis2, ppmi_merge, on = ['EVENT_ID', 'PATNO'], how = "outer" ) # Merge in second diagnosis change
    ppmi_merge['DIAG1'].replace({ 'PD' : 'Parkinson\'s Disease', 'DLB': 'Dimentia with Lewy Bodies'}, inplace = True) # Decode
    ppmi_merge['DIAG2'].replace({ 'MSA' : 'Multiple System Atrophy', 'DLB': 'Dimentia with Lewy Bodies'}, inplace = True) # Decode
    ppmi_merge.rename(columns = {'DIAG1' : 'First.Diagnosis.Change', 'DIAG2' : 'Second.Diagnosis.Change'}, inplace = True) # Rename columns
    return ppmi_merge



def merge_and_transform_data(file, list_cols, list_cols_drop = False, rename_list= None, merge_on=None, merge_how=None, mod_name=None, decode_list=None,df= None,ext_name = None, ext_drop = None):
    if not isinstance(df, pd.DataFrame): 
        df = pd.DataFrame(columns = ['PATNO','EVENT_ID'])
        
    if merge_on == None and merge_how== None : 
        df = merge_dfs(df, file, list_cols,list_cols_drop, merge_on=['PATNO', 'EVENT_ID'], merge_how = "outer", ext_name=ext_name, ext_drop=ext_drop)

    else : 
        df = merge_dfs(df, file, list_cols,  list_cols_drop, merge_on=merge_on, merge_how =merge_how, ext_name= ext_name, ext_drop=ext_drop)
    
    if decode_list:
        df = decode(df, mod_name, decode_list)
    
    if rename_list: 
        df.rename(columns=rename_list, inplace=True)
    return df      



def decode(df, MOD_NAME, cols_to_decode, rename_cols = None) : 
    for col in cols_to_decode : 
        new_code_list = code_list[code_list['MOD_NAME'] == MOD_NAME]
        new_code_list = new_code_list[new_code_list['ITM_NAME'] == col]
        decoding_dict = dict(zip(new_code_list['CODE'], new_code_list['DECODE']))
        try : 
            decoding_dict_float = {float(k): v for k, v in decoding_dict.items()}
        except : 
            decoding_dict_float = decoding_dict
        df[col] = df[col].map(decoding_dict_float)
    
    if rename_cols :
        df.rename(columns =rename_cols, inplace = True)
    return df



def read_and_transform_data(csv_filename : str, list_cols : List, drop=False) :
    df = pd.read_csv(ppmi_download_path + csv_filename, skipinitialspace = True)  ## Read in csv
    if drop == False :
        df = df[list_cols] # keep columns in list_cols
    else :
        df.drop(list_cols, axis = 1, inplace = True) # drop columns in list_cols
    return df



def merge_dfs(df : pd.DataFrame, csv_filename : str, list_cols : List, drop, merge_on : str, merge_how : str, ext_name=None, ext_drop = None) :
    demo_df = read_and_transform_data(csv_filename, list_cols, drop) # Read in csv and keep only cols in list_cols
    if ext_name :
        demo_df = add_extension_to_column_names(demo_df, ext_drop, ext_name)
    if csv_filename == 'Socio-Economics_' + date + '.csv' :
        demo_df = demo_df.groupby('PATNO').mean().reset_index() # Take the mean of education years if there are 2 different number of years for one subject
    
    ppmi_merge = pd.merge(df, demo_df, on = merge_on, how = merge_how) # Merge
    return ppmi_merge



def add_extension_to_column_names(df, skip_col_list, ext):
    # For all UPDRS df columns - add the respective extension for which UPDRS assessment it is
    for col_name in df :
        if col_name not in skip_col_list :
            df.rename(columns = {str(col_name) : str(col_name) + ext }, inplace = True)
    return df



def format_updrs(df):
    ## Change UPDRS to floats 
    for col_name in df :
        if col_name.startswith('N') :
            df[col_name] = pd.to_numeric(df[col_name], errors = 'coerce', downcast = 'float')

    ## Keep only numeric variables 
    conditions = ['NP', 'PATNO', 'EVENT', 'NHY'] # Define the conditions for selecting numeric variables
    numeric_vars = [col_name for col_name in df.columns if col_name.startswith(tuple(conditions))] # Use list comprehension to filter columns based on the conditions
    df = df[numeric_vars] # Select only the numeric variables
    return df



def remove_duplicate_datscans(df):
    # FIXME - After merging in datscan files, duplicate event ids being created one with DATSCAN as "Completed" one with DATSCAN as "not completed" - if there are both of these - keep only "Completed"
    duplicate_datscan = df[['PATNO','EVENT_ID']].duplicated(keep = False) # Find locations of True for duplicated subs w/ 2 MRI at baseline
    duplicate_datscan_index = df[duplicate_datscan == True].index.tolist() # Get index of duplicates
    dup_subid_list = [] # Initialize duplicate subid list variable
    [dup_subid_list.append(index) for index in duplicate_datscan_index if df['DATSCAN'][index] == 'Not Completed']# Get the indices of duplicate subids that were labeled as Not Completed
    df = df.reset_index(drop = True)
    [df.drop(index = i, axis = 1, inplace = True) for i in reversed(dup_subid_list) if df['DATSCAN'][i] == 'Not Completed'] # Get rid of the duplicate subids that were labeled as Not Completed
    df.reset_index(drop=True, inplace=True)   
    return df



def add_mri_csv(df) :
    mri_df = merge_and_transform_data( 'Magnetic_Resonance_Imaging__MRI__' + date + '.csv', list_cols = [ 'PATNO', 'EVENT_ID', 'INFODT', 'MRICMPLT', 'MRIWDTI', 'MRIWRSS', 'MRIRSLT', 'MRIRSSDF' ], list_cols_drop = False, rename_list= { 'INFODT' : 'Image.Acquisition.Date', 'MRICMPLT' : 'MRI.Completed', 'MRIWDTI' : 'MRI.DTI' , 'MRIWRSS' : 'MRI.Resting.State' , 'MRIRSLT' : 'MRI.Results' , 'MRIRSSDF' : 'Resting.State.Dif.Day.PDMed.Use'}, merge_on=None, merge_how=None, mod_name='MRI', decode_list = ['MRIWDTI','MRIWRSS','MRIRSSDF','MRICMPLT','MRIRSLT'])
    duplicate_mri = mri_df[['PATNO','EVENT_ID']].duplicated(keep = False) # Find locations of True for duplicated subs w/ 2 MRI at baseline
    duplicate_mri_index = mri_df[duplicate_mri == True].index.tolist() # Get index of duplicates
    dup_subid_list = [] # Initialize duplicate subid list variable
    [dup_subid_list.append(index) for index in duplicate_mri_index if mri_df['MRI.Completed'][index] == 'Not Completed']# Get the indices of duplicate subids that were labeled as Not Completed
    mri_df = mri_df.reset_index(drop = True)
    [mri_df.drop(index = i, axis = 1, inplace = True) for i in reversed(dup_subid_list) if mri_df['MRI.Completed'][i] == 'Not Completed'] # Get rid of the duplicate subids that were labeled as Not Completed (that also have another labeled as completed)
    df = pd.merge(df, mri_df, on = ['PATNO','EVENT_ID'], how = "outer")
    return df



def add_concomitant_med_log(df : pd.DataFrame) :
    med_df = pd.read_csv(ppmi_download_path + 'Concomitant_Medication_Log_' + date + '.csv', skipinitialspace=True) # Medication history
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
    df = pd.merge(df, med_df, on = ['PATNO', 'EVENT_ID'], how = "outer") # Merge med_df in
    df = df.sort_values(by = ['PATNO','Age']).reset_index(drop = True) # Sort values by subject and age (similar to event id bc age in order of event id)
    return df



def add_LEDD(ppmi_merge) :
    def func(row):
        ## If in LD column there is a (i.e. 150 + LD) * 0.33) - create a new duplicate column with just 150 variable - bc this LEDD needs to be added to full LEDD and these formulas are therefore not correct?  # per Pavan notes issues
        if '(' in str(row['LEDD']):
            row2 = row.copy()
            temp = row2['LEDD']
            row2['LEDD'] = re.search('\(([0-9]+)', temp).group(1)
            return pd.concat([row, row2], axis=1)
        return row

    ## LEDD Medication Status - FIXME Assumtion : If stop date is NA we assume LEDD only occurred in that month
    LEDD_med_df = read_and_transform_data( 'LEDD_Concomitant_Medication_Log_' + date + '.csv', ['PATNO', 'LEDD', 'STARTDT', 'STOPDT'], drop = False)
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
    LEDD_med_df = read_and_transform_data('LEDD_Concomitant_Medication_Log_' + date + '.csv', ['PATNO','LEDTRT', 'LEDD', 'STARTDT', 'STOPDT'], drop = False)
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
    
    ## LEDD Medication Status - FIXME Assumption : If stop date is NA we assume therapy is ongoing
    LEDD_med_df = read_and_transform_data('LEDD_Concomitant_Medication_Log_' + date + '.csv', ['PATNO', 'LEDD', 'STARTDT', 'STOPDT'], drop = False)
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
    LEDD_med_df = read_and_transform_data('LEDD_Concomitant_Medication_Log_' + date + '.csv', ['PATNO','LEDTRT', 'LEDD', 'STARTDT', 'STOPDT'], drop = False)
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



def add_comorbidities(ppmi_merge) :
    ## Comorbidities # FIXME not useful column
    comorbid_df = pd.read_csv(ppmi_download_path + 'Medical_Conditions_Log_' + date + '.csv', skipinitialspace=True) # Medication history
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



def add_subscore(df : pd.DataFrame, subscore_side_list : list, new_col_name : str, side = None, ext = None) :
    """
    Include lateralized subscroes (i.e. Brady Rigidity and Tremor subscores) into dataframe.
    Arguments
    ------------------
    df : pd.DataFrame containing scores that make up subscore
    subscore_side_list : list containing column names of the scores that make up the subscore
    side : 'Left' or 'Right' or 'Symmetric'
    new_col_name : name of new column name with lateralized subscore
    """
    subscore_side = df[subscore_side_list]  # Get dataframe of only columns in brady_left
    df[new_col_name] = 0 # Initialize lateralized variable

    
    if side == 'Right' or side == 'Left' : 
        subscore_side.loc[subscore_side['Dominant.Side.Disease'] != side, :] = np.nan # Make all rows nan if dominant side of disease is not left
        subscore_side_temp = subscore_side.drop('Dominant.Side.Disease',1) # Drop dominant side of disease - necessary because this cannot be summed in next line
        idx  = subscore_side_temp.loc[pd.isnull(subscore_side_temp).any(1), :].index
        df[new_col_name] = subscore_side_temp.sum(axis = 1) # Sum of all columns in each row where dom side is left
        df[new_col_name].iloc[idx] = np.nan # Fill in subscores that should be nans as nan
    
    elif side == 'Symmetric' : 
        subscore_side.loc[subscore_side['Dominant.Side.Disease'] != side, :] = np.nan # Make all rows nan if dominant side of disease is not left
        subscore_side_temp = subscore_side.drop('Dominant.Side.Disease',1) # Drop dominant side of disease - necessary because this cannot be summed in next line
        idx  = subscore_side_temp.loc[pd.isnull(subscore_side_temp).any(1), :].index
        x = subscore_side_temp.fillna(0) # because adding 1 plus nan equals nan
        if "Brady" in new_col_name :
            df[new_col_name] = x['Rigidity.Neck' + ext ] + (x['Rigidity.RUE' + ext] + x['Rigidity.LUE'+ ext ])/2 + (x['Rigidity.RLE'+ ext] + x['Rigidity.LLE'+ ext])/2  + (x['Finger.Tapping.Right.Hand'+ ext] +x['Finger.Tapping.Left.Hand'+ ext])/2 + (x['Hand.Movements.Right.Hand'+ ext] + x['Hand.Movements.Left.Hand'+ ext])/2 + (x['Pronation.Supination.Right.Hand'+ ext]+x['Pronation.Supination.Left.Hand'+ ext])/2 +  (x['Toe.Tapping.Right.Foot'+ ext]+ x['Toe.Tapping.Left.Foot'+ ext])/2 +  (x['Leg.Agility.Right.Leg'+ ext] + x['Leg.Agility.Left.Leg'+ ext])/2
            df[new_col_name].iloc[idx] = np.nan # Fill in subscores that should be nans as nan
        elif "Tremor" in new_col_name :
            df[new_col_name] = x['Tremor.UPDRS2.Num'] +  (x['Postural.Tremor.Right.Hand' + ext ]  + x['Postural.Tremor.Left.Hand' + ext ])/2 + (x['Kinetic.Tremor.Right.Hand' + ext ] + x['Kinetic.Tremor.Left.Hand'+ ext ])/2 + (x['Rest.Tremor.Amplitude.RUE' + ext ]+ x['Rest.Tremor.Amplitude.LUE' + ext])/2 + (x['Rest.Tremor.Amplitude.RLE' + ext ] +  x['Rest.Tremor.Amplitude.LLE' + ext])/2 + x['Rest.Tremor.Amplitude.Lip.Jaw' + ext] + x['Constancy.of.Rest.Tremor' + ext]
            df[new_col_name].iloc[idx] = np.nan
    
    else :
        idx  = subscore_side.loc[pd.isnull(subscore_side).any(1), :].index
        df[new_col_name] = subscore_side.sum(axis = 1) # Get sum of subscore
        df[new_col_name].iloc[idx] = np.nan # Replace rows that should be nan with nan
    return df



def create_lateralized_subscore(df : pd.DataFrame, subscore_lateralized_name : str, right_subscore_name : str, left_subscore_name : str, sym_subscore_name : str, subscore_name ) :
    df[subscore_lateralized_name] = df.pop(right_subscore_name).fillna(df.pop(left_subscore_name))
    df[subscore_lateralized_name] = df.pop(subscore_lateralized_name).fillna(df.pop(sym_subscore_name))
    
    latisna = df[subscore_lateralized_name].isna() & df[subscore_name].notna()
    df[subscore_lateralized_name].loc[latisna] = df[subscore_name].loc[latisna]
    return df     
 


def add_DXsimplified(df):
    df['DXsimplified'] = '' # Initialize DXsimplfied
    df.loc[df['Consensus.Subtype'] == 'Healthy Control', 'DXsimplified'] = 'HC'
    df.loc[df['Enroll.Diagnosis'] == 'Healthy Control', 'DXsimplified'] = 'HC'
    df.loc[df['Enroll.Diagnosis'] == 'Parkinson\'s Disease', 'DXsimplified'] = 'Sporadic_PD'
    df.loc[df['Consensus.Subtype'] ==  "Sporadic", 'DXsimplified'] = "Sporadic_PD"
    df.loc[df['Enroll.Diagnosis'] == "Prodromal", 'DXsimplified'] = "Sporadic_Pro"
    df.loc[df['Consensus.Subtype'] == "Hyposmia" , 'DXsimplified'] = "Sporadic_Pro"
    df.loc[df['Consensus.Subtype'] == "Hyposmia : Phenoconverted", 'DXsimplified'] = "Sporadic_Pro"
    df.loc[df['Consensus.Subtype'] == "RBD", 'DXsimplified'] = "Sporadic_Pro"
    df.loc[df['Consensus.Subtype'] == "RBD : Phenoconverted", 'DXsimplified'] = "Sporadic_Pro"
    df.loc[df['Consensus.Subtype'] == "Genetic : LRRK2", 'DXsimplified'] = "LRRK2_PD"
    df.loc[df['Consensus.Subtype'] == "Genetic : LRRK2 + GBA", 'DXsimplified'] = "LRRK2_PD"
    df.loc[df['Consensus.Subtype'] == "Genetic : LRRK2 + GBA not Prodromal", 'DXsimplified'] = "LRRK2_PD"  
    df.loc[df['Consensus.Subtype'] == "Genetic : LRRK2 not Prodromal", 'DXsimplified'] = "LRRK2_PD"
    df.loc[df['Consensus.Subtype'] == "Genetic : LRRK2 + GBA Prodromal", 'DXsimplified'] = "LRRK2_Pro"
    df.loc[df['Consensus.Subtype'] == "Genetic : LRRK2 Phenoconverted", 'DXsimplified'] = "LRRK2_Pro"
    df.loc[df['Consensus.Subtype'] ==  "Genetic : LRRK2 Prodromal", 'DXsimplified'] = "LRRK2_Pro"
    df.loc[df['Consensus.Subtype'] == "Genetic : GBA", 'DXsimplified'] = "GBA_PD"
    df.loc[df['Consensus.Subtype'] == "Genetic : GBA not Prodromal", 'DXsimplified'] = "GBA_PD"
    df.loc[df['Consensus.Subtype'] == "Genetic : GBA Prodromal", 'DXsimplified'] = "GBA_Pro"
    df.loc[df['Consensus.Subtype'] ==  "RBD : Phenoconverted with GBA", 'DXsimplified'] = "GBA_Pro"
    df.loc[df['Enroll.Diagnosis'] == 'SWEDD', 'DXsimplified'] = "nonPDorMSA"
    df.loc[df['Consensus.Subtype'] == "non-PD", 'DXsimplified'] = "nonPDorMSA"
    df.loc[df['Consensus.Subtype'] ==  "SWEDD/non-PD Active", 'DXsimplified'] = "nonPDorMSA"
    df.loc[df['Consensus.Subtype'] == "GBA", 'DXsimplified'] = "GBA_HC"
    df.loc[df['Consensus.Subtype'] ==  "Genetic : SNCA", 'DXsimplified'] = "SNCA_PD"
    df.loc[df['Consensus.Subtype'] == "Genetic : SNCA Prodromal", 'DXsimplified'] = "SNCA_Pro"
    df.loc[df['Consensus.Subtype'] == "No Mutation not Prodromal", 'DXsimplified'] = np.NaN
    df.loc[df['Consensus.Subtype'] == "non-HC", 'DXsimplified'] = np.NaN
    df.loc[df['Consensus.Subtype'] ==  "SWEDD/PD Active", 'DXsimplified'] = np.NaN
    return df



def add_PD_Disease_Duration(df : pd.DataFrame)  :
    df['PD.Diagnosis.Duration'] = '' # Initialize PD.Diagnosis.Duration variable
    for row_num in range(len(df['PD.Diagnosis.Date'])) :
        if isinstance(df['PD.Diagnosis.Date'].loc[row_num], str) and isinstance(df['INFODT'].loc[row_num], str): # If we have both a PD Diagnosis date and an event id date
            diag_year = int(df['PD.Diagnosis.Date'].loc[row_num].split('/')[1]) # Diagnosis year
            diag_month = int(df['PD.Diagnosis.Date'].loc[row_num].split('/')[0]) # Diagnosis month
            event_year = int(df['INFODT'].loc[row_num].split('/')[1]) # Visit date year
            event_month = int(df['INFODT'].loc[row_num].split('/')[0]) # Visit date month
            diff = relativedelta.relativedelta(datetime(event_year, event_month, 1), datetime(diag_year, diag_month, 1)) # FIXME ASSUMPTION visit date and diagnosis date was the first of the month
            df['PD.Diagnosis.Duration'].iloc[row_num] = ((diff.years)*12 + diff.months)/12 # PD.Diagnosis.Duration in years
    
    ## Add in min PD Disease duration
    df['DXsimplified'].fillna('NA', inplace = True)
    df['PD.Diagnosis.Duration'].fillna('', inplace = True)
    subids = df['PATNO'].unique() # Unique subject ids
    for subid in subids :
        temp_df = df[(df['PATNO'] == subid) & (df['DXsimplified'].str.contains('_PD')) & (df['PD.Diagnosis.Duration'] != '')]
        if len(temp_df) > 1 :
            mydd = min(temp_df['PD.Diagnosis.Duration'])
            df.loc[df['PATNO'] == subid, 'PD.Min.Disease.Duration'] = mydd
        else : 
            mydd = temp_df['PD.Diagnosis.Duration']
            df.loc[df['PATNO'] == subid, 'PD.Min.Disease.Duration'] = mydd  
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

    

def get_enrollment_dx_nonanalytic(df, cohort_df) : 
    analytic_cohort_subids = cohort_df['PATNO'].unique().tolist() # subids for analytic cohort
    df['Analytic.Cohort'] = df['PATNO'].apply(lambda x: 'Analytic Cohort' if x in analytic_cohort_subids else 'Not Analytic Cohort')
    participant_status = read_and_transform_data('Participant_Status_' + date + '.csv',['PATNO', 'COHORT_DEFINITION'], drop = False )    ## Get Enrollment Diagnosis for subjects in Not Analytic Cohort - do this using the participants_status.csv
    participant_status.rename(columns = {'COHORT_DEFINITION' : 'Enroll.Diagnosis'}, inplace = True)
    not_analytic = df[df['Analytic.Cohort'] == 'Not Analytic Cohort'] # Split up Analytic cohort df and not Analytic Cohort df    
    not_analytic_participant_status = pd.merge(not_analytic, participant_status, on = ['PATNO'], how = "left") # Merge not Atlantic subids with enrollment diagnosis in participant_status
    not_analytic_participant_status.drop(['Enroll.Diagnosis_x'], axis = 1, inplace = True) # Remove the extra Enroll.Diagnosis created at merge
    not_analytic_participant_status.rename(columns = {'Enroll.Diagnosis_y' : 'Enroll.Diagnosis'}, inplace = True)
    not_analytic_participant_status = not_analytic_participant_status[['PATNO','EVENT_ID','Enroll.Diagnosis','Enroll.Subtype']]
    not_analytic_participant_status.loc[not_analytic_participant_status['Enroll.Diagnosis'] == 'Healthy Control', 'Enroll.Subtype'] = 'Healthy Control' # For Healthy Control subjects in the Not Analytic Cohort - make 'Enroll.Subtype' = Healthy Control
    df = pd.merge(df, not_analytic_participant_status, how = 'left', on = ['PATNO','EVENT_ID'])
    df = merge_columns(df, ['Enroll.Diagnosis_x', 'Enroll.Diagnosis_y'], 'Enroll.Diagnosis', '')
    df = merge_columns(df, ['Enroll.Subtype_x', 'Enroll.Subtype_y'], 'Enroll.Subtype', '')
    return df



def fixed_variables(df: pd.DataFrame, fixed_var_list: List[str]) -> pd.DataFrame:
    for col_name in fixed_var_list:
        df[col_name].fillna('NA', inplace=True)
        na_rows = df[col_name] == 'NA'  # Find rows with NA values
        
        # Get unique PATNO values in the NA rows
        unique_patnos = df.loc[na_rows, 'PATNO'].unique()
        
        # Iterate over unique PATNO values and fill in NA values
        for patno in unique_patnos:
            mask = (df['PATNO'] == patno) & (~na_rows)
            fixed_var_value = df.loc[mask, col_name].values
            if fixed_var_value.any():
                df.loc[na_rows & (df['PATNO'] == patno), col_name] = fixed_var_value[0]
    return df



def add_Visit(df) :
    df['Visit'] = np.NaN # Initialize Visit col
    searchfor = ['BL', 'V', 'R', 'TANS'] # Strings to search for
    temp = df['EVENT_ID'].str.contains('|'.join(searchfor)) # locations of where row contains str: baseline or visit month
    df['Visit'].loc[temp == True] = df['EVENT_ID'].loc[temp == True] # Fill in 'Visit' col with event.ID for baseline or visit month
    df['Visit'] = df['Visit'].str.replace("R", "") # Replace Remote visit month with '' (want only month number)
    df['Visit'] = df['Visit'].str.replace("V", "") # Replace Visit month with '' (want only month number)
    df['Visit'] = df['Visit'].str.replace("BL", "0") # Replace baseline with 0
    df['Visit'] = df['Visit'].str.replace("TANS", "NA") # Replace baseline with 0
    return df



def reindex_df(df)  :
    # Reindex columns
    desired_order = ['Subject.ID', 'Event.ID', 'Event.ID.Date' , 'Enroll.Diagnosis', 'Enroll.Subtype', 'Consensus.Diagnosis', 'Consensus.Subtype','Analytic.Cohort','Subject.Phenoconverted','First.Diagnosis.Change', 'Second.Diagnosis.Change',  'First.Symptom.Date', 'PD.Diagnosis.Date', 'PD.Diagnosis.Duration','BirthDate', 'Age', 'Sex', 'Handed', 'Weight(kg)',    'Height(cm)', 'Systolic.BP.Sitting', 'Diastolic.BP.Sitting',  'Systolic.BP.Standing',  'Diastolic.BP.Standing', 'SCAU8', 'SCAU9', 'SCAU15', 'SCAU16', 'MSEADLG', 'Education.Years', 'Dominant.Side.Disease', 'African.Berber.Race','Ashkenazi.Jewish.Race', 'Basque.Race', 'Hispanic.Latino.Race', 'Asian.Race', 'African.American.Race', 'Hawian.Other.Pacific.Islander.Race', 'Indian.Alaska.Native.Race', 'Not.Specified.Race',  'White.Race', 'Motor.Function.Page.Name',    'Motor.Function.Source',    'Trouble.Rising.Chair',    'Writing.Smaller',    'Voice.Softer',    'Poor.Balance',    'Feet.Stuck',    'Less.Expressive',    'Arms/Legs.Shake',    'Trouble.Buttons',    'Shuffle.Feet',    'Slow.Movements',    'Been.Told.PD',    'Cognitive.Page.Name',    'Cognitive.Source', 'Cognitive.Decline',    'Functional.Cognitive.Impairment',    'Confidence.Level.Cognitive.Diagnosis',    'Cognitive.State',    'Cognitive.Tscore.Cat',    'MOCA.Total', 'Medication(Dates)' ,'LEDD.sum', 'LEDD.sum.Cat', 'LEDD.ongoing.sum','LEDD.ongoing.sum.Cat','Medical.History.Description(Diagnosis.Date)']
    other_columns = [col for col in df.columns if col not in desired_order]
    new_column_order = desired_order + other_columns
    df = df[new_column_order]
    
    # Reindex rows
    df['INFODT_temp'] = pd.to_datetime(df['Event.ID.Date'])
    df = df.sort_values(by=['Subject.ID', 'INFODT_temp'])
    df.drop(['INFODT_temp'], axis = 1, inplace = True) # drop columns in list_cols
    df = df.reset_index(drop=True)
    return df 

    

if __name__=="__main__":
    main()          
