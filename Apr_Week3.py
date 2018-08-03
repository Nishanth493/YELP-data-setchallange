####### Reading Deepika's columns + My earlier data + Create a column with average
import pandas as pd
######## Read saketa's updated data
SakData = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Business_CityAtt.csv")
SakData['review_count'].describe()
### Deepika's files
DData1 = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/file_categories.csv")
DData2 = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/file_hours.csv")


######## Read review data
RData = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/yelp_academic_dataset_review.csv")
### Create a data with business id and average review 
len(set(RData['business_id'])) # 144073 same as unique business ids available for us
Business_ReviewFreq = pd.crosstab(index = RData.business_id, columns = 'count', margins = True)
Business_ReviewFreq.head()
Business_ReviewFreq['business_id'] = Business_ReviewFreq.index
Business_AvgRevStar = RData.groupby('business_id')['stars'].mean()
Business_AvgRevStar = pd.DataFrame(Business_AvgRevStar)
Business_AvgRevStar['business_id'] = Business_AvgRevStar.index
Business_Review = Business_ReviewFreq.merge(Business_AvgRevStar, on = 'business_id', how = 'left')

### Merging above both data sets
Merge0 = SakData.merge(Business_Review, on = 'business_id', how = 'left')

### Merge with data and drop unnecessary columns
Merge1 = Merge0.merge(DData1, how = 'left', on = 'business_id')
len(Merge1)
pp =Merge1.columns.values # 1308 columns !!

Merge2 = Merge1.merge(DData2, how = 'left', on = 'business_id')
Merge2.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/MergedData_214.csv")

#### Just the business star and the average review star
Star = Merge2[['business_id','stars_x', 'stars_y']]
Star.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Star.csv")

#########RData drop few columns ##############
RData_V1 = RData[['business_id','cool','date','funny','review_id','stars','type','useful','user_id']]
RData_V1.to_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/Review_wotext.csv")

