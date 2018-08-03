##=============New Feature Extraction=========================##
import pandas as pd
### Read user data
#User = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/yelp_academic_dataset_user.csv")
User_new = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/User_modified(new).csv")
#### Yelping years - already there
### Elite years - already there
## Fans - already present 
###Compliments already present
### Friends already present
####Elite starting year
User_new['Elite_start'] = [min(User_new['elite'][x].split(',')) for x in range(len(User_new))]

### Yelping year
User_new['Yelp_start'] = [User_new['yelping_since'][x].split('-')[0] for x in range(len(User_new))]

### Yelping age in days
from datetime import datetime
User_new['Yelp_age_days'] = [(datetime.strptime('2017-04-27' , '%Y-%m-%d') - datetime.strptime(User_new['yelping_since'][x] , '%Y-%m-%d')).days for x in range(len(User_new))] 

### Elite diff since start
def elite_timetaken(x):
    if User_new['Elite_start'][x] == 'None':
        return('None')
    else:
        return(int(User_new['Elite_start'][x]) - int(User_new['Yelp_start'][x]) + 1)
        
User_new['Elite_timetaken'] = [elite_timetaken(x) for x in range(len(User_new))]

##================= Read review data (withhout text) ===================#
Rev = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Review_wotext.csv")
Rev.columns.values
Rev = Rev[Rev['funny'] != 'aZs_IrhA7rvuLBumVhJjCw'] ## Cleaning it up
#### Average stars per user
Avg_star = Rev.groupby(['user_id'])['stars'].mean()
Avg_star = pd.DataFrame(Avg_star)
Avg_star['user_id'] = Avg_star.index


### Total no. of funny votes per user
Rev['funny'] = Rev['funny'].astype(int)
Total_funny = Rev.groupby(['user_id'])['funny'].sum()
Total_funny = pd.DataFrame(Total_funny)
Total_funny['user_id'] = Total_funny.index
Total_funny.head()

### Total no. of useful votes per user
Total_useful = Rev.groupby(['user_id'])['useful'].sum()
Total_useful = pd.DataFrame(Total_useful)
Total_useful['user_id'] = Total_useful.index
Total_useful.head()

### Total no of cool votes per user
Rev['cool'] = Rev['cool'].astype(int)
Total_cool = Rev.groupby(['user_id'])['cool'].sum()
Total_cool = pd.DataFrame(Total_cool)
Total_cool['user_id'] = Total_cool.index
Total_cool.head()

### Count of reviews with rating X(round it off) 1 to 5
Star_1= (Rev[Rev['stars'] == 1]).groupby(['user_id']).size()
Star_1 = pd.DataFrame(Star_1)
Star_1['user_id'] = Star_1.index
Star_1.columns = ['star_1','user_id']

Star_2= (Rev[Rev['stars'] == 2]).groupby(['user_id'])['stars'].size()
Star_2 = pd.DataFrame(Star_2)
Star_2['user_id'] = Star_2.index
Star_2.columns = ['star_2','user_id']

Star_3= (Rev[Rev['stars'] == 3]).groupby(['user_id'])['stars'].size()
Star_3 = pd.DataFrame(Star_3)
Star_3['user_id'] = Star_3.index
Star_3.columns = ['star_3','user_id']

Star_4= (Rev[Rev['stars'] == 4]).groupby(['user_id'])['stars'].size()
Star_4 = pd.DataFrame(Star_4)
Star_4['user_id'] = Star_4.index
Star_4.columns = ['star_4','user_id']

Star_5= (Rev[Rev['stars'] == 5]).groupby(['user_id'])['stars'].size()
Star_5 = pd.DataFrame(Star_5)
Star_5['user_id'] = Star_5.index
Star_5.columns = ['star_5','user_id']

##business type review count
Rev_b = Rev.groupby(['user_id'])['business_id'].nunique()
Rev_b = pd.DataFrame(Rev_b)
Rev_b['user_id'] = Rev_b.index

### Merge all of the above files
mm1 = Avg_star.merge(Total_funny, how = 'left', on = 'user_id')
mm2 = mm1.merge(Total_useful, how = 'left', on = 'user_id')
mm3 = mm2.merge(Total_cool, how = 'left', on = 'user_id')
mm4 = mm3.merge(Star_1, how = 'left', on = 'user_id')
mm5 = mm4.merge(Star_2, how = 'left', on = 'user_id')
mm6 = mm5.merge(Star_3, how = 'left', on = 'user_id')
mm7 = mm6.merge(Star_4, how = 'left', on = 'user_id')
mm8 = mm7.merge(Star_5, how = 'left', on = 'user_id')
mm8 = mm8.fillna(0)

Rev = Rev.merge(mm8, how = 'left', on = 'user_id')
Rev = Rev.merge(Rev_b, how = 'left', on = 'user_id')
## ==================Read business data =========================#
Bussiness = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Business_CityAtt.csv")
Bus_sub = Bussiness[['business_id','postal_code','city','state']]
Bus_sub.columns = ['business_id_x','postal_code','city','state']
### Merge with above rev data
Rev_bus = Rev.merge(Bus_sub, how = 'left', on = 'business_id_x')
Rev_bus.head()
##total no. of postal codes reviewed by user
Tot_pcodes = Rev_bus.groupby(['user_id'])['postal_code'].nunique()
Tot_pcodes = pd.DataFrame(Tot_pcodes)
Tot_pcodes['user_id'] = Tot_pcodes.index
Tot_pcodes.columns = ['pc_count','user_id']
## total no. of cities reviewed by user
Tot_cities = Rev_bus.groupby(['user_id'])['city'].nunique()
Tot_cities = pd.DataFrame(Tot_cities)
Tot_cities['user_id'] = Tot_cities.index
Tot_cities.columns = ['city_count','user_id']
##total no. of states reviewed by state
Tot_state = Rev_bus.groupby(['user_id'])['state'].nunique()
Tot_state = pd.DataFrame(Tot_state)
Tot_state['user_id'] = Tot_state.index
Tot_state.columns = ['state_count','user_id']
Bus1 = Rev_bus.merge(Tot_pcodes, on = 'user_id', how = 'left')
Bus2 = Bus1.merge(Tot_cities, on = 'user_id', how = 'left')
Review_Business = Bus2.merge(Tot_state, on = 'user_id', how = 'left')

##====================Read Tips data =================================##
tips = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/yelp_academic_dataset_tip.csv")
tips.head()
### Count of total tips created per user
Total_tips = tips.groupby(['user_id']).size()
Total_tips = pd.DataFrame(Total_tips)
Total_tips['user_id'] = Total_tips.index
Total_tips.columns = ['tip_count', 'user_id']

##### Total tip likes
Total_likes = tips.groupby(['user_id'])['likes'].sum()
Total_likes = pd.DataFrame(Total_likes)
Total_likes['user_id'] = Total_likes.index
Total_likes.head()

### Business type tips count
Tip_business = tips.groupby(['user_id'])['business_id'].nunique()
Tip_business = pd.DataFrame(Tip_business)
Tip_business['user_id'] = Tip_business.index
Tip_business.head()

tip1 = Total_tips.merge(Total_likes, on = 'user_id')
tip2 = tip1.merge(Tip_business, on = 'user_id')

#============= Merge all required data sets ==================#

### Merge with user data
RBU = User_new.merge(Review_Business, on = 'user_id', how = 'left')
RBU_1  = RBU.drop_duplicates(['user_id'])
RBU_1.head()
RBU_1.tail()
len(RBU_1)
### Merge with tips data
RBUT = RBU_1.merge(tip2, on = 'user_id', how = 'left')
RBUT.head()
RBUT.tail()
RBUT= pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Wed_alldata.csv")
### Drop unnecessary columns
def elite(x):
    if RBUT['elite'][x] == 'None':
        return(0)
    else:
        return(1)
RBUT['Response'] = [elite(x) for x in range(len(RBUT))]
Part1= RBUT.ix[:,3:15].reset_index()
Part3 = RBUT.ix[:,[16,18,19,20,23,27,29,30,54,55,56,57,58,59,60]].reset_index()
Part2 = RBUT.ix[:,41:51].reset_index()
FinalData =  pd.concat([Part1, Part2, Part3], axis = 1).reset_index(drop = True)
## Length of final data is 1029432
### Replace 'NA' with 0
FinalData = FinalData.fillna(0)
##Create the predictor variable

### Drop columns with elite information 
del FinalData['index']

###Save the final file
FinalData = FinalData.rename(columns = {'stars_y':'avg_stars','funny_y':'funny_review','useful_y':'useful_review','cool_y':'cool_review','business_id_y':'bus_type_review','business_id':'bus_type_tip'})
FinalData.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Wed_cleandata_v2.csv")
FinalData=pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Wed_cleandata_v2.csv")

##======================= Training and Testing Split ============================#
import random
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn import tree
random.seed(100)
Train, Test = train_test_split(FinalData, test_size=0.2, random_state=0)
Train.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Wed_Train_v2.csv")
Test.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Wed_Test_v2.csv")
Y_train = Train.Response
Y_test = Test.Response
X_train = Train.ix[:,0:36]
X_test = Test.ix[:,0:36]
### Default accuracy = 95.19%

##==============Dtree ==================#
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, Y_train)
Y_pred = clf.predict(X_test)
print(confusion_matrix(Y_test, Y_pred)) ### 97.206%

##============LR===========================#
from sklearn import linear_model
logreg2 = linear_model.LogisticRegression()
logreg2 = logreg2.fit(X_train,Y_train)                        
y_pred1 = logreg2.predict(X_test)
print(confusion_matrix(Y_test, y_pred1)) ### 97.16%

##================RF=====================#
from sklearn.ensemble import RandomForestClassifier
clf_2 = RandomForestClassifier()  
clf_2= clf_2.fit(X_train, Y_train)   
clf_2.features_importances_
Y_pred2 = clf_2.predict(X_test)
print(confusion_matrix(Y_test, Y_pred2)) ### 97.97%

##===============Boosting ===================#

from sklearn.ensemble import GradientBoostingClassifier
clf_3 = GradientBoostingClassifier()  
clf_4= clf_3.fit(X_train, Y_train)   
Y_pred3 = clf_4.predict(X_test)
print(confusion_matrix(Y_test, Y_pred3)) #### 98.09%


######================Box Plots ====================#

sub = FinalData[['friend_number','Response']]
sub.columns = ['Friends_Count','Response']
#sub1 = sub[sub['Response'] == 1]
#pd.crosstab(index = sub1['Elite_timetaken'], columns = 'count', margins = True)
sub.boxplot('Friends_Count', by = 'Response') 
plt.ylim(0,400)
plt.show()



