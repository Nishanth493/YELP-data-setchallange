############# Few basic exploratory analysis
import pandas as pd
##### Create count of unique categories and count of business attributes
RData = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/yelp_academic_dataset_review.csv")
DData1 = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/file_categories.csv")
Business_Ids1 = DData1[DData1['Restaurants'] == 1.0]['business_id']
Business_Ids2 = DData1[DData1['Shopping'] == 1.0]['business_id']
Business_Ids3 = DData1[DData1['Food'] == 1.0]['business_id']

Ids1 = Business_Ids1.append(Business_Ids2)
Ids2 = Ids1.append(Business_Ids3)
Ids3 = set(Ids2)
Ids3 = [Ids3]
#Ids4 = [Ids3.transpose]
#Ids4 = pd.DataFrame(pd.DataFrame(Ids3).transpose)
#Ids3.to_csv("C:/User/Nishanth/Documents/IEOR242/Project/DataSets/Final_Ids.csv")

pp = DData1[DData1['business_id'].isin(Ids3)][['business_id','Restaurants','Shopping','Food']]
SakData_1 = SakData[SakData['business_id'].isin(Ids3)]
########## Just take RData rows with above Ids2
Rp = RData[RData['business_id'].isin(Ids3)]
Deep_Data = Rp.merge(pp, how = 'left' , on = 'business_id')
Deep_Data.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Review_3Cat.csv")

################ Business data attributes########

####### First subset attribute dataset with only three categories
col_names = SakData_1.columns.values
Att = pd.DataFrame()
denom = float(len(SakData_1))
Att_list = []
for name in col_names:
    print(name)
    Att_list = [name]
    avail = float(len(SakData_1[name].dropna()))/denom * 100
    Att_list = Att_list + [avail]
    Att = pd.concat([Att, pd.DataFrame(Att_list).transpose()], axis = 0)
Att.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Avail_v1.csv")

######## Identifying required attributes of business we want to capture
Att.columns = ['Attribute', 'Availability']
colnames_att = Att[Att['Availability'] >= 40]['Attribute']

### First few columns
BA_1 = SakData_1.ix[:,0:18]
del BA_1['Unnamed: 1']
BA_2 = SakData_1[colnames_att]
BA_2 = BA_2.ix[:,18:53]
BA_2 = BA_2.fillna('None')
### Make all the above columns except business id categorical
BA_2 = BA_2.apply(lambda x: x.astype('category')) 
BA_2.apply(lambda x: x.astype('category')).dtypes
####### Combine everything and clean up the rest of columns and save the business attribute data
BA = pd.concat([BA_1, BA_2], axis = 1).reset_index()
BA.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Tuesday_Files/Attr.csv")

####### Category Count 
Cat_sub = DData1[DData1['business_id'].isin(Ids3)] ##length is 81583
Cat_1 = Cat_sub.ix[:,17: 1209]
Cat_1 = Cat_1.fillna(0)
col_sum = Cat_1.sum(axis = 1)
pp['Cat_count'] = col_sum
pp.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Tuesday_Files/Cate.csv")

############# Duration on weekdays - 30 mins
Time_data = DData2[DData2['business_id'].isin(Ids3)].reset_index()
Time_1 = Time_data.ix[:,[0,4]]
Time_dt = Time_data.ix[:,18:25]

def duration_day(x):
    if str(Time_dt['Monday'][x]) == 'nan':
        return(0)
    else:
        day_row = str(Time_dt['Monday'][x]).split('-')
        if int(day_row[1].split(':')[0]) < 12 and int(day_row[0].split(':')[0]) != int(day_row[1].split(':')[0]):
            closing_hour = int(day_row[1].split(':')[0]) + 12
        else:
            closing_hour = int(day_row[1].split(':')[0])
        duration = closing_hour - int(day_row[0].split(':')[0])
        return(duration)
Time_dt['WeekdayDur'] = [duration_day(x) for x in range(len(Time_dt))]
### Duration on weekends -  30 mins
Time_dt['SatDur'] = [duration_day(x) for x in range(len(Time_dt))]
Time_dt['SunDur'] = [duration_day(x) for x in range(len(Time_dt))]

def closing_hour(x):
    if str(Time_dt['Sunday'][x]) == 'nan':
        return(0)
    else:
        day_row = str(Time_dt['Sunday'][x]).split('-')
        if int(day_row[1].split(':')[0]) < 12 and int(day_row[0].split(':')[0]) != int(day_row[1].split(':')[0]):
            closing_hour = int(day_row[1].split(':')[0]) + 12
        else:
            closing_hour = int(day_row[1].split(':')[0])
        return (closing_hour)
        
def opening_hour(x):
    if str(Time_dt['Sunday'][x]) == 'nan':
        return(0)
    else:
        day_row = str(Time_dt['Sunday'][x]).split('-')
        return (int(day_row[1].split(':')[0]))
    

##### Opening hour on weekdays and weekends -  30 mins
Time_dt['Opening_Weekday'] = [opening_hour(x) for x in range(len(Time_dt))]
Time_dt['Closing_Weekday'] = [closing_hour(x) for x in range(len(Time_dt))]
Time_dt['Opening_Saturday'] = [opening_hour(x) for x in range(len(Time_dt))]
Time_dt['Closing_Saturday'] = [closing_hour(x) for x in range(len(Time_dt))]
Time_dt['Opening_Sunday'] = [opening_hour(x) for x in range(len(Time_dt))]
Time_dt['Closing_Sunday'] = [closing_hour(x) for x in range(len(Time_dt))]
Time_all = pd.concat([Time_1,Time_dt], axis = 1).reset_index()
Time_all.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Tuesday_Files/Time.csv")

##### City, average rating - 1 hr 
import random
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
random.seed(100)
Train, Test = train_test_split(BA, test_size=0.2, random_state=0)
del Train['level_0']
del Test['level_0']
len(Train)
len(Test)
City_rating = pd.DataFrame(Train.groupby(['city'])['stars'].mean()) ##685 different cities
City_rating['city'] = City_rating.index
Train_data = Train.merge(City_rating, how = 'left' , on = 'city').reset_index()
del Train_data['level_0']
Test_data = Test.merge(City_rating, how = 'left', on = 'city').reset_index()
del Test_data['level_0']
Test_data['stars_y'] = Test_data['stars_y'].fillna(0)


####### Merge above columns with columns from Apoorv  at Business level 

#### Merge Categories
Train_data = Train_data.merge(pp, how = 'left', on = 'business_id').reset_index()
Test_data = Test_data.merge(pp, how = 'left', on = 'business_id').reset_index()
del Train_data['level_0']
del Test_data['level_0']

#### Merge Time
Train_data = Train_data.merge(Time_all, how = 'left', on = 'business_id').reset_index()
Test_data = Test_data.merge(Time_all, how = 'left', on = 'business_id').reset_index()
del Train_data['level_0']
del Test_data['level_0']
Train_data.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Tuesday_Files/TrainV1.csv")
Test_data.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Tuesday_Files/TestV1.csv")
##### Merge Review/User info

User_data = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/User_modified(new).csv")
User_sub = User_data[['user_id','average_stars','compliments_received','votes_given','friend_number','yelping_since_year','elite_years']]    
Rev_wotext = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Review_wotext.csv")

### Create new metrics related to users at business level

### Subset the data based on business ids
Rev_sub = Rev_wotext[Rev_wotext['business_id'].isin(Ids3)] ### 3 million records
### Merge with User_sub
Rev_merg = Rev_sub.merge(Rev_sub, how = 'left', on = 'user_id')
#### Creating the User metrics at business level




######### Save both training and testing separately



################# Just use the text of the tweet (combine multiple to one) and along with other's
##try building a multi class classification and see what's the accuracy!! - [4 hrs]

##### With user, review but with no review text - just emply dtree to see how it's working!!
import pandas as pd
Train =pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Tuesday_Files/TrainV1.csv")
Test = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Tuesday_Files/TestV1.csv")

########## User, review along with text 
from sklearn import tree
from sklearn.metrics import confusion_matrix
X_train_1 = Train.ix[:,18:53]
X_train_2 = Train.ix[:,[54,55,56,57,70,71,72,73,74,75,76,77,78]]
X_train =  pd.concat([X_train_1, X_train_2], axis = 1).reset_index(drop = True)
Train['stars_x'] = Train['stars_x'].astype('category')
Y_train = Train.stars_x
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, Y_train)
Y_pred = clf.predict(X_test)
print(confusion_matrix(Y_test, Y_pred))















