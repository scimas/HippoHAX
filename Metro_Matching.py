import pandas as pd
import os

metro_zip = {'Braddock Road': '22314',
             'King St-Old Town': '22314',
             'Huntington': '22203',
             'Crystal City': '22202',
             'Ronald Reagan Washington National Airport': '22202',
             'Eisenhower Avenue': '22314',
             'L\'Enfant Plaza': '20024',
             'Rosslyn': '22209',
             'Arlington Cemetery': '22209',
             'Van Dorn Street': '22310',
             'Franconia-Springfield': '22150',
             'Pentagon': '22202',
             'Pentagon City': '22202'}

df = pd.read_csv('data/metro_stations.csv')
zipc = ['fixme'] * df.shape[0]
df['zipc'] = zipc
for index, row in df.iterrows():
    for key in metro_zip.keys():
        if row['Name'] == key.strip():
            df.iloc[index, 4] = metro_zip[key]

filz = os.getcwd() + '/data'

acs_files = [fil for fil in os.listdir(filz) if fil[0:3] == 'ACS']
counter = 0
for df in acs_files:
    if counter == 0:
        counter += 1
        acs_dat = pd.read_csv(filz+'/' + df, header=1)
        acs_dat['year'] = df.split('_')[1]
        acs_dat['zip'] = acs_dat['Geography'][0].split(' ')[1]
    else:
        newframe = pd.read_csv(filz+'/' + df, header=1)
        newframe['year'] = df.split('_')[1]
        newframe['zip'] = newframe['Geography'][0].split(' ')[1]
        acs_dat = pd.concat([acs_dat, newframe]).reset_index(drop=True)
        counter += 1

fem_frame = acs_dat.iloc[:, 0:126]
# the first three are the id and geoid of this new one,
# and zip + strange string
rest = acs_dat.iloc[:, 129:]
man_frame = rest.iloc[:, 0:126]
only_frame = rest.iloc[:, 126:]

drop_list = []
for col in only_frame.columns:
    if 'error;' in col.lower().split(' '):
        drop_list.append(col)
    elif 'percent imputed' in col.lower():
        drop_list.append(col)

    elif 'percent allocated' in col.lower():
        drop_list.append(col)

    elif '12' in col.lower().split(' '):
        drop_list.append(col)

only_frame.drop(drop_list, axis=1, inplace=True)
only_frame.to_csv(os.getcwd() + '/data/acs1.csv')

# braddock king and eisenhower aer e22314 unless you coulnt king as 22301.
# Huntiongon is 22303
# van dorn 22310
# pentagon = 22202
# pentagon city = 22202
# pentagon 22202
# crystal city = 22202
# ronald reagan = 22202
# Huntington = 22303
# L'Enfant Plaza =  20024
# rosslyn = 22209
# arlington cemetary = 22209
# franconia springfield, VA 22150

df2 = pd.read_csv('data/acs.csv')
df2['zip2'] = df2['zip'].apply(str)
df3 = df.merge(df2, how='left', left_on=df.zipc, right_on=df2.zip2)

filz = os.getcwd() + '/data'

acs_files = [fil for fil in os.listdir(filz) if fil[0:3] == 'ACS']
counter = 0
for df in acs_files:
    if counter == 0:
        counter += 1
        acs_dat = pd.read_csv(filz+'/'+df, header=1)
        acs_dat['year'] = df.split('_')[1]
        acs_dat['zip'] = acs_dat['Geography'][0].split(' ')[1]
    else:
        newframe = pd.read_csv(filz+'/'+df, header=1)
        newframe['year'] = df.split('_')[1]
        newframe['zip'] = newframe['Geography'][0].split(' ')[1]
        acs_dat = pd.concat([acs_dat, newframe]).reset_index(drop=True)
        counter += 1
