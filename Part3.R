#============== Part 3 ==========================#
library(rpart)
library(caret)
## Reading the training and test data sets created in python
Train = read.csv("C:/Users/saketha lakshmi/Documents/JOBS/Cogitativo/Train.csv")
Test = read.csv("C:/Users/saketha lakshmi/Documents/JOBS/Cogitativo/Test.csv")

## Converting to factor variables
col_names = c('Claim.Line.Number','Provider.ID','Line.Of.Business.ID','Revenue.Code', 'Service.Code', 'Procedure.Code', 'Diagnosis.Code','In.Out.Of.Network',
              'Reference.Index', 'Pricing.Index','Capitation.Index', 'Claim.Type', 'Claim.Subscriber.Type', 'Network.ID')
Data = rbind(Train, Test)
for (i in 1:14){
  column = col_names[i]
  Data[,column] = as.factor(Data[,column]) 
}

Train = Data[1:nrow(Train),2:17]
X_Test = Data[nrow(Train)+1:nrow(Data),1:ncol(Data) - 1]
y_test = Test$Outcome

#=================Decision Tree ==========================#
train.cart <- rpart(Outcome ~ .,
                    data = Train,
                    method = "class")
summary(train.cart)
importance = varImp(train.cart, scale = TRUE)
print(importance)
#plot(importance)
pred <- predict(train.cart, newdata = X_Test, type = 'class')
table(y_test, pred)
prp(train.cart, digits = 3)
## Accuracy is 91.04%

#===========Random Forest ====================#
library(randomForest)
req_cols = c('Provider.ID', 'Service.Code', 'Claim.Charge.Acount', 'In.Out.Of.Network','Diagnosis.Code','Line.Of.Business.ID', 'Procedure.Code',
             'Reference.Index', 'Pricing.Index','Capitation.Index', 'Network.ID', 'Outcome')
Train1 = Train[,which(names(Train) %in% req_cols)]
req_cols1 = c('Provider.ID','Revenue.Code', 'Service.Code', 'Claim.Charge.Acount', 'In.Out.Of.Network',
              'Reference.Index', 'Pricing.Index','Capitation.Index', 'Claim.Type', 'Claim.Subscriber.Type', 'Network.ID')
X_Test1 = X_Test[,which(names(X_Test) %in% req_cols1)]
train.rf = randomForest(factor(Outcome) ~ ., data = Train1, na.action = na.exclude)
summary(train.rf)
importance(train.rf)
pred_rf <- predict(train.rf, newdata = X_Test1, na.action = na.exclude)
#summary(pred)
table(y_test, pred_rf)

### Accuracy is 91.15%  
table(y_test)
##Baseline accuracy is 79.23%
