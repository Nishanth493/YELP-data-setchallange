############# Reading all the data sets ###############
#### Trying to convert Attributes section of Business data into separate columns 
import pandas as pd
import numpy as np
Business = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/yelp_academic_dataset_business.csv")
from itertools import izip_longest
new_cols = Business(list(izip_longest(Business[1].apply(lambda x:x.split(",")), fillvalue="")))
User = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/yelp_academic_dataset_user.csv")

########## Need to make the attributes into separate columns
import string
dictionary = []
dictionary1 = list(set(dictionary))
dictionary2 = list(set(dictionary1))
dictionary2_df = pd.DataFrame(dictionary2)
dictionary2_df = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Dict_Attribute.csv")
dictionary2 = dictionary2_df['0']
for i in range(140852,len(Business)):
    print(i)
    ncol = np.where(Business.ix[i,17:].notnull() == False)[0][0] + 17
    for j in range(17, ncol):
        dictionary1 = dictionary1 + [Business.ix[i,j].split(":")[-2].translate(None, string.punctuation)]

Attribute = pd.DataFrame()

len(Business)
### For row loop
for i in range(122533, len(Business)):
    #print(i)
    ncol = np.where(Business.ix[i,17:].notnull() == False)[0][0] + 17
    Att_list = [Business['business_id'][i]]
    for k in range(0, len(dictionary2)):
        a = dictionary2[k].strip()
        for j in range(17, ncol):
            splstr = Business.ix[i,j].split(a)
            if len(splstr) > 1:
                break
        if len(splstr) > 1:
            #print(k)
            Att_list = Att_list + [splstr[-1].translate(None, string.punctuation).strip()]
        else:
            Att_list = Att_list + ['NaN']
    Attribute = pd.concat([Attribute, pd.DataFrame(Att_list).transpose()], axis = 0)
    
                
            
Attribute.to_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Attribute4.csv")       




########### Availability % for each features in each data set #########



###### Think of possible attributes/into the clustering model ###########

#======== Business Data =====================#

###(1) Check if the long latitude are sufficient or use postal code/ neighborhood, city , state and country
##Get the no. of unique values of each of the above and try to plot in Tableau

###(2) Review Count - Can split this into number of 5 star, 3 star and 1 star reviews etc.

#### (3) Attributes - Find the most important and see the variation with star rating may be

#### (4) Categories - # unique categories it is identified as , also identify the most common category combinations 
###and  their correlation with final ratings

####(5) Time - ## Duration of open hours, ### Opening Hour ### Closing Hour #==== can be separated at weekday and weekend


##=============== User Data =====================#

#### For each business get all the unique users who have reviewed it

###### Get the summary statistics of all columns and if possible categorize them 

## (1) No. of elite users who reviewed ## (2) Average star given by elite users 
##(3) Average funny voted value of user who reviewed this 'Compliment_funny'
## (4) Average age of the yelp user or the longest yelper review received



