# PPMI Longitudinal Clinical File 
The ppmi_merge.csv file created [here](file:///Users/areardon/Desktop/ppmi_merge/ppmi_revamp.html) includes patient-specific measurements that provide the appropriate context for understanding the patients in PPMI 1.0 and 2.0 as they change over time including but not limited to : 

#### Clinical Information
- Diagnosis
- Subtype
- Disease laterality
- Medication status
- Motor symptoms
- Cognitive symptoms
- MDS-UPDRS Parts 1-4 
- MRI-characteristics 

#### Genetic Information 
- Static genetic info (SNPs)

#### T1-Weighted antspyt1w Derived Variables
- Area of ROIs (references below)
- Volumes of ROIs (references below)



## To create ppmi_merge.csv:
We utilized PPMI subject clinical data files (PPMI Study Data), genetic information, and T1-weighted antspyt1w derived variables to create a single .csv file that contains genetic information, longitudinal clinical information, and longitudinal imaging information of PPMI subjects.

#### Clinical Information : 
1.) Get access to PPMI database and login [here](https://ida.loni.usc.edu/login.jsp?project=PPMI).  
2.) Click download from the navigation bar and select study data.  
3.) Select ALL documents and zip files and click download.  
4.) Unzip and save the folder on your computer.  


#### Genetic Information :
We also utilize genetic info... (TBD)


#### T1 Information : 
We also use T1 derived variables from [antspyt1w](https://www.nature.com/articles/s41598-021-87564-6) to get area and volumes of ROIs from each T1-weighted MRI image for every subject.  

References to include :   
1.) Imaging derived variables via : https://www.nature.com/articles/s41598-021-87564-6   
2.) Cortical regions : 101 labeled brain images and a consistent human cortical labeling protocol. Arno Klein, Jason Tourville. Frontiers in Brain Imaging Method   6:171. DOI: 10.3389/fnins.2012.00171  and https://mindboggle.readthedocs.io/en/latest/labels.html  
3.) Cit 168 labels https://www.nature.com/articles/sdata201863  
4.) Basal forebrain :  in preparation  
5.) Hippocampus subfields : in preparation  
6.) QC : in preparation
