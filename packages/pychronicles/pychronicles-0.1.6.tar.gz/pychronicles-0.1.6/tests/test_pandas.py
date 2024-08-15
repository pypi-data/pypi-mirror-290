import pandas as pd
import numpy as np
from pychronicles import Chronicle

df = pd.read_csv("/data/physionet.org/files/mimiciv/1.0/core/admissions.csv")
df.head()

# data preparation (dates have to be set to be is the right format)
df['admittime'] = pd.to_datetime(df['admittime'])
df['admittime'] = df['admittime'].dt.date

temp = np.array([np.datetime64(str(elt)) for elt in df['admittime'].tolist()])
df.index = temp
df.index = df.index.astype("datetime64[ns]") # enforce the time format (required!)

# definition of the chronicle to match
c=Chronicle()
#c.add_event(0,'insurance=="Medicaid"')
c.add_event(0,'admission_type=="EW EMER."')
c.add_event(1,'admission_type=="OBSERVATION ADMIT"')
c.add_event(2,'admission_type=="EW EMER."')
c.add_constraint(0,1, (np.timedelta64(1,'D'),np.timedelta64(1000,'D')))

print(f'Chronicle:\n{c}')

"""patientid=15496609

print(f"Recognition for patient {patientid}")

# application to one sequence of the dataset
data = df[df['subject_id']==patientid]

ret = data.tpattern.match(c)
print(f"match: {ret}")

ret = data.tpattern.project(c)
print(f"projection:\n{ret}")"""


print(f"Projection for the first 100 patients")

ret= df.groupby('subject_id').apply(lambda d: d.tpattern.match(c))
print(ret.sum())

patients_selection = ret[ret].reset_index().sample(100)

reduced_df = df.merge(patients_selection, on="subject_id", how="right")


reduced_df = reduced_df[ ["subject_id", 'admittime', 'dischtime', 'admission_type', 'admission_location'] ]

#ret= df.iloc[:100].groupby('subject_id').apply(lambda d: d.tpattern.recognize(c))
#print(ret)
"""ret= df.iloc[10000:30000].groupby('subject_id').apply(lambda d: d.tpattern.project(c))
L=ret.to_list()
L = [l for l in L if len(l)>0]
ret = pd.concat(L)
print(ret)"""
