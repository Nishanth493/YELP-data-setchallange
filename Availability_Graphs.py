######### Availability Graphs for each of dataset
import pandas as pd

####### Do for Rdata
RData = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/yelp_academic_dataset_review.csv")
def availability(df):
    col_names = df.columns.values
    Att = pd.DataFrame()
    denom = float(len(df))
    Att_list = []
    for name in col_names:
        #print(name)
        Att_list = [name]
        avail = float(len(df[name].dropna()))/denom * 100
        Att_list = Att_list + [avail]
        Att = pd.concat([Att, pd.DataFrame(Att_list).transpose()], axis = 0)
    return (Att)
    
#All columns are available   


############ Do for final merged data
Merge2 = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/MergedData_214.csv")

col_names = Merge2.columns.values
Att = pd.DataFrame()
denom = float(len(Merge2))
Att_list = []
for name in col_names:
    print(name)
    Att_list = [name]
    avail = float(len(Merge2[name].dropna()))/denom * 100
    Att_list = Att_list + [avail]
    Att = pd.concat([Att, pd.DataFrame(Att_list).transpose()], axis = 0)
    
Att.to_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Merge_DataAvail.csv")

####### Separately Busines Attributes and Business Categories

### Business Attributes

SakData = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Business_CityAtt.csv")
col_names = SakData.columns.values
Att = pd.DataFrame()
denom = float(len(SakData))
Att_list = []
for name in col_names:
    print(name)
    Att_list = [name]
    avail = float(len(SakData[name].dropna()))/denom * 100
    Att_list = Att_list + [avail]
    Att = pd.concat([Att, pd.DataFrame(Att_list).transpose()], axis = 0)
Att.to_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Attr_Avail.csv")
    
######### Business Categories
DData1 = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/file_categories.csv")
col_names = DData1.columns.values
Att = pd.DataFrame()
denom = float(len(DData1))
Att_list = []
for name in col_names:
    print(name)
    Att_list = [name]
    avail = float(len(DData1[name].dropna()))/denom * 100
    Att_list = Att_list + [avail]
    Att = pd.concat([Att, pd.DataFrame(Att_list).transpose()], axis = 0)
Att.to_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Cat_Avail.csv")

########## Business Timings
DData2 = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/file_hours.csv")
col_names = DData2.columns.values
Att = pd.DataFrame()
denom = float(len(DData2))
Att_list = []
for name in col_names:
    print(name)
    Att_list = [name]
    avail = float(len(DData2[name].dropna()))/denom * 100
    Att_list = Att_list + [avail]
    Att = pd.concat([Att, pd.DataFrame(Att_list).transpose()], axis = 0)
Att.to_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Time_Avail.csv")
