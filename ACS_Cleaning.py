import os
import pandas as pd
filz = os.getcwd() + '/data'

acs_files = [fil for fil in os.listdir(filz) if fil[0:3]=='ACS']
counter = 0 
for df in acs_files:
    if counter == 0:
        counter +=1
        acs_dat = pd.read_csv(filz+'/'+df,header=1)
        acs_dat['year'] = df.split('_')[1] 
        acs_dat['zip'] = acs_dat['Geography'][0].split(' ')[1] 
    
    else: 
        newframe = pd.read_csv(filz+'/'+df,header=1)
        newframe['year'] = df.split('_')[1]
        newframe['zip'] =  newframe['Geography'][0].split(' ')[1]
        acs_dat = pd.concat([acs_dat,newframe]).reset_index(drop=True)

        counter +=1 

fem_frame = acs_dat.iloc[:,0:126]
# the first three are the id and geoid of this new one, and zip + strange string
rest = acs_dat.iloc[:,129:]
man_frame = rest.iloc[:,0:126]
only_frame = rest.iloc[:,126:]

drop_list = []
for col in only_frame.columns:
    if  'error;' in col.lower().split(' '):
        drop_list.append(col)
    elif 'percent imputed' in col.lower():
        drop_list.append(col)

    elif 'percent allocated' in col.lower():
        drop_list.append(col)

    elif '12' in col.lower().split(' '):
        drop_list.append(col)

only_frame.drop(drop_list,axis = 1,inplace=True)
only_frame.to_csv(os.getcwd()+'/data/acs.csv') 
