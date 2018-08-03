#import json
#from pprint import pprint
import os
os.chdir("C:/Users/saketha lakshmi/Documents/IEOR242/Project/yelp_dataset_challenge_round9/yelp_dataset_challenge_round9~/")

with open('yelp_academic_dataset_checkin.json') as data_file:
    data = json.load(data_file)
print(data)
    
    
import json
import pandas as pd
from glob import glob

def convert(x):
    ''' Convert a json string to a flat python dictionary
    which can be passed into Pandas. '''
    ob = json.loads(x)
    for k, v in ob.items():
        if isinstance(v, list):
            ob[k] = ','.join(v)
        elif isinstance(v, dict):
            for kk, vv in v.items():
                ob['%s_%s' % (k, kk)] = vv
            del ob[k]
    return ob

for json_filename in glob('*.json'):
    print(json_filename)
    csv_filename = '%s.csv' % json_filename[:-5]
    print 'Converting %s to %s' % (json_filename, csv_filename)
    df = pd.DataFrame([convert(line) for line in file(json_filename)])
    df.to_csv(csv_filename, encoding='utf-8', index=False)
 
########### Read the data sets and make sure everything looks right

business = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/yelp_dataset_challenge_round9/yelp_dataset_challenge_round9~/yelp_academic_dataset_business.csv")
checkin = pd.read_csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/yelp_dataset_challenge_round9/yelp_dataset_challenge_round9~/yelp_academic_dataset_checkin.csv")
tip = pd.read_csv("yelp_academic_dataset_tip.csv")
user = pd.read_csv("yelp_academic_dataset_user.csv")
review = pd.read_csv("yelp_academic_dataset_review.csv")
