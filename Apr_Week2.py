###############Reading all the data sets ###############
#### Trying to correct Cities Column and add attrbitures section
import pandas as pd
import numpy as np
import string
import re
Business = pd.read_csv("C:/Users/Nishanth/Documents/IEOR242/Project/DataSets/yelp_academic_dataset_business.csv")
Cities = [set(Business['Cities'])]
City_df = pd.DataFrame(Cities)
City_df = pd.DataFrame(City_df.transpose())
City_df.columns = ['Cities']
City_df['New_City'] = City_df['Cities']
Cities = City_df['Cities']
#### Remove non english characters
Business['Cities'] = [re.sub("[^a-zA-Z]", "", str(Business['city'][x])) for x in range(len(Business))]
Cities = set(Business['Cities']) # 850 unique cities information

####### Use selenium code to get the new match

from explicit import waiter, ID
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.common.exceptions import StaleElementReferenceException
NO_SUGGESTION = 'Add a missing place to Google Maps.'
def get_name_suggestion(driver, name):
    # Find the search box, clear it, write the name
    waiter.find_write(driver, 'searchboxinput', name, by=ID, clear_first=True)

    class SuggestionLoads(object):
        def __init__(self):
            self._last_seen = None

        def __call__(self, driver):
            """ Custom expected condition.
                Returns either the first suggested name, or '<No Suggestion>'
                Raises a TimeoutException in the event the page source is different
            """
            suggestion_icon = 'div.suggest-icon-container'
            suggest_css = 'div.suggest-left-cell > span.suggest-query'
            try:

                # Only want suggestions that have the location icon next to them, and not the
                # magnifying glass. Return False if we don't find any so as to retry
                icons = driver.find_elements_by_css_selector(suggestion_icon)
                if len(icons) < 1:
                    return False

                elems = driver.find_elements_by_css_selector(suggest_css)

                if len(elems) == 0:
                    # No suggestions have loaded yet, return False so the Wait can retry
                    return False

                suggest_text = elems[0].text
                if len(suggest_text) == 1:
                    # Sometimes we catch text mid-update. Return False to retry
                    # and hopefully get the whole suggestion
                    return False
                elif suggest_text == NO_SUGGESTION:
                    # Google has no suggestion for us, return NO_SUGGESTION, which the Wait will
                    # evaluate as True and exit
                    return '<No Suggestion>'
                else:
                    # We found a valid suggestion. We need to make sure nothing else is going to
                    # get AJAXed in, so compare it to or _last_seen property. If they match,
                    # everything has stabilized and return the string, which will be evaluated as
                    # True and cause the Wait to exit
                    # If you don't do this, you wind up with jung suggestions like "Traffic"
                    if suggest_text == self._last_seen:
                        return suggest_text
                    else:
                        self._last_seen = suggest_text
                        return False

            except StaleElementReferenceException:
                # Because the DOM is constantly updating, there is a pretty decent chance that a
                # SERE will get thrown. Catch it if it does and return False so the Wait
                # can try again
                return False

    return Wait(driver, 30).until(SuggestionLoads())


def main():
    driver = webdriver.Chrome()
    k = 0
    try:
        driver.get("http://maps.google.com")
        driver.maximize_window()
        for orig_name in Cities:
            suggested_name = get_name_suggestion(driver, orig_name)
            City_df['New_City'][k] = suggested_name.strip()
            print(k)
            #print "{0}: {1}".format(orig_name, suggested_name.encode('utf-8').strip())
            k = k + 1
    finally:  # This is useful to make sure the browsers get closed, even if an exception is thrown
        driver.quit()



if __name__ == "__main__":
    main()
    

######## Read all business-attributes files 
Att1 = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Attribute1.csv")
Att2 = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Attribute2.csv")
Att3 = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Attribute3.csv")
Att4 = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Attribute4.csv")
Att5 = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Attribute5.csv")
#Att5 = Attribute
len(Att1)
len(Att2)
len(Att3)
Att_13 = Att1.append(Att2, ignore_index = True)
Att_13 = Att_13.append(Att3, ignore_index = True)
Att_14 = Att_13.append(Att4, ignore_index = True)
Att_15 = Att_14.append(Att5, ignore_index = True)
Att15 = Att_15.drop_duplicates(['0']).reset_index() #en 142251
Att15.rename(columns={'0': 'business_id'}, inplace=True)
Att15.columns = ['index','Unnamed','business_id'] + list(dictionary2)
Att15.to_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Attribute_all.csv")
Business_Ids_Captured = Att_14['Business_Id']
AllBusiness = Business['business_id']
NotCaptured = list(set(AllBusiness) - set(Business_Ids_Captured)) 


############### Re running the attribute code for these not captured business

Attribute = pd.DataFrame()

for i in range(0, len(NotCaptured)):
    print(i)
    id = NotCaptured[i]
    loc = np.where(Business['business_id'] == id)[0]
    ncol = np.where(Business.ix[loc,17:].notnull() == False)[0][0] + 17
    Att_list = [id]
    for k in range(0, len(dictionary2)):
        a = dictionary2[k].strip()
        for j in range(17, ncol):
            splstr = Business.ix[loc,j].split(a)
            if len(splstr) > 1:
                break
        if len(splstr) > 1:
            #print(k)
            Att_list = Att_list + [splstr[-1].translate(None, string.punctuation).strip()]
        else:
            Att_list = Att_list + ['NaN']
    Attribute = pd.concat([Attribute, pd.DataFrame(Att_list).transpose()], axis = 0)
    
                
            
Attribute.to_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Attribute5.csv")       

### Drop the 50 odd columns
Business_V1 = Business.ix[:,0:16]
Business_V2 = Business_V1.merge(Att15, how = 'left' , on = 'business_id')


#### Merge the business data with attribute column, city column
City_df.rename(columns = {'Cities':'city'}, inplace = True)
Business_V3 = Business_V2.merge(City_df, how = 'left', on = 'city')
City_df['Tp'] = [City_df['New_City'][x].encode('utf-8').strip() for x in range(len(City_df))]
### Save the final data
del Business_V3['New_City']
Business_V3.to_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Business_CityAtt.csv")
