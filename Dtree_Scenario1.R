
####### 242 project
######## Decision Tree for Scenario 1
library(rpart)
library(ctree)
library(partykit)
### Read the dataset
Train =read.csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Tuesday_Files/TrainV1.csv")
Test = read.csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Tuesday_Files/TestV1.csv")
Train$stars_x = as.factor(Train$stars_x) 
#Train$postal_code = as.factor(Train$postal_code)
#Test$postal_code = as.factor(Test$postal_code)
X_train = Train[,c(15,19:58,71:79)]
X_test = Test[,c(19:58,67:75)]
colnames(Test)[55:58] = c('Restaurants_x','Shopping_x','Food_x','Cat_count_x') 
###### Run a decision tree
train.cart <- rpart(stars_x ~ .,
                    data = X_train,
                    method = "class")
summary(train.cart)
pred <- predict(train.cart, newdata = X_test, type = 'response')
summary(pred)
table(Test$stars_x, pred)
table(loans.test$not.fully.paid, predTest > 0.5)


######### To find correlation matrix
